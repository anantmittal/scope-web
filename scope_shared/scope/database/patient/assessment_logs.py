from typing import List, Optional

import pymongo.collection
import scope.database.collection_utils

DOCUMENT_TYPE = "assessmentLog"
SEMANTIC_SET_ID = "assessmentLogId"


def get_assessment_logs(
    *,
    collection: pymongo.collection.Collection,
) -> Optional[List[dict]]:
    """
    Get list of "assessmentLog" documents.
    """

    return scope.database.collection_utils.get_set(
        collection=collection,
        document_type=DOCUMENT_TYPE,
    )


def get_assessment_log(
    *,
    collection: pymongo.collection.Collection,
    set_id: str,
) -> Optional[dict]:
    """
    Get "assessmentLog" document.
    """

    return scope.database.collection_utils.get_set_element(
        collection=collection,
        document_type=DOCUMENT_TYPE,
        set_id=set_id,
    )


def post_assessment_log(
    *,
    collection: pymongo.collection.Collection,
    assessment_log: dict,
) -> scope.database.collection_utils.SetPostResult:
    """
    Post "assessmentLog" document.
    """

    return scope.database.collection_utils.post_set_element(
        collection=collection,
        document_type=DOCUMENT_TYPE,
        semantic_set_id=SEMANTIC_SET_ID,
        document=assessment_log,
    )


def put_assessment_log(
    *,
    collection: pymongo.collection.Collection,
    assessment_log: dict,
    set_id: str,
) -> scope.database.collection_utils.SetPutResult:
    """
    Put "assessmentLog" document.
    """

    return scope.database.collection_utils.put_set_element(
        collection=collection,
        document_type=DOCUMENT_TYPE,
        semantic_set_id=SEMANTIC_SET_ID,
        set_id=set_id,
        document=assessment_log,
    )
