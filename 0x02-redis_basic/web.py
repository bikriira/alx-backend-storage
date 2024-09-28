#!/usr/bin/env python3
"""
This module provides a simple caching system using Redis for
storing and retrieving HTML content of web pages.
"""
import requests
import redis
from typing import Callable
from functools import wraps
from datetime import timedelta
# ~~~~~ TO SEE DIFFERENCE IN EXECUTION TIME UNCOMMENT all ~~~~~#
# import time


# def timer_decorator(func):
#     """Decorator to measure the execution time of a function."""
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         exec_time = end_time - start_time
#         print(f"Execution time of {func.__name__}: {exec_time:.4f} seconds")
#         return result
#     return wrapper


redis_client = redis.Redis()


def cacher(f: Callable) -> Callable:
    """Decorator that caches the result of a function.

    Args:
        f (Callable): The function to be cached.

    Returns:
        Callable: A wrapper function that implements caching.
    """
    @wraps(f)
    def wrapper(*args: list) -> str:
        """Wrapper function to cache the output of the decorated function."""
        url = args[0]
        redis_client.incr(f"count:{url}")
        page_content = redis_client.get(f"text:{url}")
        if not page_content:
            page_content = f(url)
            redis_client.setex(f"text:{url}", timedelta(seconds=10), page_content)
        else:
            page_content = str(page_content)
        return page_content
    return wrapper


# @timer_decorator
@cacher
def get_page(url: str) -> str:
    """Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)  # Send GET request
    return response.text  # Return response content


if __name__ == "__main__":
    get_page("http://slowwly.robertomurray.co.uk")
