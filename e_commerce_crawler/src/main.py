import asyncio
import argparse
from src.crawler.product_crawler import ProductCrawler
from src.utils.logger import setup_logger


async def main():
    parser = argparse.ArgumentParser(description='E-commerce Product URL Crawler')
    parser.add_argument('--domains', nargs='+', required=True,
                      help='List of domains to crawl')
    parser.add_argument('--config', default='config/config.yaml',
                      help='Path to config file')
    
    args = parser.parse_args()
    logger = setup_logger()
    
    try:
        crawler = ProductCrawler(args.config)
        await crawler.crawl_domains(args.domains)
    except Exception as e:
        logger.error(f"Crawler failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
