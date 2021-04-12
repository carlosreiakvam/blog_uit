from typing import List
from extensions import db
from flask import abort

class Kommentar_logg:
    def __init__(self,
                 id: int = None,
                 innhold: int = None,
                 dato: str = None,
                 brukernavn: str = None,
                 slettet_dato: str = None):
        self.id = id
        self.innhold = innhold
        self.brukernavn = brukernavn
        self.dato = dato
        self.slettet_dato = slettet_dato

    @staticmethod
    def get_all(innlegg_id: int) -> List["Kommentar_logg"]:
        query = """
        select 
            kommentar_id, kommentar_innhold, kommentar_dato, bruker_navn, slettet_dato
        from kommentar_logg
        where innlegg_id = %s
        order by kommentar_dato
        """
        db.cursor.execute(query, (innlegg_id,))
        result = [Kommentar_logg(*x) for x in db.cursor.fetchall()]
        return result

    @staticmethod
    def get_kommentar(kommentar_id: int) -> "Kommentar_logg":
        query = """
            select 
                kommentar_id, kommentar_innhold, kommentar_dato, bruker_navn, slettet_dato
            from kommentar_logg 
            where kommentar_id = %s
            """
        db.cursor.execute(query, (kommentar_id,))
        result = Kommentar_logg(*db.cursor.fetchone())
        if result.id:
            return result
        else:
            abort(404)

    @staticmethod
    def undoDelete(kommentar_id: int) -> "kommentar_logg":
        query = """
                    select 
                        kommentar_id, kommentar_innhold, kommentar_dato, bruker_navn
                    from kommentar_logg 
                    where kommentar_id = %s
                    """
        db.cursor.execute(query, (kommentar_id,))
        result = Kommentar_logg(*db.cursor.fetchone())
        Kommentar.insert_kommentar(result, id) #må klassen Kommentar importeres eller noe?



        '''
    def add_kommentar(self, innlegg_id) -> "Kommentar_logg":
        query = """
        insert into kommentar_logg(kommentar_innhold, bruker_navn, innlegg_id )
        values(%s, %s, %s) 
        """
        db.cursor.execute(query, (self.innhold, self.brukernavn, innlegg_id))
        db.connection.commit()
        return self.get_kommentar(db.cursor.lastrowid)
    '''