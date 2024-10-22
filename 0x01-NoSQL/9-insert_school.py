#!/usr/bin/env python3

"""Module defines `insert_school` method"""


from typing import Any, Dict, Optional

def insert_school(mongo_collection, **kwargs: Dict) -> Optional[Any]:
    """Inserts school in collection

    Args:
        mongo_collection: The MongoDb collection
        kwargs: The document data

    Return:
        The assigned ID of the newly inserted document
    """
    return mongo_collection.insert_one(kwargs).inserted_id

