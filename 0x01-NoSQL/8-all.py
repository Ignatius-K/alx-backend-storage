#!/usr/bin/env python3

"""Module defines the `list_all` method"""


from typing import List


def list_all(mongo_collection) -> List:
    """Returns list of documents in collection"""
    return list(mongo_collection.find())
