import random
from pprint import pprint
from typing import Callable

import faker
import pytest
import scope.database.format_utils
import scope.database.patient.assessments
import scope.schema
import scope.testing.fake_data.enums
import scope.testing.fake_data.fake_utils as fake_utils


def fake_assessment_factory(
    *,
    faker_factory: faker.Faker,
    assessment_type: scope.testing.fake_data.enums.AssessmentType,
) -> Callable[[], dict]:
    """
    Obtain a factory that will generate fake assessment documents.
    """

    def factory() -> dict:

        fake_assessment = {
            "_type": scope.database.patient.assessments.DOCUMENT_TYPE,
            "assessmentId": fake_utils.fake_unique_id(),
            "assessmentName": assessment_type.value,
            "assigned": random.choice([True, False]),
            "assignedDate": scope.database.format_utils.format_date(
                faker_factory.date_object()
            ),
            "frequency": fake_utils.fake_enum_value(
                scope.testing.fake_data.enums.AssessmentFrequency
            ),
            "dayOfWeek": fake_utils.fake_enum_value(
                scope.testing.fake_data.enums.DayOfWeek
            ),
        }

        return fake_assessment

    return factory


@pytest.fixture(name="data_fake_assessment_factory")
def fixture_data_fake_assessment_factory(
    faker: faker.Faker,
    assessment_type: scope.testing.fake_data.enums.AssessmentType,
) -> Callable[[], dict]:
    """
    Fixture for data_fake_assessment_factory.
    """

    unvalidated_factory = fake_assessment_factory(
        faker_factory=faker,
        assessment_type=assessment_type,
    )

    def factory() -> dict:
        fake_assessment = unvalidated_factory()

        fake_utils.xfail_for_invalid(
            schema=scope.schema.assessment_schema,
            document=fake_assessment,
        )

        return fake_assessment

    return factory
