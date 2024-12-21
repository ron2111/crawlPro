
import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
from typing import Set, Dict, Optional
import logging
import yaml
import random
from urllib.parse import urljoin, urlparse
from src.utils.validators import URLValidator
from src.utils.exceptions import *
from src.utils.rate_limiter import RateLimiter
from src.utils.html_parser import HTMLParser

class BaseCrawler:
    def __init__(self, config_path: str):
        self.logger = logging.getLogger('e_commerce_crawler')
        self.config = self._load_config(config_path)
        self.visited_urls: Set[str] = set()
        self.rate_limiter = RateLimiter(self.config['requests_per_second'])
        self.session = None
        self.failed_urls: Set[str] = set()

    def _verify_site_accessibility(self, url: str) -> bool:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, headers=headers, timeout=10, verify=True)
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Site verification failed for {url}: {str(e)}")
            return False
        
    async def _init_session(self):
        if not self.session:
            timeout = aiohttp.ClientTimeout(total=self.config['request_timeout'])
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            self.session = aiohttp.ClientSession(
                headers=headers,
                timeout=timeout
            )

    async def _fetch_url(self, url: str, domain: str) -> Optional[str]:
        await self.rate_limiter.acquire(domain)
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        for attempt in range(self.config['max_retries']):
            try:
                async with self.session.get(url, allow_redirects=True) as response:
                    if response.status in [200, 301, 302]:
                        try:
                            return await response.text()
                        except Exception as e:
                            # If aiohttp fails, fallback to requests
                            try:
                                sync_response = requests.get(url, 
                                                          headers=self.session._default_headers,
                                                          timeout=10)
                                return sync_response.text
                            except Exception as e2:
                                self.logger.error(f"Both async and sync requests failed for {url}: {str(e2)}")
                                return None
                    
                    if response.status == 404:
                        self.logger.warning(f"Page not found: {url}")
                        return None
                    
                    if response.status == 429:
                        retry_after = int(response.headers.get('Retry-After', 60))
                        self.logger.warning(f"Rate limited. Waiting {retry_after} seconds.")
                        await asyncio.sleep(retry_after)
                        continue
                    
                    if response.status >= 500:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    
                    self.logger.error(f"HTTP {response.status} for {url}")
                    return None
                    
            except asyncio.TimeoutError:
                self.logger.warning(f"Timeout on attempt {attempt + 1} for {url}")
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                self.logger.error(f"Error fetching {url}: {str(e)}")
                if attempt == self.config['max_retries'] - 1:
                    self.failed_urls.add(url)
                return None
        
        self.failed_urls.add(url)
        return None

    def _extract_urls(self, html: str, base_url: str) -> Set[str]:
        if not html:
            return set()
            
        try:
            parser = HTMLParser(html, base_url)
            urls = parser.extract_urls()
            valid_urls = set()
            
            for url in urls:
                if URLValidator.is_valid_url(url) and URLValidator.should_crawl(url):
                    parsed = urlparse(url)
                    cleaned_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                    valid_urls.add(cleaned_url)
            
            return valid_urls
        except Exception as e:
            self.logger.error(f"Error parsing HTML from {base_url}: {e}")
            return set()

    async def close(self):
        if self.session:
            await self.session.close()
            
    def _load_config(self, config_path: str) -> Dict:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)['crawler']