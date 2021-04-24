from datetime import datetime
from typing import List
from extensions import db
from flask import abort

from models.kommentar import Kommentar
from models.vedlegg import Vedlegg


class Innlegg:
    def __init__(self,
                 innlegg_id: int = None,
                 innlegg_tittel: str = None,
                 innlegg_innhold: str = None,
                 innlegg_dato: datetime = None,
                 innlegg_endret: datetime = None,
                 innlegg_treff: int = None,
                 blog_prefix: str = None
                 ):
        self.innlegg_id = innlegg_id
        self.innlegg_tittel = innlegg_tittel
        self.innlegg_innhold = innlegg_innhold
        self.innlegg_dato = innlegg_dato
        self.innlegg_endret = innlegg_endret
        self.innlegg_treff = innlegg_treff
        self.blog_prefix = blog_prefix
        self._kommentarer = None
        self._vedlegg = None

    @property
    def kommentarer(self) -> List[Kommentar]:
        if not self._kommentarer:
            self._kommentarer = Kommentar.get_all(self.innlegg_id)
        return self._kommentarer

    @property
    def vedlegg(self) -> List[Vedlegg]:
        if not self._vedlegg:
            self._vedlegg = Vedlegg.get_all(self.innlegg_id)
        return self._vedlegg

    @staticmethod
    def get_all(blog_navn: str) -> List["Innlegg"]:
        query = """
        select innlegg_id, 
               innlegg_tittel, 
               innlegg_innhold, 
               innlegg_dato, 
               innlegg_endret, 
               innlegg_treff,
               blog_prefix
        from innlegg where blog_prefix = %s and innlegg_dato > CURRENT_TIMESTAMP
        """

        db.cursor.execute(query, (blog_navn,))
        result = [Innlegg(*x) for x in db.cursor.fetchall()]
        return result

    @staticmethod
    def get_one(innlegg_id: int) -> "Innlegg":
        query = """
        select innlegg_id, 
               innlegg_tittel, 
               innlegg_innhold, 
               innlegg_dato, 
               innlegg_endret, 
               innlegg_treff,
               blog_prefix
        from innlegg where innlegg_id = %s
        """
        db.cursor.execute(query, (innlegg_id,))
        result = db.cursor.fetchone()
        if result:
            return Innlegg(*result)
        else:
            abort(404)

    def get_ten_newest() -> "Innlegg":
        query = """
         select innlegg_id, 
            innlegg_tittel, 
            innlegg_innhold, 
            innlegg_dato, 
            innlegg_endret, 
            innlegg_treff
         from innlegg order by innlegg_dato desc limit 10
         """

        db.cursor.execute(query)
        result = [Innlegg(*x) for x in db.cursor.fetchall()]
        return result

    def insert(self) -> "Innlegg":
        query = """
        insert into innlegg(innlegg_tittel, innlegg_innhold, blog_prefix)
        values (%s, %s, %s)
        """
        db.cursor.execute(query, (self.innlegg_tittel, self.innlegg_innhold, self.blog_prefix))
        db.connection.commit()

        return Innlegg.get_one(db.cursor.lastrowid)

    def delete(self):
        query = """
        delete from innlegg 
        where innlegg_id = %s
        """
        db.cursor.execute(query, (self.innlegg_id,))
        db.connection.commit()
