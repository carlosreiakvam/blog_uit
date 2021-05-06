from typing import List
from extensions import db


class Tagger:
    def __init__(self,
                 tagnavn: str = None,
                 innleggid: int = None,
                 antallbruk: int = None):
        self.tagnavn = tagnavn
        self.innleggid = innleggid
        self.antallbruk = antallbruk

    def add_tag(self):
        query = """
        insert into tag(tag_navn, innlegg_id)
        values (%s, %s)
        """
        db.cursor.execute(query, (self.tagnavn, self.innleggid))
        db.connection.commit()
        return self.get_tags(db.cursor.lastrowid)

    @staticmethod
    def tag_usage() -> List["Tagger"]:
        query = """
        select tag_navn,
        innlegg.innlegg_id,
        Round(((COUNT(innlegg.innlegg_id)/(SELECT COUNT(innlegg.innlegg_id) from innlegg))*150),0) as antallbruk
         from innlegg, tag
         where innlegg.innlegg_id = tag.innlegg_id GROUP BY tag.tag_navn order by RAND()
         """
        db.cursor.execute(query)
        result = [Tagger(*tagger) for tagger in db.cursor.fetchall()]
        return result

    @staticmethod
    def get_tags(innlegg_id) -> List[str]:
        query = """
        select tag_navn
        from tag
        where innlegg_id = %s
        """
        db.cursor.execute(query, (innlegg_id,))
        result = [Tagger(*tagger) for tagger in db.cursor.fetchall()]
        return result

    def delete_tag(self):
        query = """
        delete from tag
        where tag_navn = %s and innlegg_id = %s"""
        db.cursor.execute(query, (self.tagnavn, self.innleggid))
        db.connection.commit()

    @staticmethod
    def get_all_available_tags() -> List[str]:
        query = """
        select distinct tag_navn from tag 
        """
        db.cursor.execute(query)
        result = [x[0] for x in db.cursor.fetchall()]
        return result

    @staticmethod
    def get_all_available_tags_not_used_in_post(innlegg_id: int) -> List[str]:
        query = """
            select distinct tag_navn from tag
            where tag_navn not in (
                select tag_navn from tag where innlegg_id = %s
            )
            """
        db.cursor.execute(query, (innlegg_id,))
        result = [x[0] for x in db.cursor.fetchall()]
        return result
