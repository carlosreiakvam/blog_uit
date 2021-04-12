from typing import List
from extensions import db
from flask import abort


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
        db.cursor.execute(query, innlegg_id, )
        result = [Kommentar(*x) for x in db.cursor.fetchall()]
        return result

    @staticmethod
    def get_kommentar(kommentar_id: int) -> "Kommentar":
        query = """
        select 
            kommentar_id, kommentar_innhold, kommentar_dato, bruker_navn
        from kommentar 
        where kommentar_id = %s
        """
        db.cursor.execute(query, (kommentar_id,))
        result = Kommentar(*db.cursor.fetchone())
        if result.id:
            return result
        else:
            abort(404)

    def insert_kommentar(self, innlegg_id) -> "Kommentar":
        query = """
            insert into kommentar(kommentar_id, kommentar_innhold,brukernavn,innlegg_id )
        values((select innlegg_id from innlegg where innlegg_id = %s) %s, %s, %s, %s) 
        """
        db.cursor.execute(query, (innlegg_id, self.id, self.inhold, self.brukernavn, self.innlegg_id))
        db.connection.commit()
        return self.get_post(db.cursor.lastrowid)

    def delete_kommentar(self):
        query = """ 
        delete from kommentar 
        where id = %s"""
        db.cursor.execute(query, (self.id,))
        db.connection.commit()
