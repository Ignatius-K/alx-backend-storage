#!/usr/bin/env python3

"""Update topics based on `school` name"""


from typing import Sequence


def update_topics(mongo_collection, name: str, topics: Sequence) -> None:
    """Update topics on documents

    The documents to be updated are to be
    of a given school

    Args:
        mongo_collection: The MongoDB collection
        name: The school name

    Return: (void)
    """

    mongo_collection.update_many(
        {"name": name},
        {"$set": {
            "topics": topics
        }}
    )
