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
        result = db.cursor.fetchone()
        if result:
            return Kommentarlogg(*result)
        else:
            abort(404)

    @staticmethod
    def undo_delete(kommentar_id: int) -> Kommentar:
        delete_query = """ 
        delete from kommentar_logg 
        where kommentar_id = %s
        """

        insert_query = """
        insert into kommentarer(kommentar_id, kommentar_innhold, kommentar_dato, bruker_navn, innlegg_id)
        values (%s, %s, %s, %s, %s)
        """

        result = Kommentarlogg.get_kommentar(kommentar_id)

        db.cursor.execute(
            insert_query,
            (result.id, result.innhold, result.dato, result.brukernavn, result.innlegg_id)
        )
        db.cursor.execute(delete_query, (kommentar_id,))
        db.connection.commit()
        return Kommentar.get_kommentar(result.id)



