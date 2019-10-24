import requests
from bs4 import BeautifulSoup
from global_vars import VERB, TRANSL
from cooljugator_globals import COOLJUGATOR_LIST_JSON, RAW_COOLJUGATOR_PARADIGM_JSON, COOLJUGATOR_FIELDNAMES
from helpers import which_watch, dump_utf_json, load_utf_json, counter, write_json_lines


@which_watch
def collect_verbs(list_json=COOLJUGATOR_LIST_JSON):
    dump_utf_json(
        [list(map(lambda v: v.strip(), verb.text.split('-', 1))) for verb in BeautifulSoup(
            requests.get('https://cooljugator.com/gr/list/all').content, 'lxml').find_all('li', {'class': 'item'})],
        list_json
    )


@which_watch
@write_json_lines
def collect_paradigms(raw_paradigm_json, list_json=COOLJUGATOR_LIST_JSON):
    verbs = load_utf_json(list_json)
    exceptions = dict()
    count = counter(len(verbs))
    for verb, transl in verbs:
        next(count)
        paradigm, errors = get_paradigm(verb)
        paradigm.update({VERB: verb, TRANSL: transl})
        if errors:
            exceptions[verb] = errors
        yield paradigm
    if exceptions:
        print('\n\nExceptions:')
        for exception in exceptions:
            print(exception)
            for item in exceptions[exception]:
                print("     {}".format(item))
            print()


def get_paradigm(verb):
    errors = list()
    paradigm = {fieldname: str() for fieldname in COOLJUGATOR_FIELDNAMES}
    verb = BeautifulSoup(requests.get('https://cooljugator.com/gr/' + verb).content, 'lxml')
    for fieldname in paradigm:
        try:
            paradigm[fieldname] = verb.find('div', {'class': 'conjugation-cell', 'id': fieldname}).attrs['data-default']
        except AttributeError:
            pass
        except Exception as e:
            errors.append((fieldname, type(e), str(e)))
    return paradigm, errors


@which_watch
def get_fieldnames(list_json=COOLJUGATOR_LIST_JSON, fieldnames_json='cooljugator_fieldnames.json'):
    fieldnames = set()
    verbs = load_utf_json(list_json)
    count = counter(len(verbs))
    for verb, _ in verbs:
        next(count)
        for cell in BeautifulSoup(
                requests.get('https://cooljugator.com/gr/' + verb).content, 'lxml'
        ).find_all('div', {'class': 'conjugation-cell'}):
            try:
                fieldnames.add(cell.attrs['id'])
            except KeyError:
                pass
    dump_utf_json(sorted(list(fieldnames)), fieldnames_json)


if __name__ == '__main__':
    from helpers import write_pid, delete_pid
    pid_fname = write_pid()
    collect_paradigms(RAW_COOLJUGATOR_PARADIGM_JSON)
    delete_pid(pid_fname)
    # collect_verbs()
    # get_fieldnames()
    # p, err = get_paradigm('είμαι')
    # for i in p:
    #     print(i, "      ", p[i])
