import os
from urllib.parse import urljoin

from flask import Blueprint, Flask, request
from flask_cors import CORS
from flask_json import FlaskJSON, as_json
from markupsafe import escape

import blueprints.app.config
import database
from blueprints.patient.safety_plan import patient_safety_plan_blueprint

# Import patient & registry blueprints.
from blueprints.patient.values_inventory import patient_values_inventory_blueprint
from blueprints.registry.assessment_logs import registry_assessment_logs_blueprint
from blueprints.registry.case_reviews import registry_case_reviews_blueprint
from blueprints.registry.clinical_history import registry_clinical_history_blueprint
from blueprints.registry.patient_profile import registry_patient_profile_blueprint
from blueprints.registry.patients import registry_patients_blueprint
from blueprints.registry.safety_plan import registry_safety_plan_blueprint
from blueprints.registry.sessions import registry_sessions_blueprint
from blueprints.registry.values_inventory import registry_values_inventory_blueprint
from fake import getFakePatient, getRandomFakePatients
from utils import parseInt


def create_app():
    app = Flask(__name__)

    # Apply our configuration
    flask_environment = os.getenv("FLASK_ENV")
    if flask_environment == "production":
        from config.prod import ProductionConfig

        app.config.from_object(ProductionConfig())
    elif flask_environment == "development":
        from config.dev import DevelopmentConfig

        app.config.from_object(DevelopmentConfig())
    else:
        raise ValueError

    # Although ingress could provide CORS in production,
    # our development configuration also generates CORS requests.
    # Simple CORS wrapper of the application allows any and all requests.
    CORS().init_app(app=app)

    # Improved support for JSON in endpoints.
    FlaskJSON().init_app(app=app)

    # Database connection
    database.Database().init_app(app=app)

    # Temporary store for patients
    patients = getRandomFakePatients()
    patient_map = {p["identity"]["identityId"]: p for p in patients}

    # API TODO:
    # - check method
    # - check parameters
    # - return appropriate error message and code

    @app.route("/auth")
    @as_json
    def auth():
        return {"name": "Luke Skywalker", "authToken": "my token"}

    @app.route("/patients")
    @as_json
    def get_patients():
        return {"patients": patients}

    @app.route("/patient/<recordId>", methods=["GET"])
    @as_json
    def get_patient_data(recordId):
        if request.method == "GET":
            if recordId == None or patient_map.get(recordId, None) == None:
                return "Patient not found", 404

            return patient_map[recordId]

        else:
            return "Method not allowed", 405

    # Basic status endpoint.
    # TODO - move this into a blueprint
    @app.route("/")
    @as_json
    def status():
        return {"flask_status": "ok"}

    # App blueprints
    app.register_blueprint(
        blueprints.app.config.app_config_blueprint, url_prefix="/app"
    )

    # # Register all the `registry` blueprints, i.e. blueprints for web_registry
    # app.register_blueprint(registry_patients_blueprint)  # url_prefix="/patients"
    # app.register_blueprint(
    #     registry_patient_profile_blueprint
    # )  # url_prefix="/patients/<patient_collection>/profile"
    # app.register_blueprint(
    #     registry_clinical_history_blueprint
    # )  # url_prefix="/patients/<patient_collection>/clinicalhistory"
    # app.register_blueprint(
    #     registry_values_inventory_blueprint
    # )  # url_prefix="/patients/<patient_collection>/values"
    # app.register_blueprint(
    #     registry_safety_plan_blueprint
    # )  # url_prefix="/patients/<patient_collection>/safety"
    # app.register_blueprint(
    #     registry_sessions_blueprint
    # )  # url_prefix="/patients/<patient_collection>/sessions"
    # app.register_blueprint(
    #     registry_case_reviews_blueprint
    # )  # url_prefix="/patients/<patient_collection>/casereviews"
    # app.register_blueprint(
    #     registry_assessment_logs_blueprint
    # )  # url_prefix="/patients/<patient_collection>/assessmentlogs"

    # # Register all the `patient` blueprints, i.e. blueprints for web_patient
    # patient = Blueprint("patient", __name__, url_prefix="/patient")
    # patient.register_blueprint(patient_values_inventory_blueprint, url_prefix="/values")
    # patient.register_blueprint(patient_safety_plan_blueprint, url_prefix="/safety")

    # app.register_blueprint(patient)

    return app


# Instead of using `flask run`, import the app normally, then run it.
# Did this because `flask run` was eating an ImportError, not giving a useful error message.
if __name__ == "__main__":
    app = create_app()

    app.run(
        host=os.getenv("FLASK_RUN_HOST"),
        port=os.getenv("FLASK_RUN_PORT"),
    )
