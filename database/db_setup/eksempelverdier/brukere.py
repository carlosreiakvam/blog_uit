from models.bruker import Bruker


def legg_inn_bruker():
    bruker = Bruker(brukernavn="test", epost="test@test.no", opprettet=None, fornavn="test", etternavn="test")
    bruker.hash_password("asdasd")
    bruker.insert_user()


def sjekk_passord():
    bruker = Bruker.get_user("janerik")
    bruker.check_password("test")
