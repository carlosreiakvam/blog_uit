from typing import List
from extensions import db
from flask import abort

# Legg til disse imports når de er klare
# from database.db_setup import innlegg
# from database.db_setup import bruker

class Kommentar:
    def __init__(self,
                 id: int = None,
                 innhold: int = None,
                 dato: str = None,
                 brukernavn: str = None):
        self.id = id
        self.innhold = innhold
        self.brukernavn = brukernavn
        self.dato = dato


    @staticmethod
    def get_all(innlegg_id: int) -> List["Kommentar"]:
        query = """
        select 
            kommentar_id, kommentar_innhold, kommentar_dato, bruker_navn
        from kommentarer
        where innlegg_id = %s
        order by kommentar_dato
        """
        db.cursor.execute(query, (innlegg_id,))
        result = [Kommentar(*x) for x in db.cursor.fetchall()]
        return result

    @staticmethod
    def get_kommentar(kommentar_id: int) -> "Kommentar":
        query = """
        select 
            kommentar_id, kommentar_innhold, kommentar_dato, bruker_navn
        from kommentarer 
        where kommentar_id = %s
        """
        db.cursor.execute(query, (kommentar_id,))
        result = db.cursor.fetchone()
        if result:
            return Kommentar(*result)
        else:
            abort(404)

    # brukernavn må importeres og hentes fra tabell bruker
    # innlegg_id må importeres og hentes fra tabell innlegg
    def insert_kommentar(self, innlegg_id) -> "Kommentar":
        query = """
        insert into kommentarer(kommentar_innhold, bruker_navn, innlegg_id )
        values(%s, %s, %s) 
        """
        db.cursor.execute(query, (self.innhold, self.brukernavn, innlegg_id))
        db.connection.commit()
        return self.get_kommentar(db.cursor.lastrowid)

    def delete_kommentar(self):
        query = """ 
        delete from kommentarer 
        where kommentar_id = %s"""
        db.cursor.execute(query, (self.id,))
        db.connection.commit()