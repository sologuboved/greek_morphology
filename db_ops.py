import datetime

from pymongo import MongoClient
from pymongo.errors import OperationFailure

from global_vars import DB_NAME, LOCALHOST, PORT, VERBS
from helpers import counter


def save_entry(coll, entry):
    coll.replace_one({'_id': entry['_id']}, entry)


def copy_collection(db_name, coll_name, postfix='_old', copy_name=None, is_backup=False, indices=()):
    assert coll_name != copy_name, "Source & target collection names are identical"
    assert postfix or copy_name, "Elaborate target collection postfix or name"
    if is_backup:
        target_collname = f'{coll_name}_backup{datetime.datetime.now():%Y%m%d}'
    elif copy_name:
        target_collname = copy_name
    else:
        target_collname = coll_name + postfix
    print("Copying {}.{} to {}.{}...".format(db_name, coll_name, db_name, target_collname))
    d_b = MongoClient(LOCALHOST, PORT)[db_name]
    target_coll = d_b[target_collname]
    target_coll.drop()
    if indices:
        add_indices(target_coll, coll_name, indices=indices)
    d_b.get_collection(coll_name).aggregate([{'$out': target_collname}])
    print('...done')


def add_field(fieldname, fieldcontent, fltr=None, dbname=DB_NAME, collname=VERBS):
    if not fltr:
        fltr = dict()
    print("{}.{}: setting '{}' to \"{}\"...".format(dbname, collname, fieldname, fieldcontent))
    target = MongoClient(LOCALHOST, PORT)[dbname][collname]
    count = counter(target.count_documents(fltr))
    for entry in target.find(fltr):
        next(count)
        entry[fieldname] = fieldcontent
        save_entry(target, entry)
    print()


def edit_field(fieldname, func, fltr=None, dbname=DB_NAME, collname=VERBS):
    if not fltr:
        fltr = dict()
    print("{}.{}: editing '{}' with '{}'...".format(dbname, collname, fieldname, func.__name__))
    target = MongoClient(LOCALHOST, PORT)[dbname][collname]
    count = counter(target.count_documents(fltr))
    for entry in target.find(fltr):
        next(count)
        entry[fieldname] = func(entry.get(fieldname))
        save_entry(target, entry)
    print()


def add_indices(target, coll_name='', indices=(), source=None):
    print("Indexing{}{}...".format(' ' * (coll_name != ''), coll_name))
    if not (source or indices):
        print("No indices to add")
        return
    if source:
        for _, index in source.index_information().items():
            try:
                target.create_index(index['key'])
            except OperationFailure:
                pass
    for indx in indices:
        if isinstance(indx, str):
            target.create_index([(indx, 1)])
        else:
            target.create_index([(fieldname, 1) for fieldname in indx])


def print_verbs(fieldname, fltr, func=None, dbname=DB_NAME, collname=VERBS):
    target = MongoClient(LOCALHOST, PORT)[dbname][collname]
    match = list(target.find(fltr))
    total = target.count_documents(fltr)
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
