class CrawlerException(Exception):
    """Base exception for crawler errors"""
    pass

class RateLimitException(CrawlerException):
    """Raised when rate limit is exceeded"""
    pass

class RobotsExcludedException(CrawlerException):
    """Raised when URL is excluded by robots.txt"""
    pass
