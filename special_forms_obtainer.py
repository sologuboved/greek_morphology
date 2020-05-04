import requests
from bs4 import BeautifulSoup
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


def guess_stress(word):
    guesses = [word]
    for diacritical in DIACRITICALS:
        if diacritical in word:
            return guesses
    for indx in range(len(word)):
        char = word[indx]
        if char in DIACRITICS:
            for diacritical in DIACRITICS[char]:
                guess = word[:indx] + diacritical
                try:
                    guess += word[indx + 1:]
                except IndexError:
                    pass
                guesses.append(guess)
    return guesses


def look_up_fem_nom_pl(noun):
    if noun.endswith('η') or noun.endswith('ή'):
        soup = BeautifulSoup(requests.get('https://el.wiktionary.org/wiki/' + noun).content, 'lxml')
        titles = {title.get('title').strip() for title in soup.find_all('a', {'title': True})}
        if 'ονομαστική' in titles and 'πληθυντικός' in titles:
            pluralis = soup.find_all('td', align='left')
            for cell in pluralis[1:]:
                try:
                    return cell.find('a').get('title').split('(')[0].strip()
                except AttributeError:
                    continue


if __name__ == '__main__':
    # for v in ('αγοραζομαι', 'αγυρντιζω', 'εντυπωσιάζομαι', 'ηχογραφω'):
    #     for res in guess_stress(v):
    #         print(res)
    #     print()
    # print(look_up_fem_nom_pl('θάλασση'))
    # print(look_up_fem_nom_pl('επιτροπή'))
    # print(look_up_fem_nom_pl('άφιξη'))
    # print(look_up_fem_nom_pl('εισαγωγή'))
    # print(look_up_fem_nom_pl('ηδονή'))
    pass
