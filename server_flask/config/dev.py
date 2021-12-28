import os

import scope.config
from config.base import Config

# Path is relative to server_flask
DEV_LOCAL_FLASK_CONFIG_PATH = "../secrets/configuration/dev_local_flask.yaml"


class DevelopmentConfig(Config):
    def __init__(self):
        flask_config = scope.config.FlaskConfig.load(DEV_LOCAL_FLASK_CONFIG_PATH)

        Config.__init__(
            self=self,
            secret_key=flask_config.secret_key,
            documentdb_host=flask_config.documentdb_host,
            documentdb_port=int(os.getenv("DOCUMENTDB_LOCAL_PORT")),
            documentdb_directconnection=flask_config.documentdb_directconnection,
            documentdb_tlsinsecure=flask_config.documentdb_tlsinsecure,
            database_name=flask_config.database_name,
            database_user=flask_config.database_user,
            database_password=flask_config.database_password,
        )
