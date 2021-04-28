from models.bruker import Bruker


def opprett_brukere():
    brukere = [
        {
            "brukernavn": "tyt005",
            "epost": "tyt005@post.uit.no",
            "fornavn": "Thomas",
            "etternavn": "Ytterdal"
        },
        {
            "brukernavn": "jbi017",
            "epost": "jbi017@post.uit.no",
            "fornavn": "Jan Erik",
            "etternavn": "Skaiå Bisseth"
        },
        {
            "brukernavn": "hro047",
            "epost": "hro047@post.uit.no",
            "fornavn": "Hanstein",
            "etternavn": "Rommerud"
        },
        {
            "brukernavn": "cre032",
            "epost": "cre032@post.uit.no",
            "fornavn": "Carlos",
            "etternavn": "Reiakvam"
        }
    ]
    print(20 * "-")
    for bruker in brukere:
        bruker_object = Bruker(**bruker)
        bruker_object.hash_password("super-secret")
        bruker_object = bruker_object.insert_user()
        print(f"Opprettet bruker: {bruker_object.brukernavn}")

