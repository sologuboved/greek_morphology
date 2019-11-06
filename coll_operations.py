from pymongo import MongoClient, ASCENDING
from global_vars import DB_NAME, VERBS, LOCALHOST, PORT, VERB, PARADIGM, SOURCE
from helpers import counter


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


def add_field(fieldname, fieldcontent, fltr=None, dbname=DB_NAME, collname=VERBS):
    if not fltr:
        fltr = dict()
    print("{}.{}: setting '{}' to \"{}\"...".format(dbname, collname, fieldname, fieldcontent))
    target = MongoClient(LOCALHOST, PORT)[dbname][collname]
    cursor = target.find(fltr)
    count = counter(cursor.count())
    for entry in cursor:
        next(count)
        entry[fieldname] = fieldcontent
        target.save(entry)
    print()


def add_indices(target, indices):
    print("\nIndexing...")
    for indx in indices:
        if type(indx) is tuple:
            target.create_index([(fieldname, ASCENDING) for fieldname in indx])
        else:
            target.create_index([(indx, ASCENDING)])


if __name__ == '__main__':
    add_field(SOURCE, 'c')
    copy_collection(target_collname=VERBS + '_backup')