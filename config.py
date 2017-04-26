import os

import dotenv

dotenv.load()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    This is the base class for all configuration classes. it contains the
    basic settings common to the three environments.
    """
    SECRET_KEY = dotenv.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """
    This is the configuration settings for the development environment.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = dotenv.get('DEV_DATABASE_URL').format(basedir)
    SERVER_NAME = dotenv.get('SERVER_NAME')


class TestingConfig(Config):
    """
    This is the configuration settings for the testing environment.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = dotenv.get('TEST_DATABASE_URL').format(basedir)
    SERVER_NAME = dotenv.get('SERVER_NAME')


class ProductionConfig(Config):
    """
    This is the configuration settings for the production environment.
    """
    SQLALCHEMY_DATABASE_URI = dotenv.get('DATABASE_URL').format(basedir)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
