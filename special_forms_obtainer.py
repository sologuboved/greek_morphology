from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

from global_vars import DB_NAME, DIACRITICALS, DIACRITICS, LOCALHOST, PARADIGM, PORT, VERBS


def look_up_verb(verb, db_name=DB_NAME, coll_name=VERBS):
    verb = verb.lower()
    coll = MongoClient(LOCALHOST, PORT)[db_name][coll_name]
    for guess in guess_stress(verb):
        res = coll.find_one({PARADIGM: guess})
        if res is None:
            res = coll.find_one({PARADIGM: {'$elemMatch': {'$elemMatch': {'$in': [guess]}}}})
            if res is None:
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
        for noun in guess_stress(noun):
            soup = BeautifulSoup(requests.get('https://el.wiktionary.org/wiki/' + noun).content, 'lxml')
            titles = {title.get('title').strip() for title in soup.find_all('a', {'title': True})}
            if 'ονομαστική' in titles and 'πληθυντικός' in titles:
                pluralis = soup.find_all('td', align='left')
                for cell in pluralis[1:]:
                    try:
                        return cell.find('a').get('title').split('(')[0].strip()
                    except AttributeError:
                        continue
