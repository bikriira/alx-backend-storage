#!/usr/bin/env python3
"""
This module provides a simple caching system using Redis for
storing and retrieving HTML content of web pages.

Features:
- Tracks the number of accesses for each URL.
- Caches HTML content of the URL in Redis with a 10-second expiration time.
- Optionally, measures and displays the execution time of each
  request (uncomment the timing decorator for this feature).
"""
from typing import Callable
import requests
import redis

redis_client = redis.Redis()


def cacher(f: Callable) -> Callable:
    """Decorator that caches the result of a function.

    Args:
        f (Callable): The function to be cached.

    Returns:
        Callable: A wrapper function that implements caching.
    """
    def wrapper(*args):
        """Wrapper function to cache the output of the decorated function."""
        url = args[0]
        redis_client.incr(f"count:{url}")
        page_content = redis_client.get(f"text:{url}")
        if not page_content:
            page_content = f(url)
            redis_client.setex(f"text:{url}", 10, page_content)
        else:
            page_content = page_content.decode("utf-8")
        return page_content
    return wrapper


@cacher
def get_page(url: str) -> str:
    """Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)  # Send GET request
    print("NOT CACHED")
    return response.text  # Return response content


# Example usage
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk"
    print(get_page(test_url)[:100])  # Print first 100 characters of content
    print(f"Access count: {redis_client.get(
        f'count:{test_url}').decode('utf-8')}")
