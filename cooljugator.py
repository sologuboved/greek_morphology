import requests
from bs4 import BeautifulSoup
from global_vars import *
from helpers import which_watch, dump_utf_json, load_utf_json


@which_watch
def collect_verbs(list_json=COOLJUGATOR_LIST_JSON):
    dump_utf_json(
        [list(map(lambda v: v.strip(), verb.text.split('-', 1))) for verb in BeautifulSoup(
            requests.get('https://cooljugator.com/gr/list/all').content, 'lxml').find_all('li', {'class': 'item'})],
        list_json
    )


@which_watch
def collect_paradigms(list_json=COOLJUGATOR_LIST_JSON, paradigm_json=COOLJUGATOR_PARADIGM_JSON):
    for verb, translation in load_utf_json(list_json):
        pass


def get_paradigm(verb):
    pass


def get_fieldnames(verb):
    fieldnames = list()
    for cell in BeautifulSoup(
            requests.get('https://cooljugator.com/gr/' + verb).content, 'lxml'
    ).find_all('div', {'class': 'conjugation-cell'}):
        try:
            fieldnames.append(cell.attrs['id'])
        except KeyError:
            pass
    dump_utf_json(fieldnames, 'cooljugator_fieldnames.json')


if __name__ == '__main__':
    # collect_verbs()
    # collect_paradigms()
    get_fieldnames('φτερώνω')
