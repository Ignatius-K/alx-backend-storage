#!/usr/bin/env python3

"""Module defines `get_page` and `cache_request` methods"""

from functools import wraps
import redis
import requests  # type: ignore
from typing import Callable, cast


redis_cache = redis.Redis()


def cache_request(func: Callable) -> Callable:
    """Tracks the number of calls a request is made"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        request_key = args[0]
        redis_cache.incr(f"count:{request_key}")

        cached_response = cast(bytes, redis_cache.get(request_key))
        if cached_response:
            return cached_response.decode(encoding='utf-8')

        fresh_response = func(*args, **kwargs)
        redis_cache.set(name=request_key, value=fresh_response)
        redis_cache.expire(request_key, 10)
        return fresh_response
    return wrapper


@cache_request
def get_page(url: str) -> str:
    """Makes request for page

    Args:
        url: The URL for the resource/page

    Return:
        The response ie HTML content
    """
    response: requests.Response = requests.get(url=url)
    return response.text
