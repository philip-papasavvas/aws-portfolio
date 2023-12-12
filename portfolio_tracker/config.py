"""
Created on: 12 Dec 2023
Config file with DB connection strings, API keys, environment specific variables etc.
"""
import os


class Config(object):
    """
    Base configuration class. Contains default settings.
    """
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """
    Configuration settings for production environment.
    """
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Configuration settings for development environment.
    """
    DEBUG = True
    DEVELOPMENT = True


class TestingConfig(Config):
    """
    Configuration settings for testing environment.
    """
    TESTING = True
