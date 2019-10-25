from global_vars import NOT_FOUND, MISSING_WORDS_TXT
from cooljugator_globals import COOLJUGATOR_SLICES


def get_verb(res, minimalistic):
    if minimalistic:
        return "{} - {} - {}\n<i>{}</i>".format(*res)
    return "\n\n".join(
        ["<b>{}:</b>\n{}".format(label, ", ".join(res[tense])) for label, tense in COOLJUGATOR_SLICES]
    )


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
