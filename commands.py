from app import create_app
from database.db_setup.tables import create_tables
from database.db_setup.triggers import create_triggers
from database.db_setup.eksempelverdier.brukere import *
from flask.cli import AppGroup

app = create_app()
database_cli = AppGroup("db")


@database_cli.command("init")
def init_db():
    create_tables()
    create_triggers()


@database_cli.command("eksempelbruker")
def eksempelbruker():
    legg_inn_bruker()


app.cli.add_command(database_cli)

if __name__ == '__main__':
    app.run(load_dotenv=True)
