import faker
import pymongo.collection
import pymongo.database
import scope.database.patient.case_reviews
import scope.database.patient.clinical_history
import scope.database.patient.patient_profile
import scope.database.patient.safety_plan
import scope.database.patient.sessions
import scope.database.patient.values_inventory
import scope.database.patients
import scope.testing.fake_data.fixtures_fake_case_review
import scope.testing.fake_data.fixtures_fake_case_reviews
import scope.testing.fake_data.fixtures_fake_clinical_history
import scope.testing.fake_data.fixtures_fake_contact
import scope.testing.fake_data.fixtures_fake_life_areas
import scope.testing.fake_data.fixtures_fake_patient_profile
import scope.testing.fake_data.fixtures_fake_referral_status
import scope.testing.fake_data.fixtures_fake_safety_plan
import scope.testing.fake_data.fixtures_fake_session
import scope.testing.fake_data.fixtures_fake_sessions
import scope.testing.fake_data.fixtures_fake_values_inventory


def populate_database(
    *,
    database: pymongo.database.Database,
    populate_patients: int,
):
    faker_factory = faker.Faker(locale="la")

    # NOTE: Jina needs a persistent patient_id to test web_patient API endpoints.
    patient_persistent = scope.database.patients.create_persistent_patient(
        database=database, patient_id="persistent"
    )
    patient_collection = database.get_collection(patient_persistent["collection"])
    # Populate persistent patient.
    _populate_patient(
        faker_factory=faker_factory,
        patient_collection=patient_collection,
    )

    for patient_count in range(populate_patients):
        patient_current = scope.database.patients.create_patient(database=database)
        patient_collection = database.get_collection(patient_current["collection"])

        _populate_patient(
            faker_factory=faker_factory,
            patient_collection=patient_collection,
        )


def _populate_patient(
    *,
    faker_factory: faker.Faker,
    patient_collection: pymongo.collection.Collection,
):
    # Obtain factories used by other factories
    fake_contact_factory = (
        scope.testing.fake_data.fixtures_fake_contact.fake_contact_factory(
            faker_factory=faker_factory,
        )
    )
    fake_life_areas_factory = (
        scope.testing.fake_data.fixtures_fake_life_areas.fake_life_areas_factory()
    )

    # Obtain fixed documents
    fake_life_areas = fake_life_areas_factory()

    # Obtain necessary document factories
    fake_patient_profile_factory = scope.testing.fake_data.fixtures_fake_patient_profile.fake_patient_profile_factory(
        faker_factory=faker_factory,
    )
    fake_clinical_history_factory = scope.testing.fake_data.fixtures_fake_clinical_history.fake_clinical_history_factory(
        faker_factory=faker_factory,
    )
    fake_values_inventory_factory = scope.testing.fake_data.fixtures_fake_values_inventory.fake_values_inventory_factory(
        faker_factory=faker_factory,
        fake_life_areas=fake_life_areas,
    )
    fake_safety_plan_factory = (
        scope.testing.fake_data.fixtures_fake_safety_plan.fake_safety_plan_factory(
            faker_factory=faker_factory,
            fake_contact_factory=fake_contact_factory,
        )
    )
    fake_sessions_factory = scope.testing.fake_data.fixtures_fake_sessions.fake_sessions_factory(
        fake_session_factory=scope.testing.fake_data.fixtures_fake_session.fake_session_factory(
            faker_factory=faker_factory,
            fake_referral_status_factory=scope.testing.fake_data.fixtures_fake_referral_status.fake_referral_status_factory(
                faker_factory=faker_factory,
            ),
        ),
    )
    fake_case_reviews_factory = scope.testing.fake_data.fixtures_fake_case_reviews.fake_case_reviews_factory(
        fake_case_review_factory=scope.testing.fake_data.fixtures_fake_case_review.fake_case_review_factory(
            faker_factory=faker_factory,
        ),
    )

    # Put appropriate documents
    scope.database.patient.patient_profile.put_patient_profile(
        collection=patient_collection,
        patient_profile=fake_patient_profile_factory(),
    )
    scope.database.patient.clinical_history.put_clinical_history(
        collection=patient_collection,
        clinical_history=fake_clinical_history_factory(),
    )
    scope.database.patient.values_inventory.put_values_inventory(
        collection=patient_collection,
        values_inventory=fake_values_inventory_factory(),
    )
    scope.database.patient.safety_plan.put_safety_plan(
        collection=patient_collection,
        safety_plan=fake_safety_plan_factory(),
    )
    for session in fake_sessions_factory():
        scope.database.patient.sessions.post_session(
            collection=patient_collection,
            session=session,
        )
    for case_review in fake_case_reviews_factory():
        scope.database.patient.case_reviews.post_case_review(
            collection=patient_collection,
            case_review=case_review,
        )
