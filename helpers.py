from functools import wraps
import json
import os
import re
import sys
import time

from global_vars import MISSING_WORDS_TXT


def which_watch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def report_time():
            print(f"\n{func.__name__} took {time.strftime('%H:%M:%S', time.gmtime(time.perf_counter() - start))}\n")

        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        except BaseException as e:
            raise e
        else:
            return result
        finally:
            report_time()

    return wrapper


def counter(total=None, every=10):
    count = 0
    if total:
        postfix = " / {}".format(total)
    else:
        postfix = str()
    while True:
        count += 1
        if count == 1 or count == total or not count % every:
            print("\r{}{}".format(count, postfix), end=str(), flush=True)
        yield count


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


def log_missing(word):
    with open(MISSING_WORDS_TXT, 'a') as handler:
        handler.write('{}\n'.format(word))


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
