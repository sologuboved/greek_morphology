from pymongo import MongoClient

from db_ops import add_indices
from global_vars import DB_NAME, LOCALHOST, PARADIGM, PORT, SOURCE, VERB, VERBS
from helpers import counter, read_json_lines, which_watch


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
        target.insert_one(line)
    add_indices(target, coll_name, indices)
    print('\nCurrently,', target.estimated_document_count(), 'entries')
