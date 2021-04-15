from app import create_app
from database.db_setup.tables import create_tables, drop_tables
from database.db_setup.triggers import create_triggers
from database.db_setup.eksempelverdier.brukere import *
from flask.cli import AppGroup

app = create_app()
database_cli = AppGroup("db")


@database_cli.command("init")
def init_db():
    create_tables()
    create_triggers()


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
    else:
        print("Har ikke gjort noen endringer")


app.cli.add_command(database_cli)

if __name__ == '__main__':
    app.run(load_dotenv=True)
