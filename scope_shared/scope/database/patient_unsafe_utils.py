import copy
import pymongo.collection
from typing import Callable, Optional

import scope.database.collection_utils
import scope.database.patient


def _unsafe_update_singleton(
    *,
    database_get_function: Callable[[...], Optional[dict]],
    database_put_function: Callable[[...], scope.database.collection_utils.PutResult],
    database_put_document_parameter: str,
    collection: pymongo.collection.Collection,
    new_document: dict,
) -> scope.database.collection_utils.PutResult:
    """
    Update a singleton.

    Unsafe because it gets and updates the current document,
    effectively ignoring use of _rev to prevent race conflicts in modifications.
    """

    current_document = database_get_function(
        **{
            "collection": collection,
        }
    )

    if current_document:
        updated_document = copy.deepcopy(current_document)
        updated_document.update(copy.deepcopy(new_document))
        del updated_document["_id"]
    else:
        updated_document = new_document

    return database_put_function(
        **{
            "collection": collection,
            database_put_document_parameter: updated_document,
        }
    )


def unsafe_update_assessment(
    *,
    collection: pymongo.collection.Collection,
    set_id: str,
    assessment: dict,
) -> scope.database.collection_utils.SetPutResult:
    """
    Update an assessment document.

    Unsafe because it gets and updates the current document,
    effectively ignoring use of _rev to prevent race conflicts in modifications.
    """

    new_document = assessment
    current_document = scope.database.patient.get_assessment(
        collection=collection,
        set_id=set_id,
    )

    if current_document:
        updated_document = copy.deepcopy(current_document)
        updated_document.update(copy.deepcopy(new_document))
        del updated_document["_id"]
    else:
        updated_document = new_document

    return scope.database.patient.put_assessment(
        collection=collection,
        set_id=set_id,
        assessment=updated_document,
    )


def unsafe_update_clinical_history(
    *,
    collection: pymongo.collection.Collection,
    clinical_history: dict,
) -> scope.database.collection_utils.PutResult:
    return _unsafe_update_singleton(
        database_get_function=scope.database.patient.get_clinical_history,
        database_put_function=scope.database.patient.put_clinical_history,
        database_put_document_parameter="clinical_history",
        collection=collection,
        new_document=clinical_history,
    )


def unsafe_update_patient_profile(
    *,
    collection: pymongo.collection.Collection,
    patient_profile: dict,
) -> scope.database.collection_utils.PutResult:
    return _unsafe_update_singleton(
        database_get_function=scope.database.patient.get_patient_profile,
        database_put_function=scope.database.patient.put_patient_profile,
        database_put_document_parameter="patient_profile",
        collection=collection,
        new_document=patient_profile,
    )


def unsafe_update_safety_plan(
    *,
    collection: pymongo.collection.Collection,
    safety_plan: dict,
) -> scope.database.collection_utils.PutResult:
    return _unsafe_update_singleton(
        database_get_function=scope.database.patient.get_safety_plan,
        database_put_function=scope.database.patient.put_safety_plan,
        database_put_document_parameter="safety_plan",
        collection=collection,
        new_document=safety_plan,
    )


def unsafe_update_values_inventory(
    *,
    collection: pymongo.collection.Collection,
    values_inventory: dict,
) -> scope.database.collection_utils.PutResult:
    return _unsafe_update_singleton(
        database_get_function=scope.database.patient.get_values_inventory,
        database_put_function=scope.database.patient.put_values_inventory,
        database_put_document_parameter="values_inventory",
        collection=collection,
        new_document=values_inventory,
    )
