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

from typing import Any, Union, Callable, ByteString, Optional
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
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[ByteString], Any]] = None) -> Any:
        """Retrieve data from Redis using a key and optionally apply a conversion function.

        Args:
            key (str): The key for the data stored in Redis.
            fn (Optional[Callable[[Any], Any]]): A callable to convert the data back to its original format.

        Returns:
            Any: The retrieved data, optionally converted by the callable function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieve a string from Redis by decoding the byte data using UTF-8.

        Args:
            key (str): The key for the data stored in Redis.

        Returns:
            Optional[str]: The decoded string, or None if the key does not exist.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieve an integer from Redis.

        Args:
            key (str): The key for the data stored in Redis.

        Returns:
            Optional[int]: The integer value, or None if the key does not exist or cannot be converted.
        """
        return self.get(key, fn=int)
