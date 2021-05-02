from datetime import datetime
from typing import List

from flask import abort

from extensions import db


class Blog:
    def __init__(self,
                 blog_prefix: str,
                 blog_navn: str,
                 bruker_navn: str,
                 blog_opprettet: datetime = None
                 ):
        self.blog_prefix = blog_prefix
        self.blog_navn = blog_navn
        self.blog_bruker_navn = bruker_navn
        self.blog_opprettet = blog_opprettet

    @staticmethod
    def get_all() -> List["Blog"]:
        query = """
            select blog_prefix, 
                    blog_navn,
                    bruker_navn,  
                    blog_opprettet
            from blog
            """

        db.cursor.execute(query)
        result = [Blog(*x) for x in db.cursor.fetchall()]
        return result

    @staticmethod
    def get_one(blog_prefix: str) -> "Blog":
        query = """
            select blog_prefix, 
                    blog_navn,
                    bruker_navn,  
                    blog_opprettet
            from blog where blog_prefix = %s
            """

        db.cursor.execute(query, (blog_prefix,))
        result = db.cursor.fetchone()
        if result:
            return Blog(*result)
        else:
            abort(404)

    @staticmethod
    def get_blog_for_user(username: str) -> "Blog":
        query = """
        select blog_prefix,
               blog_navn,
               bruker_navn,
               blog_opprettet
        from blog where bruker_navn = %s
        """
        db.cursor.execute(query, (username,))
        result = db.cursor.fetchone()
        if result:
            result = Blog(*result)
        return result

    def insert_blog(self) -> "Blog":
        query = """
        insert into blog(blog_prefix, blog_navn, bruker_navn)
        values(%s, %s, %s) 
        """

        db.cursor.execute(query, (self.blog_prefix, self.blog_navn, self.blog_bruker_navn))
        db.connection.commit()
        return self.get_one(self.blog_prefix)

    def update_blog(self) -> "Blog":
        query = """
        update blog
        set blog_navn =%s 
        where blog_prefix = %s
        """
        db.cursor.execute(
            query,
            (
                self.blog_navn,
                self.blog_prefix,
            )
        )
        db.connection.commit()
        return Blog.get_one(self.blog_prefix)
