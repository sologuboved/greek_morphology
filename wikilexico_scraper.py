import itertools
import re

from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests

from global_vars import LOCALHOST, PORT, DB_NAME, VERBS, VERB, FUTURUM, AORIST, PARADIGM, TRANSL
from helpers import which_watch, counter, write_json_lines, read_json_lines
from wikilexico_globals import UNFILTERED_WIKILEXICO_LIST_JSON, FILTERED_WIKILEXICO_LIST_JSON, WIKILEXICO_PARADIGM_JSON


@which_watch
@write_json_lines
def collect_verbs(unfiltered_list_json):
    print("Collecting verbs to", unfiltered_list_json)
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
    print()


@which_watch
@write_json_lines
def filter_verbs(filtered_list_json, unfiltered_list_json=UNFILTERED_WIKILEXICO_LIST_JSON):
    print("Filtering {} --> {}".format(unfiltered_list_json, filtered_list_json))
    count = counter()
    coll = MongoClient(LOCALHOST, PORT)[DB_NAME][VERBS]
    for verb in read_json_lines(unfiltered_list_json):
        next(count)
        if not coll.find({VERB: verb}).count():
            yield verb
    print()


@which_watch
@write_json_lines
def collect_active_voice_paradigms(raw_paradigm_json, list_json=FILTERED_WIKILEXICO_LIST_JSON):
    count = counter()
    for verb in read_json_lines(list_json):
        next(count)
        try:
            paradigm = get_paradigm(verb, active_voice=True)
        except Exception as e:
            print()
            print(verb)
            print()
            raise e
        if paradigm:
            entry = get_shortened(paradigm)
            entry[PARADIGM] = paradigm
            yield entry


def get_paradigm(verb, active_voice):

    def get_columns():
        return rows[index].find_all('td')

    def de_br(cell):
        try:
            return br_pat.findall(str(cell))[0]
        except IndexError:
            return de_bracket(cell)

    def de_bracket(cell):
        splitted = list(map(str.strip, cell.text.split('(')[0].split(" - ")))
        if len(splitted) == 1:
            return splitted[0]
        else:
            return splitted

    br_pat = re.compile('<td>(.+?)<')
    present = list()
    raw_future = list()
    aorist = list()
    imperfect = list()
    imperative = list()

    rows = get_rows(verb, active_voice)
    if not rows:
        return

    for index in range(2, 7):
        columns = get_columns()
        present.append(de_bracket(columns[1]))
        imperfect.append(de_bracket(columns[2]))
        imperative.append(de_bracket(columns[5]))

    index = 7
    pers3_pl = get_columns()
    present.append(de_bracket(pers3_pl[1]))
    imperfect.append(de_br(pers3_pl[2]))

    index = 10
    columns = get_columns()
    aorist.append(de_bracket(columns[2]))
    raw_future.append(de_bracket(columns[3]))

    for index in range(11, 15):
        columns = get_columns()
        aorist.append(de_bracket(columns[1]))
        raw_future.append(de_bracket(columns[2]))
        imperative.append(de_bracket(columns[4]))

    index = 15
    pers3_pl = get_columns()
    aorist.append(de_br(pers3_pl[1]))
    raw_future.append(de_bracket(pers3_pl[2]))

    return list(itertools.chain(present,
                                fix_future(raw_future),
                                aorist,
                                imperfect,
                                list(filter(lambda v: v, imperative))))


# def get_active_voice_rows(verb):
#     verb = BeautifulSoup(requests.get('https://el.wiktionary.org/wiki/' + verb).content, 'lxml')
#     if not verb.find('span', {'class': 'inflexions'}):
#         return
#     for table in verb.find_all('tbody'):
#         try:
#             first_header = table.find('center').text.strip()
#         except AttributeError:
#             continue
#         if first_header == "Εξακολουθητικοί χρόνοι":
#             return table.find_all('tr')


def get_rows(verb, active_voice):
    verb = BeautifulSoup(requests.get('https://el.wiktionary.org/wiki/' + verb).content, 'lxml')
    if not verb.find('span', {'class': 'inflexions'}):
        return
    omitted_active = False
    for table in verb.find_all('tbody'):
        try:
            first_header = table.find('center').text.strip()
        except AttributeError:
            continue
        if first_header == "Εξακολουθητικοί χρόνοι":
            if omitted_active or active_voice:
                return table.find_all('tr')
            else:
                omitted_active = True
                continue


def fix_future(raw_future):
    future = list()
    for item in raw_future:
        if isinstance(item, str):
            future.append(item.split()[-1])
        else:
            future.append(fix_future(item))
    return future


def get_shortened(paradigm):
    return {VERB: paradigm[0], FUTURUM: "θα {}".format(paradigm[6]), AORIST: paradigm[12], TRANSL: str()}


if __name__ == '__main__':
    # collect_verbs(UNFILTERED_WIKILEXICO_LIST_JSON)
    # filter_verbs(FILTERED_WIKILEXICO_LIST_JSON)
    # collect_active_voice_paradigms(WIKILEXICO_PARADIGM_JSON)
    # print(get_active_voice_paradigm('αγανοϋφαίνω'))
    # get_active_voice_rows('αγανοϋφαίνω')
    print(get_paradigm('αερίζω', False))
