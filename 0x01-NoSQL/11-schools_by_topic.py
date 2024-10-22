#!/usr/bin/env python3

"""Module defines `schools_by_topic` method"""


from typing import Sequence


def schools_by_topic(mongo_collection, topic: str) -> Sequence:
    """Get schools having certain topic

    Args:
        mongo_collection (pymongo.collection.Collection):
            The MongoDB collection
        topic: The topic to filter schools with

    Return:
        The schools with given topic
    """

    return list(mongo_collection.find({"topics": topic}))
