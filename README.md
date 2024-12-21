# E-commerce Product URL Crawler

A high-performance, scalable web crawler designed to discover product URLs across multiple e-commerce websites. Built with Python using modern async programming practices.

## Features

### Core Features
- Asynchronous crawling with concurrent request handling
- Rate limiting and request throttling
- Domain-specific URL pattern matching
- Automatic compression handling (gzip, deflate, brotli)
- Comprehensive error handling and retry mechanisms
- Progress tracking with tqdm
- Detailed logging system
- Configurable through YAML files

### Technical Highlights
- **Async Architecture**: Uses `aiohttp` for non-blocking I/O operations
- **Fallback Mechanism**: Implements requests library as fallback for robustness
- **Memory Efficient**: Streams responses and implements efficient URL tracking
- **Scalability**: 
  - Concurrent request handling with configurable limits
  - Rate limiting per domain
  - Memory-efficient URL deduplication
  - Configurable retry strategies

## Project Structure
```
e_commerce_crawler/
├── config/
│   └── config.yaml         # Configuration settings
├── src/
│   ├── crawler/
│   │   ├── base_crawler.py    # Base crawling functionality
│   │   ├── product_crawler.py # Product-specific crawler
│   │   └── url_patterns.py    # URL pattern matching
│   └── utils/
│       ├── logger.py          # Logging configuration
│       ├── rate_limiter.py    # Rate limiting
│       ├── html_parser.py     # HTML processing
│       └── validators.py      # URL validation
├── tests/                     # Test suite
├── output/                    # Crawler results
└── run_crawler.py            # Entry point
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/e_commerce_crawler.git
cd e_commerce_crawler
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python run_crawler.py --domains example.com
```

### Multiple Domains
```bash
python run_crawler.py --domains amazon.com flipkart.com myntra.com
```

### Custom Configuration
```bash
python run_crawler.py --domains example.com --config path/to/config.yaml
```

## Example Run
Here's an example run with sharalle.com:
```bash
$ python run_crawler.py --domains sharalle.com
2024-12-21 19:22:40,221 - INFO - Starting crawl for 1 domains
2024-12-21 19:22:40,221 - INFO - Starting crawl for domain: sharalle.com
Crawling sharalle.com: 100%|██████████| 50/50 [00:45<00:00,  1.10it/s]
2024-12-21 19:23:25,826 - INFO - Found 23 product URLs for sharalle.com
2024-12-21 19:23:25,828 - INFO - Results saved to output/product_urls.json
```

## Output
The crawler saves results in JSON format in `output/product_urls.json`:
```json
{
  "sharalle.com": [
    "https://sharalle.com/products/example-product-1",
    "https://sharalle.com/products/example-product-2"
  ]
}
```

## Logging
- Detailed logs are saved in the format: `crawler_YYYYMMDD_HHMMSS.log`
- Logs include:
  - Request/response information
  - Error details and retry attempts
  - Rate limiting events
  - URL discovery progress

## Configuration
Key configurations in `config/config.yaml`:
```yaml
crawler:
  max_concurrent_requests: 10  # Maximum concurrent requests
  request_timeout: 30         # Request timeout in seconds
  max_retries: 3             # Maximum retry attempts
  requests_per_second: 2     # Rate limiting
```

## Testing
Run the test suite:
```bash
pytest tests/
```

Key test areas:
- URL pattern matching
- HTML parsing
- Rate limiting
- Error handling
- Domain validation

## Production Deployment Considerations
1. **Scaling:**
   - Use multiple instances with distributed rate limiting
   - Implement URL queue system (e.g., Redis)
   - Add proxy rotation support

2. **Monitoring:**
   - Add Prometheus metrics
   - Set up alerting for failures
   - Monitor memory usage

3. **Storage:**
   - Implement database storage for results
   - Add result deduplication
   - Set up periodic cleanup

4. **Resilience:**
   - Implement circuit breakers
   - Add IP rotation
   - Set up failover mechanisms

## License
MIT License
