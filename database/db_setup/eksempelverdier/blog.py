from models.blog import Blog

def insert_blog():
    #blog = Blog("Tittelen", "Bloggtittel", "test2", None)
    #blog.insert_blog()
    blog = Blog.get_one("Tittelen")
    blog.blog_tittel="ny tittel"
    blog.update_blog()