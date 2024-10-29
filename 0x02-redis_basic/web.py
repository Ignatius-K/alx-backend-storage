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
        cache_key = f'cache:{args[0]}'

        cached_response = redis_cache.get(cache_key)
        if cached_response:
            cached_response = cast(bytes, cached_response)
            return cached_response.decode(encoding='utf-8')

        count_key = f'count:{args[0]}'
        fresh_response = func(*args, **kwargs)
        redis_cache.incr(count_key)
        redis_cache.set(name=cache_key, value=fresh_response, ex=10)
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
