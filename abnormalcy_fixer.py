import re

from bs4 import BeautifulSoup
from bson.objectid import ObjectId
from pymongo import MongoClient
import requests

from cooljugator_globals import COOLJUGATOR_DO_TRANSL
from db_ops import save_entry
from global_vars import DB_NAME, LOCALHOST, PORT, TRANSL, VERB, VERBS
from helpers import counter, dump_utf_json, load_utf_json, which_watch

DO_JSON = 'do.json'
DUPLICATES_JSON = 'duplicates.json'
MORPH_ANOMALIES_JSON = 'morph_anomalies.json'


def collect_do():
    dump_utf_json(
        sorted([entry[VERB] for entry in MongoClient(LOCALHOST, PORT)[DB_NAME][VERBS].find({TRANSL: 'do'})]),
        DO_JSON,
    )


@which_watch
def collect_do_transls():
    pattern = re.compile(r'\((.+?)\)')
    doed = load_utf_json(DO_JSON)
    transls = dict()
    count = counter(len(doed))
    for verb in doed:
        next(count)
        transls[verb] = pattern.findall(
            BeautifulSoup(
                requests.get('https://cooljugator.com/gr/' + verb).content,
                'lxml',
            ).find('span', id='mainform').text,
        )[0]
    print()
    dump_utf_json(transls, COOLJUGATOR_DO_TRANSL)


@which_watch
def fix_do_transls():
    coll = MongoClient(LOCALHOST, PORT)[DB_NAME][VERBS]
    transls = load_utf_json(DO_JSON).items()
    count = counter(len(transls))
    for verb, transl in transls:
        next(count)
        match = coll.find_one({VERB: verb, TRANSL: 'do'})
        match[TRANSL] = transl
        save_entry(coll, match)
    print()


def clean_do():
    coll = MongoClient(LOCALHOST, PORT)[DB_NAME][VERBS]
    for entry in coll.find({VERB: {'$ne': 'κάνω'}, TRANSL: 'do'}):
        entry[TRANSL] = str()
        save_entry(coll, entry)


@which_watch
def collect_duplicates():
    visited = set()
    duplicates = set()
    coll = MongoClient(LOCALHOST, PORT)[DB_NAME][VERBS]
    count = counter(coll.estimated_document_count())
    for entry in coll.find():
        next(count)
        verbs = entry[VERB]
        if isinstance(verbs, str):
            verbs = [verbs]
        for verb in verbs:
            if verb in visited:
                duplicates.add(verb)
            else:
                visited.add(verb)
    print("\nDumping {} duplicates".format(len(duplicates)))
    dump_utf_json(sorted(list(duplicates)), DUPLICATES_JSON)


@which_watch
def remove_duplicates():
    def delete_except(good_entry):
        coll.delete_many({VERB: verb, '_id': {'$ne': ObjectId(good_entry['_id'])}})

    merge_count = translationless_count = identical_count = 0
    abnormal = set()
    coll = MongoClient(LOCALHOST, PORT)[DB_NAME][VERBS]
    for verb in load_utf_json(DUPLICATES_JSON):
        translated = biformed = silly = None
        for entry in coll.find({VERB: verb}):
            if isinstance(entry[VERB], list):
                biformed = entry
            elif entry[TRANSL]:
                translated = entry
            else:
                silly = entry
        if biformed and translated:
            biformed[TRANSL] = translated[TRANSL]
            save_entry(coll, biformed)
            delete_except(biformed)
            merge_count += 1
        elif translated:
            delete_except(translated)
            translationless_count += 1
        elif biformed:
            delete_except(biformed)
            identical_count += 1
        elif silly:
            delete_except(silly)
            identical_count += 1
        else:
            abnormal.add(verb)
    print("Merged {} entries. "
          "Deleted translationless duplicates {} times, "
          "identical duplicates {} times.".format(merge_count, translationless_count, identical_count))
    if abnormal:
        print("Abnormal duplicates ({}):".format(len(abnormal)))
        for duplicate in abnormal:
            print(duplicate)
    else:
        print("No further abnormalities")


def remove_morphologically_abnormal_verbs():
    abnormal_count = 0
    coll = MongoClient(LOCALHOST, PORT)[DB_NAME][VERBS]
    count = counter(coll.estimated_document_count())
    for entry in coll.find():
        next(count)
        verbs = entry[VERB]
        if isinstance(verbs, str):
            verbs = [verbs]
        for verb in verbs:
            if not (verb.endswith('ω') or verb.endswith('ώ') or verb.endswith('αι')):
                coll.delete_one({VERB: verb})
                abnormal_count += 1
    print("\nRemoved {} abnormal verbs".format(abnormal_count))
