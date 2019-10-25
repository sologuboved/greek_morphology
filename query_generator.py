from pymongo import MongoClient
from global_vars import *


def look_up_verb(verb, minimalistic=True, db_name=DB_NAME, coll_name=VERBS):
    coll = MongoClient(LOCALHOST, PORT)[db_name][coll_name]
    for guess in guess_stress(verb):
        try:
            res = coll.find({VERB: guess})[0]
        except IndexError:
            continue
        if minimalistic:
            return res[VERB], res[AORIST], res[FUTURUM], res[TRANSL]
        return res[PARADIGM]


def guess_stress(verb):
    for diacritical in DIACRITICALS:
        if diacritical in verb:
            return [verb]
    guesses = list()
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

