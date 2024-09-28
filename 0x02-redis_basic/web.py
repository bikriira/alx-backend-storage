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
# ~~~~~ TO SEE DIFERENCE IN EXECUTION TIME UNCOMMENT all ~~~~~#
# from functools import wraps
# import time
from typing import Callable
import requests
import redis

re = redis.Redis()


# def timer_decorator(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         exec_time = end_time - start_time
#         print(f"Execution time of {func.__name__}: {exec_time:.4f} seconds")
#         return result
#     return wrapper


def cacher(f: Callable) -> Callable:
    """Decorator that caches the result of a function.

    Args:
        f: The function to be cached.

    Returns:
        A wrapper function that implements caching.
    """
    def wrapper(*args):
        url = args[0]
        re.incr(f"count:{url}")
        page_content = re.get(f"text:{url}")
        if not page_content:
            page_content = f(url)
            re.setex(f"text:{url}", 10, page_content)
        return page_content
    return wrapper


# @timer_decorator
@cacher
def get_page(url: str) -> str:
    """Fetches the HTML content of a given URL.

    Args:
        url: The URL to fetch content from.

    Returns:
        The HTML content of the URL as a string.
    """
    response = requests.get(url)
    return response.text


# Example usage
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk"
    print(get_page(test_url)[:100])  # Print first 100 characters
    print(f"Access count: {re.get(f'count:{test_url}').decode('utf-8')}")
