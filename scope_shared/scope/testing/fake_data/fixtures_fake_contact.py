"""
Contacts are not stored documents.

They are generated and stored as elements of other documents.
"""

import random
from typing import Callable

import faker
import pytest
import scope.schema
import scope.testing.fake_data.enums
import scope.testing.fake_data.fake_utils as fake_utils

OPTIONAL_KEYS = [
    "address",
    "phoneNumber",
    "emergencyNumber",
]


def fake_contact_factory(
    *,
    faker_factory: faker.Faker,
) -> Callable[[], dict]:
    """
    Obtain a factory that will generate fake contact documents.
    """

    def factory() -> dict:
        fake_contact = {
            "contactType": fake_utils.fake_enum_value(
                scope.testing.fake_data.enums.ContactType
            ),
            "name": faker_factory.name(),
            "address": faker_factory.address(),
            "phoneNumber": faker_factory.phone_number(),
            "emergencyNumber": faker_factory.phone_number(),
        }

        # Remove a randomly sampled subset of optional parameters.
        fake_contact = scope.testing.fake_data.fake_utils.fake_optional(
            document=fake_contact,
            optional_keys=OPTIONAL_KEYS,
        )

        return fake_contact

    return factory


@pytest.fixture(name="data_fake_contact_factory")
def fixture_data_fake_contact_factory(
    faker: faker.Faker,
) -> Callable[[], dict]:
    """
    Fixture for data_fake_contact_factory.
    """
    unvalidated_factory = fake_contact_factory(
        faker_factory=faker,
    )

    def factory() -> dict:
        fake_contact = unvalidated_factory()

        scope.testing.fake_data.fake_utils.xfail_for_invalid(
            schema=scope.schema.contact_schema,
            document=fake_contact,
        )

        return fake_contact

    return factory
