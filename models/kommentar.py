from typing import List
from extensions import db
from flask import abort


# TODO: Test og reparer :). Legg merke til TODO lenger ned også
class Kommentar:
    def __init__(self,
                 id: int = None,
                 innhold: int = None,
                 brukernavn: str = None):
        self.id = id
        self.innhold = innhold
        self.brukernavn = brukernavn

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


def insert_kommentar(self) -> "Kommentar":
    # TODO: Få inn innlegg_id fra innlegg model
    query = """
    insert into kommentar(kommentar_id, kommentar_innhold,brukernavn,innlegg_id )
    values(%s, %s, %s, %s) 
    """

    db.cursor.execute(
        query, (self.id, self.inhold, self.brukernavn, self.innlegg_id)
    )
    db.connection.commit()
    return self.get_post(db.cursor.lastrowid)


def delete_kommentar(self):
    query = """
    delete *
    from kommentar where
    id = %s
    """
    db.cursor.execute(query, (self.id,))
    db.connection.commit()