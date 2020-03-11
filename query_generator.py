from pymongo import MongoClient
from global_vars import *


def look_up_verb(verb, db_name=DB_NAME, coll_name=VERBS):
    verb = verb.lower()
    coll = MongoClient(LOCALHOST, PORT)[db_name][coll_name]
    for guess in guess_stress(verb):
        try:
            res = coll.find({PARADIGM: guess})[0]
        except IndexError:
            try:
                res = coll.find({PARADIGM: {'$elemMatch': {'$elemMatch': {'$in': [guess]}}}})[0]
            except IndexError:
                continue
        return res


def guess_stress(verb):
    guesses = [verb]
    for diacritical in DIACRITICALS:
        if diacritical in verb:
            return guesses
    for indx in range(len(verb)):
        char = verb[indx]
        if char in DIACRITICS:
            for diacritical in DIACRITICS[char]:
                guess = verb[:indx] + diacritical
                try:
                    guess += verb[indx + 1:]
                except IndexError:
                    pass
                guesses.append(guess)
    return guesses


def make_readable():
    pass


if __name__ == '__main__':
    # for v in ('αγοραζομαι', 'αγυρντιζω', 'εντυπωσιάζομαι', 'ηχογραφω'):
    #     for res in guess_stress(v):
    #         print(res)
    #     print()
    pass
