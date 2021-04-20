from database.db_setup.eksempelverdier import brukere, blog, innlegg


def insert_test_data():
    brukere.opprett_brukere()
    blog.opprett_blogger()
    innlegg.opprett_innlegg()
