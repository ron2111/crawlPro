from bs4 import BeautifulSoup
from typing import Set
from urllib.parse import urljoin

class HTMLParser:
    def __init__(self, html: str, base_url: str):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.base_url = base_url
    
    def extract_urls(self) -> Set[str]:
        urls = set()
        for link in self.soup.find_all('a', href=True):
            url = urljoin(self.base_url, link['href'])
            urls.add(url)
        return urls
