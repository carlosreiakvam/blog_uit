from typing import List
from extensions import db
from flask import abort


class Vedlegg:
    def __init__(self,
                 vedlegg_id=None,
                 vedlegg_navn=None,
                 vedlegg_mimetype=None,
                 bruker_navn=None
                 ):
        self.vedlegg_id = vedlegg_id
        self.vedlegg_navn = vedlegg_navn
        self.vedlegg_mimetype = vedlegg_mimetype
        self.bruker_navn = bruker_navn

    @staticmethod
    def get_all(vedlegg_id: int) -> List["Vedlegg"]:
        query = """
        select vedlegg_id, 
               vedlegg_navn,
               vedlegg_mimetype,
               bruker_navn
        from vedlegg
        where vedlegg_id = %s
        """
        db.cursor.execute(query, (vedlegg_id,))
        result = [Vedlegg(*vedlegg) for vedlegg in db.cursor.fetchall()]
        return result

    @staticmethod
    def get_by_id(vedlegg_id: int):
        query = """
                select vedlegg_id, 
                       vedlegg_navn,
                       vedlegg_mimetype,
                       bruker_navn
                from vedlegg
                where vedlegg_id = %s
                """
        db.cursor.execute(query, (vedlegg_id,))
        result = db.cursor.fetchone()
        if result:
            return Vedlegg(*result)
        else:
            abort(404)

    def insert(self) -> "Vedlegg":
        query = """
        insert into vedlegg(vedlegg_id, vedlegg_navn, vedlegg_mimetype, bruker_navn)
        values (%s, %s, %s, %s)
        """
        db.cursor.execute(query, (self.vedlegg_id, self.vedlegg_navn, self.vedlegg_mimetype, self.bruker_navn))
        db.connection.commit()
        return Vedlegg.get_by_id(db.cursor.lastrowid)

    def delete(self):
        query = """
        delete from vedlegg
        where vedlegg_id = %s
        """
        db.cursor.execute(query, (self.vedlegg_id,))

    def update(self):
        query = """
        update vedlegg set vedlegg_mimetype = %s, vedlegg_navn = %s
        """
        db.cursor.execute(query, (self.vedlegg_mimetype, self.vedlegg_navn))
        db.connection.commit()
