#!/usr/bin/env python3

"""Script provides stats of Nginx logs in MongoDB"""


from typing import Union
from pymongo import MongoClient # type: ignore


def create_connection(host: str = "127.0.0.1", port: Union[int, str] = 27017):
    """Returns connection to nginx database"""
    db = MongoClient(host=host, port=port)
    return db.logs


def print_log_stats(session, collection_name: str = "nginx") -> None:
    """Print the logs stats

    Args:
        session: The database session
        collection_name: The name of the collection
    """

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    logs = session[collection_name]

    print(f"{logs.count_documents({})} logs\nMethods:")
    for method in methods:
        print(f"\tmethod {method}: " +
              f"{logs.count_documents({'method': method})}"
              )
    print(f"{logs.count_documents({'method': 'GET', 'path': '/status'})} " +
          f"status check"
          )


if __name__ == '__main__':
    session = create_connection()
    if not session:
        exit(code=1)
    print_log_stats(session)
