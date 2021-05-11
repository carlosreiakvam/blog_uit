import os

from app import create_app
from database.db_setup.tables import create_tables, drop_tables
from database.db_setup.triggers import create_triggers
from database.db_setup.insert_data import insert_test_data
from flask.cli import AppGroup

from extensions import db
from models.vedlegg import Vedlegg

app = create_app()
database_cli = AppGroup("db")

MIMETYPER = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif"
}


@database_cli.command("init")
def init_db():
    create_tables()
    create_triggers()
    insert_test_data()


@database_cli.command("reset")
def reset_db():
    print("Denne kommandoen vil slette databasen og gjenopprette tabellene (ALL DATA VIL BLI SLETTET)")
    answer = input("Er du sikker på at du vil fortsette? (ja/nei): ")
    if answer.upper() == "JA":
        drop_tables()
        print(20 * "-")
        create_tables()
        print(20 * "-")
        create_triggers()
        insert_test_data()
    else:
        print("Har ikke gjort noen endringer")


@database_cli.command("delete")
def delete_db():
    print("Denne kommandoen vil slette databasen (ALL DATA VIL BLI SLETTET)")
    answer = input("Er du sikker på at du vil fortsette? (ja/nei): ")
    if answer.upper() == "JA":
        drop_tables()
    else:
        print("Har ikke gjort noen endringer")


@database_cli.command("add-mimetypes")
def add_mimetypes():
    print("legger til mimetyper for vedlegg")
    query = """
    ALTER TABLE vedlegg ADD COLUMN `vedlegg_mimetype` VARCHAR(45) NOT NULL DEFAULT '';
    """
    db.cursor.execute(query)
    alle_vedlegg = Vedlegg.get_all()
    for vedlegg in alle_vedlegg:
        filename, extension = os.path.splitext(vedlegg.vedlegg_navn)
        vedlegg.vedlegg_mimetype = MIMETYPER[extension]
        vedlegg.update()


app.cli.add_command(database_cli)

if __name__ == '__main__':
    app.run(load_dotenv=True)
