from typing import List
from extensions import db


class Tagger:
    def __init__(self,
                 tagnavn: str = None,
                 innleggid: int = None):
        self.tagnavn = tagnavn
        self.innleggid = innleggid

    def add_tag(self):
        query = """
        insert into tagger(tag_navn, innlegg_id)
        values (%s, %s)
        """
        db.cursor.execute(query, (self.tagnavn, self.innleggid))
        db.connection.commit()
        return self.get_tags(db.cursor.lastrowid)

    @staticmethod
    def get_tags(innlegg_id) -> List["Tagger"]:
        query = """
        select tag_navn
        from tagger
        where innlegg_id = %s
        """
        db.cursor.execute(query, (innlegg_id,))
        result = [Tagger(*tagger) for tagger in db.cursor.fetchall()]
        return result

    def delete_tag(self):
        query = """
        delete from tagger
        where tag_navn = %s and innlegg_id = %s"""
        db.cursor.execute(query, (self.tagnavn, self.innleggid))
        db.connection.commit()

    @staticmethod
    def get_all_available_tags() -> List[str]:
        query = """
        select distinct tag_navn from tagger 
        """
        db.cursor.execute(query)
        result = [x[0] for x in db.cursor.fetchall()]
        return result

    @staticmethod
    def get_all_available_tags_not_used_in_post(innlegg_id: int) -> List[str]:
        query = """
            select distinct tag_navn from tagger
            where tag_navn not in (
                select tag_navn from tagger where innlegg_id = %s
            )
            """
        db.cursor.execute(query, (innlegg_id,))
        result = [x[0] for x in db.cursor.fetchall()]
        return result
