from global_vars import NOT_FOUND, MISSING_WORDS_TXT
from cooljugator_globals import COOLJUGATOR_SLICES, FUTURE


def get_verb(res, minimalistic):
    if minimalistic:
        return "{} - {} - {}\n<i>{}</i>".format(*res)
    paradigm = list()
    for label, tense in COOLJUGATOR_SLICES:
        if label == FUTURE:
            forms = map(lambda x: "θα " + x, filter(lambda x: x, res[tense]))
        else:
            forms = filter(lambda x: x, res[tense])
        paradigm.append("<b>{}:</b>\n{}".format(label, ", ".join(forms)))
    return "\n\n".join(paradigm)


def get_missing_words(query):
    try:
        with open(MISSING_WORDS_TXT) as handler:
            lines = handler.readlines()
            try:
                start = int(query)
            except (ValueError, TypeError):
                start = 0
            return ''.join(lines[-start:]).strip()
    except FileNotFoundError:
        return NOT_FOUND
