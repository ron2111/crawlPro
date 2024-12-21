from typing import List

class URLPatternMatcher:
    COMMON_PRODUCT_PATTERNS = [
        '/product/',
        '/p/',
        '/item/',
        '/products/',
        '/dp/',
        '/pd/',
        '/buy/',
        '-p-',
        '/catalog/'
    ]

    ECOMMERCE_PLATFORMS = {
        'shopify': [
            '/products/',
            '/collections/*/products/'
        ],
        'woocommerce': [
            '/product/',
            '/shop/'
        ],
        'magento': [
            '/catalog/product/view/'
        ],
        'prestashop': [
            '/*.html'
        ],
        'amazon': [
            '/dp/',
            '/gp/product/',
            '/gp/aw/d/',
            'Amazon.com:'  
        ],
        'flipkart': [
            '/p/itm',
            '/dl/',
            'product-reviews',
            '/viewall/itemid/'
        ],
        'myntra': [
            '/buy/',
            '/product-detail/',
            '/shop/product/',
            '-p-'
        ],
        'ajio': [
            '/p/',
            '/prod/'
        ],
        'snapdeal': [
            '/product/',
            '/products/'
        ],
        'nykaa': [
            '/p/',
            '/products/'
        ],
        'meesho': [
            '/product/',
            '/products/',
            '/item/'
        ],
        'tatacliq': [
            '/p-',
            '/product-details/'
        ]
    }

    @staticmethod
    def get_patterns_for_domain(domain: str) -> List[str]:
        patterns = URLPatternMatcher.COMMON_PRODUCT_PATTERNS.copy()
        
        for platform, platform_patterns in URLPatternMatcher.ECOMMERCE_PLATFORMS.items():
            if platform in domain:
                patterns.extend(platform_patterns)
        
        
        domain_specific_patterns = {
            'amazon': ['/s?k=', '/s?rh=', '/s?ref='],  
            'flipkart': ['&pid=', '&lid=', '/search?q='],
            'myntra': ['/shop/', '/search?q=']
        }
        

        for known_domain, specific_patterns in domain_specific_patterns.items():
            if known_domain in domain:
                patterns.extend(specific_patterns)
        
        return patterns