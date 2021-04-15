from models.bruker import Bruker


def legg_inn_bruker():
    bruker = Bruker(brukernavn="test2", epost="test@test.no", opprettet=None, fornavn="test", etternavn="test")
    bruker.hash_password("asdasd")
    bruker.insert_user()


def sjekk_passord():
    bruker = Bruker.get_user("test2")
    print(bruker.check_password("asdasd"))

