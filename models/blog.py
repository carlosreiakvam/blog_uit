from extensions import db
from flask import abort
from typing import List


class Blog:
    def __init__(self,
                 blog_navn: str,
                 blog_tittel: str,
                 brukere_bruker_navn: str,
                 blog_opprettet: str
                 ):
        self.blog_navn = blog_navn
        self.blog_tittel = blog_tittel
        self.blog_bruker_navn = brukere_bruker_navn
        self.blog_opprettet = blog_opprettet

    @staticmethod
    def get_all() -> List["Blog"]:
        query = """
            select blog_navn, 
                    blog_tittel,
                    blog_brukere_brukernavn,  
                    blog_opprettet,
            from blog
            """

        db.cursor.execute(query,)
        result = [Blog(*x) for x in db.cursor.fetchall()]
        return result


    @staticmethod
    def get_one(blog_navn: str, bruker: str) -> "Blog":
        query = """
            select blog_navn, 
                    blog_tittel,
                    blog_brukere_brukernavn,  
                    blog_opprettet,
            from blog where (blog_navn = %s and blog_brukere_brukernavn = %s)
            """

        db.cursor.execute(query, (blog_navn, bruker,))
        result = Blog(*db.cursor.fetchone())
        if result.blog_navn:
            return result
        else:
            abort(404)

    @staticmethod
    def get_all_by_user_name(bruker_navn: str) -> "Blog":
        query = """
            select blog_navn, 
                    blog_tittel,
                    blog_brukere_brukernavn,  
                    blog_opprettet,
            from blog where blog_brukere_brukernavn = %s
            """

        db.cursor.execute(query, (bruker_navn,))
        result = [Blog(*x) for x in db.cursor.fetchall()]
        return result

    def insert_blog(self) -> "Blog":
        query = """
        insert into blog(blog_navn, blog_tittel, blog_bruker_navn)
        values(%s, %s, %s) 
        """

        db.cursor.execute(query, (self.blog_navn, self.blog_tittel, self.blog_bruker_navn))
        db.connection.commit()
        return self.get_one(db.cursor.lastrowid)