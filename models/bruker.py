from datetime import date
from os import abort

from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models.blog import Blog


class Bruker:
    def __init__(self,
                 brukernavn: str = None,
                 epost: str = None,
                 opprettet: date = None,
                 fornavn: str = None,
                 etternavn: str = None):
        self._passwordhash = None
        self.brukernavn = brukernavn
        self.epost = epost
        self.opprettet = opprettet
        self.fornavn = fornavn
        self.etternavn = etternavn
        self._blog = None

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def fullt_navn(self):
        return f"{self.fornavn} {self.etternavn}"

    @property
    def blog(self):
        if not self._blog:
            self._blog = Blog.get_blog_for_user(self.brukernavn)
        return self._blog

    def get_id(self):
        return self.brukernavn

    def hash_password(self, password):
        self._passwordhash = generate_password_hash(password)

    def check_password(self, password):
        return bool(check_password_hash(self._get_password(), password))

    def _get_password(self) -> str:
        query = """
        select bruker_passord_hash
        from bruker
        where bruker_navn = %s
        """
        db.cursor.execute(query, (self.brukernavn,))
        result = db.cursor.fetchone()
        if not result:
            abort(404)
        else:
            return result[0]

    @staticmethod
    def get_user(username) -> "Bruker":
        query = """
        select bruker_navn,
            bruker_epost,
            bruker_opprettet,
            bruker_fornavn,
            bruker_etternavn
        from bruker
        where bruker_navn = %s
        """
        db.cursor.execute(query, (username,))
        result = db.cursor.fetchone()
        if result:
            result = Bruker(*result)
        return result

    @staticmethod
    def get_user_for_blog(blog_prefix: str) -> "Bruker":
        query = """
        select bruker.bruker_navn,
            bruker_epost,
            bruker_opprettet,
            bruker_fornavn,
            bruker_etternavn
        from bruker
        join blog b on bruker.bruker_navn = b.bruker_navn
        where b.blog_prefix = %s
        """
        db.cursor.execute(query, (blog_prefix,))
        result = db.cursor.fetchone()
        if result:
            result = Bruker(*result)
        return result

    def insert_user(self) -> "Bruker":
        query = """
        insert into bruker(bruker_navn,
            bruker_epost,
            bruker_passord_hash,
            bruker_fornavn,
            bruker_etternavn)
        values (%s, %s, %s, %s, %s)
        """
        db.cursor.execute(query, (self.brukernavn, self.epost, self._passwordhash, self.fornavn,
                                  self.etternavn))
        db.connection.commit()
        return Bruker.get_user(self.brukernavn)
