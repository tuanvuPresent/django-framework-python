import time
import functools


def cache(timeout):
    memo = {}
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            if args in memo and time.time() - memo[args]['time'] < timeout:
                return memo[args]['result']
            else:
                result = func(*args)
                memo[args] = {'result': result, 'time': time.time()}
                return result
        return wrapper
    return decorator

import time

class Cache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        value, ttl, created = self.cache.get(key, (None, None, None))
        if ttl is not None and time.time() > ttl + created:
            self.delete(key)
            return None
        return value

    def set(self, key, value, ttl=None):
        created = time.time()
        self.cache[key] = (value, ttl, created)

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        self.cache.clear()

    def size(self):
        return len(self.cache)
    
cache = Cache()
