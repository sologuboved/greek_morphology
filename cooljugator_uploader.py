from pymongo import MongoClient
from cooljugator_globals import COOLJUGATOR_PARADIGM_JSON
from global_vars import *
from helpers import which_watch, add_indices, counter, read_json_lines


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


@which_watch
def copy_collection(target_collname, dbname=DB_NAME, source_collname=VERBS, indices=(VERB, PARADIGM)):
    print("[{}]: copying [{}] to [{}]...".format(dbname, source_collname, target_collname))
    assert target_collname != source_collname, "Collections should not have identical names"
    database = MongoClient(LOCALHOST, PORT)[dbname]
    target_coll = database[target_collname]
    target_coll.drop()
    source_coll = database[source_collname]
    count = counter(source_coll.count())
    for entry in source_coll.find():
        next(count)
        target_coll.insert(entry)
    add_indices(target_coll, indices)


if __name__ == '__main__':
    copy_collection(target_collname=VERBS + '_backup')

