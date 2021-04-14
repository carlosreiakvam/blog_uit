from typing import List
from extensions import db
from flask import abort
from models.kommentar import Kommentar

class Kommentarlogg:
    def __init__(self,
                 id: int = None,
                 innhold: int = None,
                 dato: str = None,
                 brukernavn: str = None,
                 innlegg_id: str = None,
                 slettet_dato: str = None):
        self.id = id
        self.innhold = innhold
        self.brukernavn = brukernavn
        self.dato = dato
        self.innlegg_id = innlegg_id
        self.slettet_dato = slettet_dato

    @staticmethod
    def get_all(innlegg_id: int) -> List["Kommentarlogg"]:
        query = """
        select 
            kommentar_id, kommentar_innhold, kommentar_dato, bruker_navn, innlegg_id, slettet_dato
        from kommentar_logg
        where innlegg_id = %s
        order by kommentar_dato
        """
        db.cursor.execute(query, (innlegg_id,))
        result = [Kommentarlogg(*x) for x in db.cursor.fetchall()]
        return result

    @staticmethod
    def get_kommentar(kommentar_id: int) -> "Kommentarlogg":
        query = """
            select 
                kommentar_id, kommentar_innhold, kommentar_dato, bruker_navn, innlegg_id, slettet_dato
            from kommentar_logg 
            where kommentar_id = %s
            """
        db.cursor.execute(query, (kommentar_id,))
        result = Kommentarlogg(*db.cursor.fetchone())
        if result.id:
            return result
        else:
            abort(404)

    @staticmethod
    def undo_Delete(kommentar_id: int) -> "kommentar_logg":

        deletequery = """ 
                delete from kommentar_logg 
                where kommentar_id = %s"""


        result = Kommentarlogg.get_kommentar(kommentar_id)

        kommentar = Kommentar(
            id=result.id,
            innhold=result.innhold,
            dato=result.dato,
            brukernavn=result.brukernavn,
            innlegg_id=result.innlegg_id
        )
        kommentar.insert_kommentar(result.innlegg_id)


        db.cursor.execute(deletequery, (kommentar_id,))
        date_query = "insert into kommentar(dato) values (%s);"
        db.cursor.execute(date_query, result.dato, )
        db.connection.commit()
        Kommentar.insert_kommentar(result, id)


