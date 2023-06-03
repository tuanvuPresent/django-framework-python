import re
import time

from django.conf import settings
from django.contrib.admindocs.views import simplify_regex
from redis.client import Redis
from rest_framework.exceptions import Throttled

redis_cache = Redis.from_url(settings.REDIS_CACHE)


def path_pattern(request):
    if request.resolver_match is None:
        return None

    PATH_PARAMETER_PATTERN = (
        r"(?:[^/]*?)<(?:(?:.*?:))*?(\w+)>(?:(?:[^/]*?\[\^[^/]*/)?[^/]*)"
    )
    path_regex = re.compile(PATH_PARAMETER_PATTERN)
    route = path_regex.sub(r"{\1}", request.resolver_match.route)
    if route[:1] == "^":
        route = route[1:]
    if route[-1:] == "$":
        route = route[:-1]
    return f"/{route}"


def rate_limit(max_requests, timeout):
    def decorator(view_func):
        def wrapped_view(request, *args, **kwargs):
            ident = request.user.id if request.user.is_authenticated else request.META.get('REMOTE_ADDR', '')
            cache_key = f'rate_limit:{request.method}-{simplify_regex(request.resolver_match.route)}-{ident}'

            current_time = time.time()
            redis_cache.zremrangebyscore(cache_key, 0, current_time - timeout)
            request_count = redis_cache.zcard(cache_key)
            if request_count >= max_requests:
                raise Throttled()

            redis_cache.zadd(cache_key, {current_time: current_time})
            redis_cache.expire(cache_key, timeout)
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator
