#!/usr/bin/env python3

"""Module define the Cache service"""

import redis
from typing import Callable, Optional, TypeVar, Union, cast
import uuid


T = TypeVar('T')
CacheDataType = Union[str, bytes, int, float]


def get_str(data: bytes) -> str:
    """Gets str from bytes"""
    return data.decode(encoding="utf-8")


def get_int(data: bytes) -> int:
    """Gets int from bytes"""
    return int(get_str(data))


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
