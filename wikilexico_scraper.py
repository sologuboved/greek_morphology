import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from wikilexico_globals import UNFILTERED_WIKILEXICO_LIST_JSON, FILTERED_WIKILEXICO_LIST_JSON
from global_vars import LOCALHOST, PORT, DB_NAME, VERBS, VERB
from helpers import which_watch, counter, write_json_lines, read_json_lines


@which_watch
@write_json_lines
def collect_verbs(unfiltered_list_json):
    page_url = 'https://el.wiktionary.org/w/index.php?title=%CE%9A%CE%B1%CF%84%CE%B7%CE%B3%CE%BF%CF%81%CE%AF%CE%B1:' \
               '%CE%A1%CE%AE%CE%BC%CE%B1%CF%84%CE%B1_(%CE%BD%CE%AD%CE%B1_%CE%B5%CE%BB%CE%BB%CE%B7%CE%BD%CE%B9%CE%BA' \
               '%CE%AC)&from=%CE%B1#mw-pages'
    count = counter()
    while True:
        soup = BeautifulSoup(requests.get(page_url).content, 'lxml')
        for a_tag in soup.find_all('a', href=True):
            a_text = a_tag.text
            if a_tag.get('title') == a_text:
                next(count)
                yield a_text
        try:
            page_url = 'https://el.wiktionary.org' + soup.find('a', href=True, text="επόμενη σελίδα")['href']
        except TypeError:
            break


@which_watch
@write_json_lines
def filter_verbs(filtered_list_json, unfiltered_list_json=UNFILTERED_WIKILEXICO_LIST_JSON):
    count = counter()
    coll = MongoClient(LOCALHOST, PORT)[DB_NAME][VERBS]
    for verb in read_json_lines(unfiltered_list_json):
        next(count)
        if not coll.find({VERB: verb}).count():
            yield verb


if __name__ == '__main__':
    # collect_verbs(UNFILTERED_WIKILEXICO_LIST_JSON)
    filter_verbs(FILTERED_WIKILEXICO_LIST_JSON)
