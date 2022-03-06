import copy
import pprint

import pymongo.database
from typing import List

import scope.config
import scope.populate.populate_account
import scope.populate.populate_fake
import scope.populate.populate_patient
import scope.populate.populate_provider


def populate_from_config(
    *,
    database: pymongo.database.Database,
    cognito_config: scope.config.CognitoClientConfig,
    populate_config: dict,
) -> dict:
    """
    Populate from a provided config.

    Return a new state of the populate config.
    """
    populate_config = copy.deepcopy(populate_config)

    #
    # Create any fake patients and providers
    #
    populate_config = scope.populate.populate_fake.populate_fake_from_config(
        database=database,
        populate_config=populate_config,
    )

    #
    # Create specified patients
    #
    created_patients = _create_patients(
        database=database,
        create_patients=populate_config["patients"]["create"],
    )
    populate_config["patients"]["create"] = []
    populate_config["patients"]["existing"].extend(created_patients)

    #
    # Populate patient accounts
    #
    for patient_current in populate_config["patients"]["existing"]:
        if "account" in patient_current:
            patient_current["account"] = scope.populate.populate_account.populate_account_from_config(
                database=database,
                cognito_config=cognito_config,
                populate_config_account=patient_current["account"]
            )

    #
    # Create specified providers
    #
    created_providers = _create_providers(
        database=database,
        create_providers=populate_config["providers"]["create"],
    )
    populate_config["providers"]["create"] = []
    populate_config["providers"]["existing"].extend(created_providers)

    #
    # Populate provider accounts
    #
    for provider_current in populate_config["providers"]["existing"]:
        if "account" in provider_current:
            provider_current["account"] = scope.populate.populate_account.populate_account_from_config(
                database=database,
                cognito_config=cognito_config,
                populate_config_account=provider_current["account"]
            )

    return populate_config


def _create_patients(
    *,
    database: pymongo.database.Database,
    create_patients: List[dict],
) -> List[dict]:
    result: List[dict] = []
    for create_patient_current in create_patients:
        created_patient = scope.populate.populate_patient.create_patient(
            database=database,
            name=create_patient_current["name"],
            mrn=create_patient_current["MRN"],
            create_patient=create_patient_current,
        )

        result.append(created_patient)

    return result


def _create_providers(
    *,
    database: pymongo.database.Database,
    create_providers: List[dict],
) -> List[dict]:
    result: List[dict] = []
    for create_provider_current in create_providers:
        created_provider = scope.populate.populate_provider.create_provider(
            database=database,
            name=create_provider_current["name"],
            role=create_provider_current["role"],
            create_provider=create_provider_current,
        )

        result.append(created_provider)

    return result
