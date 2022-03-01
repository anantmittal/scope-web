from dataclasses import dataclass
import datetime
import jschon
import requests
from typing import Callable, List
from urllib.parse import urljoin

import blueprints.patient.summary
import scope.config
import scope.database.date_utils as date_utils
import scope.database.patient.safety_plan
import scope.database.patient.scheduled_assessments
import scope.database.patient.values_inventory
from scope.schema import patient_summary_schema
import scope.testing.fixtures_database_temp_patient


import tests.testing_config

TESTING_CONFIGS = tests.testing_config.ALL_CONFIGS

QUERY = "patient/{patient_id}/summary"


def _patient_summary_assertions(summary: dict) -> None:
    # Remove "status" for schema validation
    if "status" in summary:
        del summary["status"]

    schema_result = patient_summary_schema.evaluate(jschon.JSON(summary))
    assert schema_result.valid

    assigned_scheduled_assessments = summary["assignedScheduledAssessments"]
    for assigned_scheduled_assessment_current in assigned_scheduled_assessments:
        assert assigned_scheduled_assessment_current["completed"] == False
        assert (
            date_utils.parse_date(assigned_scheduled_assessment_current["dueDate"])
            <= datetime.datetime.today()
        )


def test_patient_summary_get(
    database_temp_patient_factory: Callable[
        [],
        scope.testing.fixtures_database_temp_patient.DatabaseTempPatient,
    ],
    data_fake_safety_plan_factory: Callable[[], dict],
    data_fake_values_inventory_factory: Callable[[], dict],
    data_fake_scheduled_assessments_factory: Callable[[], List[dict]],
    flask_client_config: scope.config.FlaskClientConfig,
    flask_session_unauthenticated_factory: Callable[[], requests.Session],
):

    temp_patient = database_temp_patient_factory()

    # Insert values inventory, safety plan, and scheduled assessments
    values_inventory = data_fake_values_inventory_factory()
    scope.database.patient.values_inventory.put_values_inventory(
        collection=temp_patient.collection,
        values_inventory=values_inventory,
    )
    safety_plan = data_fake_safety_plan_factory()
    scope.database.patient.safety_plan.put_safety_plan(
        collection=temp_patient.collection,
        safety_plan=safety_plan,
    )
    scheduled_assessments = data_fake_scheduled_assessments_factory()
    for scheduled_assessment_current in scheduled_assessments:
        scope.database.patient.scheduled_assessments.post_scheduled_assessment(
            collection=temp_patient.collection,
            scheduled_assessment=scheduled_assessment_current,
        )

    # Obtain a session
    session = flask_session_unauthenticated_factory()
    query = QUERY.format(patient_id=temp_patient.patient_id)
    response = session.get(
        url=urljoin(
            flask_client_config.baseurl,
            query,
        ),
    )

    assert response.ok

    summary = response.json()
    _patient_summary_assertions(summary=summary)


def test_compute_patient_summary_values_inventory(
    data_fake_safety_plan_factory: Callable[[], dict],
    data_fake_values_inventory_factory: Callable[[], dict],
    data_fake_scheduled_assessments_factory: Callable[[], List[dict]],
):
    # Create values inventory, safety plan, and scheduled assessments
    values_inventory = data_fake_values_inventory_factory()
    safety_plan = data_fake_safety_plan_factory()
    scheduled_assessments = data_fake_scheduled_assessments_factory()

    patient = {
        "valuesInventory": values_inventory,
        "safetyPlan": safety_plan,
        "scheduledAssessments": scheduled_assessments,
    }

    # OPTION 1 - assigned is False.
    values_inventory["assigned"] = False
    patient["valuesInventory"] = values_inventory
    summary = blueprints.patient.summary.compute_patient_summary(patient=patient)
    assert summary["assignedValuesInventory"] == False
    _patient_summary_assertions(summary=summary)

    # OPTION 2 - assigned is True and acivity exists in values
    values_inventory = data_fake_values_inventory_factory()
    while not len(values_inventory.get("values", [])) > 0:
        values_inventory = data_fake_values_inventory_factory()
    values_inventory["assigned"] = True
    patient["valuesInventory"] = values_inventory
    summary = blueprints.patient.summary.compute_patient_summary(patient=patient)
    assert summary["assignedValuesInventory"] == False
    _patient_summary_assertions(summary=summary)

    # OPTION 3 - assigned is True and no acivity exists in values
    values_inventory = data_fake_values_inventory_factory()
    while not len(values_inventory.get("values", [])) == 0:
        values_inventory = data_fake_values_inventory_factory()
    values_inventory["assigned"] = True
    patient["valuesInventory"] = values_inventory
    summary = blueprints.patient.summary.compute_patient_summary(patient=patient)
    assert summary["assignedValuesInventory"] == True
    _patient_summary_assertions(summary=summary)


def test_compute_patient_summary_safety_plan(
    data_fake_safety_plan_factory: Callable[[], dict],
    data_fake_values_inventory_factory: Callable[[], dict],
    data_fake_scheduled_assessments_factory: Callable[[], List[dict]],
):

    # Create values inventory, safety plan, and scheduled assessments
    values_inventory = data_fake_values_inventory_factory()
    safety_plan = data_fake_safety_plan_factory()
    scheduled_assessments = data_fake_scheduled_assessments_factory()

    patient = {
        "valuesInventory": values_inventory,
        "safetyPlan": safety_plan,
        "scheduledAssessments": scheduled_assessments,
    }

    # OPTION 1 - assigned is False.
    safety_plan["assigned"] = False
    patient["safetyPlan"] = safety_plan
    summary = blueprints.patient.summary.compute_patient_summary(patient=patient)
    assert summary["assignedSafetyPlan"] == False
    _patient_summary_assertions(summary=summary)

    # OPTION 2 - assigned is True but lastUpdatedDate = assignedDate
    safety_plan["assigned"] = True
    safety_plan["lastUpdatedDate"] = safety_plan["assignedDate"]
    patient["safetyPlan"] = safety_plan
    summary = blueprints.patient.summary.compute_patient_summary(patient=patient)
    assert summary["assignedSafetyPlan"] == False
    _patient_summary_assertions(summary=summary)

    # OPTION 3 - assigned is True but lastUpdatedDate > assignedDate
    safety_plan["lastUpdatedDate"] = date_utils.format_date(
        date_utils.parse_date(safety_plan["assignedDate"]) + datetime.timedelta(days=2)
    )
    patient["safetyPlan"] = safety_plan
    summary = blueprints.patient.summary.compute_patient_summary(patient=patient)
    assert summary["assignedSafetyPlan"] == False
    _patient_summary_assertions(summary=summary)

    # OPTION 4 - assigned is True and lastUpdatedDate < assignedDate
    safety_plan["lastUpdatedDate"] = date_utils.format_date(
        date_utils.parse_date(safety_plan["assignedDate"]) - datetime.timedelta(days=2)
    )
    patient["safetyPlan"] = safety_plan
    summary = blueprints.patient.summary.compute_patient_summary(patient=patient)
    assert summary["assignedSafetyPlan"] == True
    _patient_summary_assertions(summary=summary)


def test_compute_patient_summary_scheduled_assessments(
    data_fake_safety_plan_factory: Callable[[], dict],
    data_fake_values_inventory_factory: Callable[[], dict],
    data_fake_scheduled_assessments_factory: Callable[[], List[dict]],
):
    # Create values inventory, safety plan, and scheduled assessments
    values_inventory = data_fake_values_inventory_factory()
    safety_plan = data_fake_safety_plan_factory()
    scheduled_assessments = data_fake_scheduled_assessments_factory()

    patient = {
        "valuesInventory": values_inventory,
        "safetyPlan": safety_plan,
        "scheduledAssessments": scheduled_assessments,
    }

    # OPTION 1 - completed is True.
    for scheduled_assessment_current in scheduled_assessments:
        scheduled_assessment_current["completed"] = True
    patient["scheduledAssessments"] = scheduled_assessments
    summary = blueprints.patient.summary.compute_patient_summary(patient=patient)
    assert summary["assignedScheduledAssessments"] == []
    _patient_summary_assertions(summary=summary)

    # OPTION 2 - completed is False but dueDate > today.
    for scheduled_assessment_current in scheduled_assessments:
        scheduled_assessment_current["completed"] = False
        scheduled_assessment_current["dueDate"] = date_utils.format_date(
            datetime.datetime.today() + datetime.timedelta(days=2)
        )
    patient["scheduledAssessments"] = scheduled_assessments
    summary = blueprints.patient.summary.compute_patient_summary(patient=patient)
    assert summary["assignedScheduledAssessments"] == []
    _patient_summary_assertions(summary=summary)

    # OPTION 3 - completed is False and dueDate = today.
    for scheduled_assessment_current in scheduled_assessments:
        scheduled_assessment_current["completed"] = False
        scheduled_assessment_current["dueDate"] = date_utils.format_date(
            datetime.datetime.today()
        )
    patient["scheduledAssessments"] = scheduled_assessments
    summary = blueprints.patient.summary.compute_patient_summary(patient=patient)
    assert summary["assignedScheduledAssessments"] != []
    _patient_summary_assertions(summary=summary)

    # OPTION 4 - completed is False and dueDate < today.
    for scheduled_assessment_current in scheduled_assessments:
        scheduled_assessment_current["completed"] = False
        scheduled_assessment_current["dueDate"] = date_utils.format_date(
            datetime.datetime.today() - datetime.timedelta(days=1)
        )
    patient["scheduledAssessments"] = scheduled_assessments
    summary = blueprints.patient.summary.compute_patient_summary(patient=patient)
    assert summary["assignedScheduledAssessments"] != []
    _patient_summary_assertions(summary=summary)
