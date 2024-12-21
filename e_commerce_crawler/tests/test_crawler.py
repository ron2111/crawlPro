import pytest
import asyncio
from src.crawler.product_crawler import ProductCrawler
from src.utils.url_patterns import URLPatternMatcher
from src.utils.validators import URLValidator

@pytest.fixture
def config_path():
    return 'config/config.yaml'

@pytest.fixture
def crawler(config_path):
    return ProductCrawler(config_path)

@pytest.mark.asyncio
async def test_crawl_domain(crawler):
    domain = "example.com"
    await crawler.crawl_domain(domain)
    assert domain in crawler.product_urls
    await crawler.close()

def test_url_pattern_matcher():
    patterns = URLPatternMatcher.get_patterns_for_domain("myshopify.com")
    assert '/products/' in patterns
    assert '/product/' in patterns

def test_url_validator():
    assert URLValidator.is_valid_url('https://example.com/product/123')
    assert not URLValidator.is_valid_url('not_a_url')
    
    assert URLValidator.should_crawl('https://example.com/product/123')
    assert not URLValidator.should_crawl('https://example.com/image.jpg')
    
    assert URLValidator.is_same_domain('https://example.com/path', 'example.com')
    assert URLValidator.is_same_domain('https://sub.example.com/path', 'example.com')
    assert not URLValidator.is_same_domain('https://other.com/path', 'example.com')

@pytest.mark.asyncio
async def test_multiple_domains(crawler):
    domains = ["example1.com", "example2.com"]
    await crawler.crawl_domains(domains)
    for domain in domains:
        assert domain in crawler.product_urls
