from pymongo import MongoClient, ASCENDING
from global_vars import *
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


def edit_field(fieldname, func, fltr=None, dbname=DB_NAME, collname=VERBS):
    if not fltr:
        fltr = dict()
    print("{}.{}: editing '{}' with '{}'...".format(dbname, collname, fieldname, func.__name__))
    target = MongoClient(LOCALHOST, PORT)[dbname][collname]
    cursor = target.find(fltr)
    count = counter(cursor.count())
    for entry in cursor:
        next(count)
        entry[fieldname] = func(entry.get(fieldname))
        target.save(entry)
    print()


def add_indices(target, indices):
    print("\nIndexing...")
    for indx in indices:
        if type(indx) is tuple:
            target.create_index([(fieldname, ASCENDING) for fieldname in indx])
        else:
            target.create_index([(indx, ASCENDING)])


def print_verbs(fieldname, fltr, func=None, dbname=DB_NAME, collname=VERBS):
    match = MongoClient(LOCALHOST, PORT)[dbname][collname].find(fltr)
    total = match.count()
    if func:
        res = list()
        count = counter(total)
        for entry in match:
            next(count)
            if func(entry):
                res.append(entry[fieldname])
        print("\n{} matching items".format(len(res)))
    else:
        print(total, "matching entries")
        res = [entry[fieldname] for entry in match]
    for item in res:
        print(item)


def stringify(fieldcontent):
    if isinstance(fieldcontent, str):
        return fieldcontent
    else:
        return " / ".join(fieldcontent)


def is_abnormal_verb(entry):
    verb = stringify(entry[VERB])
    return not (verb.endswith('ω') or verb.endswith('ώ') or verb.endswith('αι'))


if __name__ == '__main__':
    # from global_vars import SOURCE, WIKILEXICO_ACT_VERBS
    # add_field(SOURCE, 'w', collname=WIKILEXICO_ACT_VERBS)
    # from global_vars import FUTURUM
    # edit_field(FUTURUM, lambda x: "θα " + x if x else x)
    # copy_collection(target_collname=VERBS + '_backup')
    # from global_vars import TRANSL, WIKILEXICO_ACT_VERBS
    # edit_field(TRANSL, lambda x: str(), collname=WIKILEXICO_ACT_VERBS)
    print_verbs(VERB, {SOURCE: 'c'}, is_abnormal_verb)
    ...
