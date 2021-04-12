from extensions import db
from mysql.connector import errorcode, Error
from flask import current_app

TEST_DATA = {}

TEST_DATA["blog"] = """ """
TEST_DATA["brukere"] = """ """
TEST_DATA["innlegg"] = """ """
TEST_DATA["kommentarer"] = """ """
TEST_DATA["tagger"] = """ """


def create_test_data():
    cursor = db.connection.cursor()
    cursor.close
