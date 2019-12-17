import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from global_vars import LOCALHOST, PORT, DB_NAME, VERBS, VERB, TRANSL
from helpers import dump_utf_json, load_utf_json, counter


DO_JSON = 'do.json'


def collect_do():
    dump_utf_json(sorted([entry[VERB] for entry in MongoClient(LOCALHOST, PORT)[DB_NAME][VERBS].find({TRANSL: 'do'})]),
                  DO_JSON)


if __name__ == '__main__':
    collect_do()
