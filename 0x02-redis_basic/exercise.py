#!/usr/bin/env python3
"""
This module provides a Cache class for storing data in Redis using randomly generated keys.

The Cache class allows data of types str, bytes, int, or float to be stored in a Redis database,
and returns the unique key associated with the stored data.

Example:
    cache = Cache()
    key = cache.store("Some data")
    print(f"Stored data with key: {key}")
"""

from typing import Any, Union
import redis
import uuid


class Cache:
    """Cache class for storing data in Redis with randomly generated keys.

    Attributes:
        _redis (redis.Redis): Instance of Redis client.
    """

    def __init__(self):
        """Initialize the Redis client and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The randomly generated key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, str(data))
        return key
