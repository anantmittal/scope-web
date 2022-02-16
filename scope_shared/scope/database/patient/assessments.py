from typing import List, Optional

import pymongo.collection
import scope.database.collection_utils

DOCUMENT_TYPE = "assessment"
DOCUMENT_ID = "assessmentId"


def get_assessments(
    *,
    collection: pymongo.collection.Collection,
) -> Optional[List[dict]]:
    """
    Retrieve list of "assessment" document.
    """

    return scope.database.collection_utils.get_set(
        collection=collection,
        document_type=DOCUMENT_TYPE,
    )


def get_assessment(
    *,
    collection: pymongo.collection.Collection,
    set_id: str,
) -> Optional[dict]:
    """
    Retrieve "assessment" document.
    """

    return scope.database.collection_utils.get_set_element(
        collection=collection,
        document_type=DOCUMENT_TYPE,
        set_id=set_id,
    )


def post_assessment(
    *,
    collection: pymongo.collection.Collection,
    case_review: dict,
) -> scope.database.collection_utils.PutResult:
    """
    Create the "assessment" document.
    """

    return scope.database.collection_utils.put_set_element(
        collection=collection,
        document_type=DOCUMENT_TYPE,
        set_id=case_review[DOCUMENT_ID],
        document=case_review,
    )


def put_assessment(
    *,
    collection: pymongo.collection.Collection,
    case_review: dict,
):
    """
    Update the "assessment" document.
    """
    # NOTE: Exactly same as post_assessment, but keeping it here if we need additional computation.

    return scope.database.collection_utils.put_set_element(
        collection=collection,
        document_type=DOCUMENT_TYPE,
        set_id=case_review[DOCUMENT_ID],
        document=case_review,
    )
