from pymongo import MongoClient
from global_vars import DB_NAME, VERBS, VERB, PARADIGM, SOURCE, LOCALHOST, PORT
from helpers import which_watch, counter, read_json_lines
from coll_operations import add_indices


@which_watch
def upload(source_json, source, db_name=DB_NAME, coll_name=VERBS, drop=False, indices=(VERB, PARADIGM)):
    target = MongoClient(LOCALHOST, PORT)[db_name][coll_name]
    if drop:
        target.drop()
    print('Initially,', target.count(), 'entries')
    count = counter()
    for line in read_json_lines(source_json):
        next(count)
        line[SOURCE] = source
        target.insert(line)
    add_indices(target, indices)
    print('\nCurrently,', target.count(), 'entries')


if __name__ == '__main__':
    # from cooljugator_globals import COOLJUGATOR_PARADIGM_JSON
    # upload(COOLJUGATOR_PARADIGM_JSON, 'c', drop=True)

    from global_vars import WIKILEXICO_VERBS
    from wikilexico_globals import WIKILEXICO_PARADIGM_JSON
    upload(WIKILEXICO_PARADIGM_JSON, 'w', coll_name=WIKILEXICO_VERBS, drop=True)
