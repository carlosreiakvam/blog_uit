from datetime import date
from werkzeug import generate_password_hash, check_password_hash, abort
from extensions import db


class Bruker:
    def __init__(self,
                 brukernavn: str = None,
                 epost: str = None,
                 passord: str = None,
                 opprettet: date = None,
                 fornavn: str = None,
                 etternavn: str = None):
        self.brukernavn = brukernavn
        self.epost = epost
        self.passord = passord
        self.opprettet = opprettet
        self.fornavn = fornavn
        self.etternavn = etternavn


def hash_password(password):
    return generate_password_hash(password)


def check_password(username, password):
    return bool(check_password_hash(get_password(username), password))


def get_password(username: str):
    query = """
    select bruker_passord_hash
    from brukere
    where bruker_navn = %s
    """
    db.cursor.execute(query, (username,))
    result = Bruker(*db.cursor.fetchone())
    if result.brukernavn:
        return result
    else:
        abort(404)

def get_bruker(username):
    query = """
    select bruker_navn,
        bruker_epost,
        bruker_opprettet,
        bruker_fornavn,
        bruker_etternavn
    from brukere
    where bruker_navn = %s
    """
    db.cursor.execute(query, (username,))
    result = Bruker(*db.cursor.fetchone())
    if result.brukernavn:
        return result
    else:
        abort(404)
