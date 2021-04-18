from database.db_setup.eksempelverdier import brukere, blog


def insert_test_data():
    brukere.opprett_brukere()
    blog.opprett_blogger()
