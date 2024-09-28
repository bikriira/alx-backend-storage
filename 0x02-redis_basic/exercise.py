#!/usr/bin/env python3
"""
This module provides a Cache class for storing and managing data in Redis
"""
from functools import wraps
from pprint import pprint
from typing import Any, Union, Callable, ByteString, Optional
import redis
import uuid


def call_history(method: Callable) -> Callable:
    """Decorator to record the history of inputs and outputs for a method.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapper function that logs inputs and outputs in Redis.
    """

    @wraps(method)
    def apply(self, *args):  # kwargs for now are not used
        """Wrapper function that logs method calls in Redis.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the method.

        Returns:
            Any: The output of the original method call.
        """
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        outputs = method(self, *args)
        self._redis.rpush(f"{method.__qualname__}:outputs", str(outputs))
        return outputs

    return apply


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a method is called.

    Args:
        method (Callable[[], Any]): The method to be decorated.

    Returns:
        Callable[[], Any]: The wrapper function that increments the count.
    """

    @wraps(method)
    def incrementer(self, *args, **kwargs):
        """This function is responsible for updating the Redis key and calling the original method.

        Args:
            self: The instance of the class.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.

        Returns:
            Any: The result of the original method call.
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return incrementer


class Cache:
    """A class that provides a caching mechanism using Redis.

    Attributes:
        _redis (redis.Redis): An instance of the Redis client for data storage.

    Example:
        cache = Cache()
        key = cache.store("Some data")
        print(f"Stored data with key: {key}")
    """

    def __init__(self):
        """Initialize the Redis client and clear the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a unique randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored in Redis.

        Returns:
            str: A unique randomly generated key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[ByteString], Any]] = None) -> Any:
        """Retrieves the data associated with the provided key,
           and can optionally apply a conversion function to the retrieved data
           for proper formatting.

        Args:
            key (str): The key for the data stored in Redis.
            fn (Optional[Callable[[ByteString], Any]]): A callable to convert
                the retrieved data to its original format.

        Returns:
            Any: The retrieved data, optionally converted by the callable
                function, or None if the key does not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> Optional[str]:
        """Retrieves the byte data associated with the specified key
           and decodes it using UTF-8 to return a string.

        Args:
            key (str): The key for the data stored in Redis.

        Returns:
            Optional[str]: The decoded string, or None if the key does not
                exist or cannot be decoded.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieves the data associated with the specified key
           and converts it to an integer if possible.

        Args:
            key (str): The key for the data stored in Redis.

        Returns:
            Optional[int]: The integer value, or None if the key does not
                exist or cannot be converted.
        """
        return self.get(key, fn=int)


def replay(method: Callable) -> None:
    """Replays the history of inputs and outputs for the given method.

    Args:
        method (Callable): The method whose call history is being replayed.
    """
    redis = method.__self__._redis
    inputs = [
        i.decode('utf-8') for i in redis.lrange(f"{method.__qualname__}:inputs", 0, -1)
    ]
    outputs = [
        o.decode('utf-8') for o in redis.lrange(f"{method.__qualname__}:outputs", 0, -1)
    ]
    result = tuple(zip(inputs, outputs))
    pprint(result)
    print(f"{method.__qualname__} was called {len(result)} times:")

    for call in result:
        print(f"{method.__qualname__}(*{call[0]}) -> {call[1]}")
