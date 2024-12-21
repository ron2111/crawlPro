from urllib.parse import urlparse

class URLValidator:
    EXCLUDED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.css', '.js'}
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def should_crawl(url: str) -> bool:
        lower_url = url.lower()
        return not any(lower_url.endswith(ext) for ext in URLValidator.EXCLUDED_EXTENSIONS)
    
    @staticmethod
    def is_same_domain(url: str, domain: str) -> bool:
        try:
            parsed = urlparse(url)
            return parsed.netloc == domain or parsed.netloc.endswith(f".{domain}")
        except Exception:
            return False
    
    @staticmethod
    def clean_url(url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
