#!/usr/bin/env python3

"""Module defines the `top_students` method"""


from typing import Sequence


def top_students(mongo_collection) -> Sequence:
    """Gets top students by average score

    Args:
        mongo_collection: The MongoDB collection

    Returns:
        A list of top students
    """
    add_average_score_field_stage = {
        '$addFields': {
            'averageScore': {'$avg': '$topics.score'}
        }
    }
    sort_stage = {
        'averageScore': -1
    }
    aggregator_pipeline = [
        add_average_score_field_stage,
        sort_stage
    ]
    return list(mongo_collection.aggregate(aggregator_pipeline))
