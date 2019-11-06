from pymongo import MongoClient
from cooljugator_globals import COOLJUGATOR_PARADIGM_JSON
from global_vars import *
from helpers import which_watch, counter, read_json_lines
from coll_operations import add_indices


@which_watch
def upload(db_name=DB_NAME, coll_name=VERBS,
           drop=False, source_json=COOLJUGATOR_PARADIGM_JSON, indices=(VERB, PARADIGM)):
    target = MongoClient(LOCALHOST, PORT)[db_name][coll_name]
    if drop:
        target.drop()
    print('Initially,', target.count(), 'entries')
    count = counter('?')
    for line in read_json_lines(source_json):
        next(count)
        target.insert(line)
    add_indices(target, indices)
    print('\nCurrently,', target.count(), 'entries')


if __name__ == '__main__':
    upload(drop=True)
