#!/usr/bin/env python3

"""Module define the Cache service"""

from functools import wraps
import redis
from typing import Callable, List, Optional, TypeVar, Union, cast
import uuid


T = TypeVar('T')
CacheDataType = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """Wrapper that counts times a function is called

    Args:
        func: The function to be counted

    Return:
        The wrapped function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if isinstance(self, Cache):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the call history of wrapped functions"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not isinstance(self, Cache):
            return method(self, *args, **kwargs)
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


class Cache(object):
    """Cache Service

    This defines the service in charge of
    caching

    Implemented on top of Redis
    """

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: Union[int, str] = 6379,
    ) -> None:
        """Initializes our Cache instance

        Attr:
            _redis: The Redis instance
        """
        self._redis = redis.Redis(host=host, port=int(port))
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: CacheDataType) -> str:
        """Stores data in Cache

        Args:
            data: The data to be stored

        Return:
            (UUID) The key to the data in the store
        """
        key = self.generate_data_key()
        with self._redis.pipeline() as pipe:
            pipe.set(key, data)
            pipe.execute()
        return key

    def get(
        self, key: str, fn: Optional[Callable[[bytes], T]] = None
    ) -> Union[T, bytes]:
        """Gets data from the Cache

        Args:
            key: The data key
            fn: The function to format the data
        """
        byte_data = cast(bytes, self._redis.get(key))
        return fn(byte_data) if fn is not None else byte_data

    def get_str(self, key: str) -> str:
        """Gets string value from cache"""
        return cast(str, self.get(key, lambda x: x.decode(encoding="utf-8")))

    def get_int(self, key: str) -> int:
        """Gets int data from cache"""
        return int(self.get_str(key))

    def generate_data_key(self) -> str:
        """Gets a new key"""
        while True:
            key = str(uuid.uuid4())
            if not self._redis.exists(key):
                return key


def replay(method: Callable) -> None:
    """Replay the calls of the method

    Prints the inputs and outputs of the methods
    as stored in the cache store in order

    Args:
        method: The method
    """
    if method is None or not hasattr(method, "__self__"):
        return
    cache = getattr(method, "__self__")
    if not isinstance(cache, Cache):
        return

    method_name = method.__qualname__
    key_inputs = '{}:inputs'.format(method_name)
    key_outputs = '{}:outputs'.format(method_name)
    print(f'{method_name} was called {cache.get_int(method_name)} times:')
    for input, output in zip(
            cast(List, cache._redis.lrange(key_inputs, 0, -1)),
            cast(List, cache._redis.lrange(key_outputs, 0, -1))
    ):
        print(f'{method_name}(*{input.decode("utf-8")})' +
              f'-> {output.decode("utf-8")}')
