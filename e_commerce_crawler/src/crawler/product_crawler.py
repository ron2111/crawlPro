from src.crawler.base_crawler import BaseCrawler
from src.utils.url_patterns import URLPatternMatcher
from typing import Dict, List, Set
import asyncio
from tqdm import tqdm
import json
from src.utils.validators import URLValidator

class ProductCrawler(BaseCrawler):
    def __init__(self, config_path: str):
        super().__init__(config_path)
        self.product_urls: Dict[str, Set[str]] = {}
        self.semaphore = asyncio.Semaphore(self.config['max_concurrent_requests'])
        self.url_pattern_matcher = URLPatternMatcher()
    
    async def crawl_domain(self, domain: str):
        self.logger.info(f"Starting crawl for domain: {domain}")
        self.product_urls[domain] = set()
        base_url = f"https://{domain}"
        
        await self._init_session()
        to_visit = {base_url}
        
        with tqdm(desc=f"Crawling {domain}") as pbar:
            while to_visit:
                current_batch = list(to_visit)[:self.config['max_concurrent_requests']]
                to_visit = set(list(to_visit)[self.config['max_concurrent_requests']:])
                
                tasks = [self._process_url(url, domain) for url in current_batch]
                new_urls = await asyncio.gather(*tasks, return_exceptions=True)
                
                for urls in new_urls:
                    if isinstance(urls, set):
                        new_unvisited = {url for url in urls 
                                       if url not in self.visited_urls 
                                       and URLValidator.is_same_domain(url, domain)}
                        to_visit.update(new_unvisited)
                
                pbar.update(len(current_batch))
        
        self.logger.info(f"Found {len(self.product_urls[domain])} product URLs for {domain}")
    
    async def _process_url(self, url: str, domain: str) -> Set[str]:
        async with self.semaphore:
            if url in self.visited_urls:
                return set()
            
            self.visited_urls.add(url)
            
            try:
                html = await self._fetch_url(url, domain)
                extracted_urls = self._extract_urls(html, url)
                
                patterns = self.url_pattern_matcher.get_patterns_for_domain(domain)
                if any(pattern in url.lower() for pattern in patterns):
                    clean_url = URLValidator.clean_url(url)
                    self.product_urls[domain].add(clean_url)
                
                return extracted_urls
            except Exception as e:
                self.logger.error(f"Error processing {url}: {e}")
                return set()
    
    async def crawl_domains(self, domains: List[str]):
        self.logger.info(f"Starting crawl for {len(domains)} domains")
        for domain in domains:
            try:
                await self.crawl_domain(domain)
            except Exception as e:
                self.logger.error(f"Failed to crawl {domain}: {e}")
        
        await self.close()
        self._save_results()
    
    def _save_results(self):
        output = {domain: list(urls) for domain, urls in self.product_urls.items()}
        with open(self.config['output_file'], 'w') as f:
            json.dump(output, f, indent=2)
        self.logger.info(f"Results saved to {self.config['output_file']}")
