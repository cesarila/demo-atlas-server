import os
basedir = os.path.abspath(os.path.dirname(__file__))


# This class is based on the Config class from "Flask Web Development" by Miguel Grinberg
class Config:
    # We will learn how to store our secrets properly in a few short weeks.
    # In the meantime, we'll use this:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "Don't ever store secrets in your actual code"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        # This can/should be implemented in the child classes
        pass

    @staticmethod
    def database_path_for(database_name):
        return "postgresql://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', database_name)
        # Alternative option if your postgres installation isn't set up to require auth:
        # return "postgresql://{}/{}".format('localhost:5432', database_name)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or Config.database_path_for("demoatlas_app_dev")
    # For local debugging purposes.  Not ideal for production environements:
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or Config.database_path_for("tests")
    LIVESERVER_PORT = 8910


class ProductionConfig(Config):
    # Fixing Heroku database URL per https://stackoverflow.com/a/66787229/35345
    env_variable = os.environ.get('DATABASE_URL')
    if env_variable:
        SQLALCHEMY_DATABASE_URI = env_variable.replace("://", "ql://", 1)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
