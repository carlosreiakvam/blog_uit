from typing import List
from extensions import db
from flask import abort


class Vedlegg:
    def __init__(self,
                 vedlegg_id=None,
                 vedlegg_navn=None
                 ):
        self.vedlegg_id = vedlegg_id
        self.vedlegg_navn = vedlegg_navn

    @staticmethod
    def get_all(vedlegg_id: int) -> List["Vedlegg"]:
        query = """
        select vedlegg_id, 
               vedlegg_navn
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
                       vedlegg_navn
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
        insert into vedlegg(vedlegg_id, vedlegg_navn)
        values (%s, %s)
        """
        db.cursor.execute(query, (self.vedlegg_id, self.vedlegg_navn))
        db.connection.commit()
        return Vedlegg.get_by_id(db.cursor.lastrowid)

    def delete(self):
        query = """
        delete from vedlegg
        where vedlegg_id = %s
        """
        db.cursor.execute(query, (self.vedlegg_id,))
