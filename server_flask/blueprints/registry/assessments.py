import flask
import flask_json
import pymongo.errors

import request_context
import request_utils
import scope.database
import scope.database.patient.assessments
import scope.schema

assessments_blueprint = flask.Blueprint(
    "assessments_blueprint",
    __name__,
)


@assessments_blueprint.route(
    "/<string:patient_id>/assessments",
    methods=["GET"],
)
@flask_json.as_json
def get_assessments(patient_id):
    context = request_context.authorized_for_patient(patient_id=patient_id)
    patient_collection = context.patient_collection(patient_id=patient_id)

    documents = scope.database.patient.assessments.get_assessments(
        collection=patient_collection,
    )

    # Validate and normalize the response
    documents = request_utils.set_get_response_validate(
        documents=documents,
    )

    return {
        "assessments": documents,
    }


@assessments_blueprint.route(
    "/<string:patient_id>/assessment/<string:assessment_id>",
    methods=["GET"],
)
@flask_json.as_json
def get_assessment(patient_id, assessment_id):
    context = request_context.authorized_for_patient(patient_id=patient_id)
    patient_collection = context.patient_collection(patient_id=patient_id)

    # Get the document
    document = scope.database.patient.assessments.get_assessment(
        collection=patient_collection,
        set_id=assessment_id,
    )

    # Validate and normalize the response
    document = request_utils.singleton_get_response_validate(
        document=document,
    )

    return {
        "assessment": document,
    }


@assessments_blueprint.route(
    "/<string:patient_id>/assessment/<string:assessment_id>",
    methods=["PUT"],
)
@request_utils.validate_schema(
    schema=scope.schema.assessment_schema,
    key="assessment",
)
@flask_json.as_json
def put_assessment(patient_id, assessment_id):
    context = request_context.authorized_for_patient(patient_id=patient_id)
    patient_collection = context.patient_collection(patient_id=patient_id)

    # Obtain the document being put
    document = flask.request.json["assessment"]

    # Validate and normalize the request
    document = request_utils.set_element_put_request_validate(
        semantic_set_id=scope.database.patient.assessments.SEMANTIC_SET_ID,
        document=document,
        set_id=assessment_id,
    )

    # Store the document
    try:
        result = scope.database.patient.assessments.put_assessment(
            collection=patient_collection,
            assessment=document,
            set_id=assessment_id,
        )
    except pymongo.errors.DuplicateKeyError:
        # Indicates a revision race condition, return error with current revision
        document_conflict = scope.database.patient.assessments.get_assessment(
            collection=patient_collection, set_id=assessment_id
        )
        # Validate and normalize the response
        document_conflict = request_utils.singleton_put_response_validate(
            document=document_conflict
        )

        request_utils.abort_revision_conflict(
            document={
                "assessment": document_conflict,
            }
        )
    else:
        # Validate and normalize the response
        document_response = request_utils.singleton_put_response_validate(
            document=result.document,
        )

        return {
            "assessment": document_response,
        }
