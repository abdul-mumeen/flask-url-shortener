import os

import dotenv

dotenv.load()


class Config:
    SECRET_KEY = dotenv.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = dotenv.get('DEV_DATABASE_URL')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = dotenv.get('TEST_DATABASE_URL')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = dotenv.get('DATABASE_URL')

config = {    'development': DevelopmentConfig,    'testing': TestingConfig,    'production': ProductionConfig,    'default': DevelopmentConfig}
