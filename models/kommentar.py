from typing import List
from extensions import db
from flask import abort


class Kommentar:
    def __init__(self,
                 id: int = None,
                 innhold: int = None,
                 brukernavn: str = None,
                 innlegg_id: int = None):
        self.id = id
        self.innhold = innhold
        self.brukernavn = brukernavn
        self.innlegg_id = innlegg_id

    @staticmethod
    def get_all() -> List["Kommentar"]:
        query = """
        select *
        from kommentarer 
        order by dato
        """
        db.cursor.execute(query)
        result = [Kommentar(*x) for x in db.cursor.fetchall()]
        return result

    @staticmethod
    def get_kommentar(kommentar_id: int) -> "Kommentar":
        query = """
        select *
        from kommentar 
        where id = %s
        """
        db.cursor.execute(query, (kommentar_id,))
        result = Kommentar(*db.cursor.fetchone())
        if result.id:
            return result
        else:
            abort(404)



# def insert_kommentar(self) -> "Kommentar":
# def delete_kommentar(self):
# def update_kommentar(self) -> "Kommentar": # Ikke nødvendig?
