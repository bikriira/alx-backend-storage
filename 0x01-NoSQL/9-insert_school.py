def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document into the specified MongoDB collection.

    Args:
        mongo_collection: The pymongo collection object where the document will be inserted.
        **kwargs: Arbitrary keyword arguments representing the document to be inserted.

    Returns:
        ObjectId: The _id of the newly inserted document.
    """
    document_id = mongo_collection.insert_one(kwargs).inserted_id
    return document_id