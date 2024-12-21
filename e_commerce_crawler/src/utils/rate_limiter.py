import asyncio
from datetime import datetime, timedelta
from typing import Dict, List

class RateLimiter:
    def __init__(self, requests_per_second: int = 2):
        self.requests_per_second = requests_per_second
        self.domain_timestamps: Dict[str, List[datetime]] = {}
    
    async def acquire(self, domain: str):
        if domain not in self.domain_timestamps:
            self.domain_timestamps[domain] = []
        
        now = datetime.now()
        self.domain_timestamps[domain] = [
            ts for ts in self.domain_timestamps[domain]
            if now - ts < timedelta(seconds=1)
        ]
        
        if len(self.domain_timestamps[domain]) >= self.requests_per_second:
            await asyncio.sleep(1)
            self.domain_timestamps[domain] = []
        
        self.domain_timestamps[domain].append(now)
