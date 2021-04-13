from typing import List
from extensions import db
from flask import abort


class Vedlegg:
    def __init__(self,
                 vedlegg_id=None,
                 vedlegg_navn=None,
                 vedlegg_beskrivelse=None,
                 vedlegg_path=None,
                 innlegg_id=None
                 ):
        self.vedlegg_id = vedlegg_id
        self.vedlegg_navn = vedlegg_navn
        self.vedlegg_beskrivelse = vedlegg_beskrivelse
        self.vedlegg_path = vedlegg_path
        self.innlegg_id = innlegg_id

    @staticmethod
    def get_all(innlegg_id: int) -> List["Vedlegg"]:
        query = """
        select vedlegg_id, 
               vedlegg_navn, 
               vedlegg_beskrivelse, 
               vedlegg_path, 
               innlegg_id
        from vedlegg
        where innlegg_id = %s
        """
        db.cursor.execute(query, (innlegg_id,))
        result = [Vedlegg(*vedlegg) for vedlegg in db.cursor.fetchall()]
        return result

    @staticmethod
    def get_by_id(innlegg_id: int):
        query = """
                select vedlegg_id, 
                       vedlegg_navn, 
                       vedlegg_beskrivelse, 
                       vedlegg_path, 
                       innlegg_id
                from vedlegg
                where innlegg_id = %s
                """
        db.cursor.execute(query, (innlegg_id,))
        result = db.cursor.fetchone()
        if result:
            return Vedlegg(*result)
        else:
            abort(404)

    def insert(self) -> "Vedlegg":
        query = """
        insert into vedlegg(vedlegg_navn, vedlegg_beskrivelse, vedlegg_path, innlegg_id)
        values (%s, %s, %s, %s)
        """
        db.cursor.execute(query, (self.vedlegg_navn, self.vedlegg_beskrivelse, self.vedlegg_path, self.innlegg_id))
        return Vedlegg.get_by_id(db.cursor.lastrowid)

    def delete(self):
        query = """
        delete from vedlegg
        where vedlegg_id = %s
        """
        db.cursor.execute(query, (self.vedlegg_id,))
