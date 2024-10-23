#!/usr/bin/env python3

"""Module define the Cache service"""

import redis
from typing import Union
import uuid


CacheDataType = Union[bytes, float, int, str]


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
        key = self.get_key()
        with self._redis.pipeline() as pipe:
            pipe.set(key, data)
            pipe.execute()
        return key

    def get_key(self) -> str:
        """Gets a new key"""
        while True:
            key = str(uuid.uuid4())
            if not self._redis.exists(key):
                return key
