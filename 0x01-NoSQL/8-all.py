#!/usr/bin/env python3
"""A script to retrieve all documents in a collection"""
from pymongo import MongoClient


def list_all(mongo_collection):
    """
    Retrieves all documents from a specified MongoDB collection.

    Args:
        mongo_collection: The MongoDB collection from which to retrieve documents.

    Returns:
        A cursor that iterates over the documents in the collection.
    """

    return mongo_collection.find()
