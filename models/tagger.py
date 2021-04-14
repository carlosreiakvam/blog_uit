from typing import List

from flask import abort
from extensions import db


class Tagger:
    def __init__(self,
                 tagnavn: str = None,
                 innleggid: int = None):
        self.tagnavn = tagnavn
        self.innleggid = innleggid


def add_tag(self) -> "Tagger":
    query = """
    insert into tagger(tag_navn, innlegg_id)
    values (%s, %s)
    """
    db.cursor.execute(query, (self.tagnavn, self.innleggid))
    db.connection.commit()
    return Tagger.get_tags(db.cursor.lastrowid)


def get_tags(innlegg_id) -> List["Tagger"]:
    query = """
    select tag_navn
    from tagger
    where innlegg_id = %s
    """
    db.cursor.execute(query, (innlegg_id,))
    result = [Tagger (*tagger) for tagger in db.cursor.fetchall()]
    if result.tagnavn:
        return result
    else:
        abort(404)


def delete_tag(self):
    query = """
    delete from tagger
    where tag_navn = %s and innlegg_id = %s"""
    db.cursor.execute(query, (self.tagnavn, self.innleggid))
    db.connection.commit()
