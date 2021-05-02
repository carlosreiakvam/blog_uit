import binascii
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or binascii.hexlify(os.urandom(36))
    DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "BlogDB")
    DATABASE_USER = os.environ.get("DATABASE_USER", "user")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "super-secret")
    UPLOAD_DIR = os.environ.get("UPLOAD_DIR", os.path.join(basedir, "upload"))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    CKEDITOR_FILE_UPLOADER = "vedlegg.upload"
    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_HEIGHT = 400
    CKEDITOR_SERVE_LOCAL = True
    URL_PREFIX = os.environ.get("URL_PREFIX", "")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DATABASE_HOST = os.environ.get("TEST_DATABASE_HOST", "localhost")
    DATABASE_NAME = os.environ.get("TEST_DATABASE_NAME", "test_db")
    DATABASE_USER = os.environ.get("TEST_DATABASE_USER", "tester")
    DATABASE_PASSWORD = os.environ.get("TEST_DATABASE_PASSWORD", "super-secret")


class ProductionConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
