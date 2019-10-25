from global_vars import *
from cooljugator_globals import *


def process_verb_output(res, minimalistic):
    if minimalistic:
        return "{} - {} - {} ({})".format(*res)


def get_links(word):
    return 'https://www.wordreference.com/gren/{}\n\n' \
           'https://el.wiktionary.org/wiki/{}\n\n' \
           'https://en.wiktionary.org/wiki/{}'.format(*[word] * 3)
