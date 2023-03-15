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
