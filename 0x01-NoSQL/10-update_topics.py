#!/usr/bin/env python3


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name.

    Args:
        mongo_collection: The pymongo collection object to update.
        name: school name to update.
        topics: the update to be reflected on the macthing school.
    """

    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
