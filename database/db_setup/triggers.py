from extensions import db
from mysql.connector import errorcode, Error
from flask import current_app

TRIGGERS = {}

TRIGGERS["kommentar_BEFORE_DELETE"] = """
CREATE TRIGGER 
`kommentar_BEFORE_DELETE` 
BEFORE DELETE ON `kommentar` FOR EACH ROW
BEGIN
    insert into `kommentar_logg` (kommentar_id, kommentar_innhold, kommentar_dato, bruker_navn, innlegg_id, slettet_dato)
    values (OLD.kommentar_id, OLD.kommentar_innhold, OLD.kommentar_dato, OLD.bruker_navn, OLD.innlegg_id, CURRENT_TIMESTAMP); 
END;
"""


def create_triggers():
    cursor = db.connection.cursor()
    cursor.execute("USE {}".format(current_app.config['DATABASE_NAME']))
    for trigger_name, trigger_definition in TRIGGERS.items():
        try:
            print(f"Creating trigger {trigger_name}: ", end="")
            cursor.execute(trigger_definition)
        except Error as err:
            if err.errno == errorcode.ER_TRG_ALREADY_EXISTS:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
    cursor.close()
