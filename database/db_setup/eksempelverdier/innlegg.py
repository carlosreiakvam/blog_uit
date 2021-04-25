from models.innlegg import Innlegg
import random

BLOGGER = ["tyt005", "jbi017", "hro047", "cre032"]
TAGGER = ["Rosa", "Matlaging", "Kaker", "Duckface", "Sol", "Varme", "Eksamen", "Narvik", "UiT", "Programmering",
          "Python", "Flask"]

KOMMENTARER = [
    "Kjempefin blog!",
    "Kan vi få mer rosa?",
    "Gleder meg til neste innlegg!"
]


def opprett_innlegg():
    innlegg = [
        {
            "innlegg_tittel": "Heia Bloggen!",
            "innlegg_innhold": "hei hei"
        },
        {
            "innlegg_tittel": "Heia igjen Bloggen!",
            "innlegg_innhold": "hei hei"
        },
        {
            "innlegg_tittel": "Hvor mye rosa er for mye rosa?",
            "innlegg_innhold": "hei hei"
        }
    ]
    print(20 * "-")
    for blog in BLOGGER:
        for _innlegg in innlegg:
            innlegg_object = Innlegg(blog_prefix=blog, **_innlegg)
            innlegg_object = innlegg_object.insert()
            tagger = random.sample(TAGGER, 3)
            for tag in tagger:
                innlegg_object.add_tag(tag)
            for bruker, kommentar in zip([x for x in BLOGGER if x != blog], KOMMENTARER):
                innlegg_object.add_kommentar(kommentar_innhold=kommentar, bruker_navn=bruker)
            slett = innlegg_object.add_kommentar(kommentar_innhold="Den her vil jeg slette!", bruker_navn=blog)
            slett.delete_kommentar()
            print(f"Opprettet innlegg: {blog}: {innlegg_object.innlegg_tittel}")
