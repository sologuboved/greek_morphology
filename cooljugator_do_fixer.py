import re
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from global_vars import LOCALHOST, PORT, DB_NAME, VERBS, VERB, TRANSL, COOLJUGATOR_DO_TRANSL
from helpers import dump_utf_json, load_utf_json, counter, which_watch


DO_JSON = 'do.json'


def collect_do():
    dump_utf_json(sorted([entry[VERB] for entry in MongoClient(LOCALHOST, PORT)[DB_NAME][VERBS].find({TRANSL: 'do'})]),
                  DO_JSON)


@which_watch
def collect_transls():
    pattern = re.compile(r'\((.+?)\)')
    doed = load_utf_json(DO_JSON)
    transls = dict()
    count = counter(len(doed))
    for verb in doed:
        next(count)
        transls[verb] = pattern.findall(
            BeautifulSoup(
                requests.get('https://cooljugator.com/gr/' + verb).content, 'lxml'
            ).find('span', id='mainform').text
        )[0]
    print()
    dump_utf_json(transls, COOLJUGATOR_DO_TRANSL)


@which_watch
def fix_transls():
    coll = MongoClient(LOCALHOST, PORT)[DB_NAME][VERBS]
    transls = load_utf_json(DO_JSON).items()
    count = counter(len(transls))
    for verb, transl in transls:
        next(count)
        match = coll.find({VERB: verb, TRANSL: 'do'})[0]
        match[TRANSL] = transl
        coll.save(match)
    print()


if __name__ == '__main__':
    # collect_do()
    # collect_transls()
    fix_transls()
