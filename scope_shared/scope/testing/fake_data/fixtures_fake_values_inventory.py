import random
from typing import Callable, List

import faker
import pytest
import scope.database.format_utils
import scope.database.patient.patient_profile
import scope.schema
import scope.testing.fake_data.enums
import scope.testing.fake_data.fake_utils as fake_utils

OPTIONAL_KEYS = [
    "values",
]


def _fake_activity(
    *,
    faker_factory: faker.Faker,
    value_id: str,
    life_area_id: str,
) -> dict:
    """
    This is currently tested by inclusion in the values inventory schema.
    If moved out on its own, it should probably get its own tests.
    """

    return {
        # TODO: WHAT IS THIS ID, WHERE IS IT USED, DO WE NEED IT
        "id": "WHAT IS THIS ID, WHERE IS IT USED, DO WE NEED IT",
        "name": faker_factory.text(),
        # TODO: WHAT IS THIS ID, WHERE IS IT USED, DO WE NEED IT, IT SEEMS REDUNDANT FROM THE PARENT
        "valueId": value_id,
        "dateCreated": scope.database.format_utils.format_date(
            faker_factory.date_object()
        ),
        "dateEdited": scope.database.format_utils.format_date(
            faker_factory.date_object()
        ),
        # TODO: WHAT IS THIS ID, WHERE IS IT USED, DO WE NEED IT, IT SEEMS REDUNDANT FROM THE PARENT
        "lifeareaId": life_area_id,
        "enjoyment": random.randint(1, 5),
        "importance": random.randint(1, 5),
    }


def _fake_value(
    *,
    faker_factory: faker.Faker,
    fake_life_area: dict,  # lifeareaId will be sampled from this
) -> dict:
    """
    This is currently tested by inclusion in the values inventory schema.
    If moved out on its own, it should probably get its own tests.
    """

    value_id = "WHAT IS THIS ID, WHERE IS IT USED, DO WE NEED IT."

    return {
        # TODO: WHAT IS THIS ID, WHERE IS IT USED, DO WE NEED IT
        "id": value_id,
        "name": faker_factory.text(),
        "dateCreated": scope.database.format_utils.format_date(
            faker_factory.date_object()
        ),
        "dateEdited": scope.database.format_utils.format_date(
            faker_factory.date_object()
        ),
        "lifeareaId": fake_life_area["id"],
        "activities": [
            _fake_activity(
                faker_factory=faker_factory,
                value_id=value_id,
                life_area_id=fake_life_area["id"],
            )
            for count in range(1, 5)
        ],
    }


def fake_values_inventory_factory(
    *,
    faker_factory: faker.Faker,
    fake_life_areas: List[dict],
) -> Callable[[], dict]:
    """
    Obtain a factory that will generate fake value inventory documents.
    """

    # TODO: Ravi mentioned patient is asked to add at least 1 value and 1 activity for each life area. Confirm again.

    def factory() -> dict:
        fake_values_inventory = {
            "_type": "valuesInventory",
            "assigned": random.choice([True, False]),
            "assignedDate": scope.database.format_utils.format_date(
                faker_factory.date_object()
            ),
            "values": [
                _fake_value(
                    faker_factory=faker_factory,
                    fake_life_area=fake_life_area,
                )
                for fake_life_area in fake_life_areas
                for count in range(random.randint(1, 5))
            ],
        }

        # Remove a randomly sampled subset of optional parameters.
        fake_values_inventory = scope.testing.fake_data.fake_utils.fake_optional(
            document=fake_values_inventory,
            optional_keys=OPTIONAL_KEYS,
        )

        return fake_values_inventory

    return factory


@pytest.fixture(name="data_fake_values_inventory_factory")
def fixture_data_fake_values_inventory_factory(
    *,
    faker: faker.Faker,
    data_fake_life_areas: List[dict],
) -> Callable[[], dict]:
    """
    Fixture for data_fake_values_inventory_factory.
    """

    unvalidated_factory = fake_values_inventory_factory(
        faker_factory=faker,
        fake_life_areas=data_fake_life_areas,
    )

    def factory() -> dict:
        fake_values_inventory = unvalidated_factory()

        scope.testing.fake_data.fake_utils.xfail_for_invalid(
            schema=scope.schema.values_inventory_schema,
            document=fake_values_inventory,
        )

        return fake_values_inventory

    return factory
