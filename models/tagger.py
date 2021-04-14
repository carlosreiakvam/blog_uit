from werkzeug.exceptions import abort

from extensions import db


class Tagger():
    def __init__(self,
                 tagnavn: str = None,
                 innleggid: int = None):
        self.tagnavn = tagnavn
        self.innleggid = innleggid


def add_tags(self) -> "Tagger":
    query = """
    insert into tagger(tag_navn, innlegg_id)
    values (%s, %s)
    """
    db.cursor.execute(query, (self.tagnavn, self.innleggid))
    db.connection.commit()
    return Tagger.get_tags(db.cursor.lastrowid)


def get_tags(innlegg_id) -> "Tagger":
    query = """
    select tag_navn
    from tagger
    where innlegg_id = %s
    """
    db.cursor.execute(query, (innlegg_id,))
    result = Tagger(*db.cursor.fetchall())
    if result.tagnavn:
        return result
    else:
        abort(404)
