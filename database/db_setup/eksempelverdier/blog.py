from models.blog import Blog


def opprett_blogger():
    blogger = [
        {
            "blog_prefix": "tyt005",
            "blog_navn": "Thomas' Blog",
            "bruker_navn": "tyt005"
        },
        {
            "blog_prefix": "jbi017",
            "blog_navn": "Jan Eriks Blog",
            "bruker_navn": "jbi017"
        },
        {
            "blog_prefix": "hro047",
            "blog_navn": "Hansteins Blog",
            "bruker_navn": "hro047"
        },
        {
            "blog_prefix": "cre032",
            "blog_navn": "Carlos' Blog",
            "bruker_navn": "cre032"
        }
    ]
    print(20 * "-")
    for blog in blogger:
        blog_object = Blog(**blog)
        blog_object = blog_object.insert_blog()
        print(f"Opprettet blog: {blog_object.blog_navn}")
