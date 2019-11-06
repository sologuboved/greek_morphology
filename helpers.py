import time
import json
import os
import sys
import re
from functools import wraps
from pymongo import MongoClient, ASCENDING
from global_vars import MISSING_WORDS_TXT, DB_NAME, VERBS, LOCALHOST, PORT, VERB, PARADIGM, SOURCE


def which_watch(func):

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(func.__name__, 'took', time.strftime("%H:%M:%S", time.gmtime(time.perf_counter() - start)))
        print()
        return result

    return wrapper


def counter(total='?'):
    count = 0
    while True:
        count += 1
        print("\r{} / {}".format(count, total), end=str(), flush=True)
        yield


def load_utf_json(json_file):
    with open(json_file, encoding='utf8') as data:
        return json.load(data)


def dump_utf_json(entries, json_file):
    with open(json_file, 'w', encoding='utf-8') as handler:
        json.dump(entries, handler, ensure_ascii=False, sort_keys=True, indent=2)


def write_json_lines(func):

    @wraps(func)
    def wrapper(json_filename, *args, **kwargs):
        count = 0
        with open(json_filename, 'w', encoding='utf-8') as handler:
            for entry in func(json_filename, *args, **kwargs):
                count += 1
                json.dump(entry, handler, ensure_ascii=False)
                handler.write('\n')
                print("\r{}".format(count), end='', flush=True)
        print("\nTotal: {} entries".format(count))

    return wrapper


def read_json_lines(json_fname):
    with open(json_fname, 'r') as handler:
        for line in handler:
            yield json.loads(line)


def add_indices(target, indices):
    print("\nIndexing...")
    for indx in indices:
        if type(indx) is tuple:
            target.create_index([(fieldname, ASCENDING) for fieldname in indx])
        else:
            target.create_index([(indx, ASCENDING)])


def log_missing(word):
    with open(MISSING_WORDS_TXT, 'a') as handler:
        handler.write('{}\n'.format(word))


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


def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_abs_path(fname):
    return os.path.join(get_base_dir(), fname)


def write_pid():
    prefix = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    previous_pid = find_previous_pid(prefix)
    if previous_pid:
        print("\nRemoving {}...".format(previous_pid))
        os.remove(previous_pid)
    pid_fname = get_abs_path('{}_{}.pid'.format(prefix, str(os.getpid())))
    print("Writing {}\n".format(pid_fname))
    with open(pid_fname, 'w') as handler:
        handler.write(str())
    return pid_fname


def delete_pid(pid_fname):
    try:
        os.remove(pid_fname)
    except FileNotFoundError as e:
        print(str(e))


def find_previous_pid(prefix):
    for fname in os.listdir(get_base_dir()):
        if re.fullmatch(r'{}_\d+\.pid'.format(prefix), fname):
            return get_abs_path(fname)


if __name__ == '__main__':
    add_field(SOURCE, 'c')
    copy_collection(target_collname=VERBS + '_backup')
