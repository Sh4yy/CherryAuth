from cachetools import TTLCache
from datetime import timedelta


# class VerifyCache(CacheEngine):
#
#     ttl_cache = TTLCache(maxsize=1000, ttl=timedelta(seconds=30).seconds)
#
#     async def get(self, request: Request):
#         """ query cache for response """
#         return self.ttl_cache.get(request.headers.get('Authorization'))
#
#     async def store(self, request: Request, response):
#         """ if response code is 200, store response in cache """
#         if response.status_code == 200:
#             self.ttl_cache[request.headers.get('Authorization')] = response
