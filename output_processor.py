from global_vars import NOT_FOUND, MISSING_WORDS_TXT, VERB, AORIST, FUTURUM, TRANSL, PARADIGM
from cooljugator_globals import COOLJUGATOR_SLICES, FUTURE


def get_verb(res, minimalistic, appendix=False):
    def process_sequence(raw_seq):
        seq = list()
        for item in raw_seq:
            if isinstance(item, list):
                seq.append(" / ".join(item))
            else:
                seq.append(item)
        return seq

    def get_minimalistic():
        if appendix:
            separator = " | "
            newline = '\n\n'
        else:
            separator = '\n'
            newline = str()
        verb, aorist, futurum, transl = process_sequence([res[VERB], res[AORIST], res[FUTURUM], res[TRANSL]])
        return "{}{} - {} - {}{}<i>{}</i>".format(newline, verb, aorist, futurum, separator, transl)

    def get_tense():
        return process_sequence(filter(lambda x: x, res[tense]))

    if minimalistic:
        return get_minimalistic()

    res = res[PARADIGM]
    if not res:
        return "Paradigm is missing\n\n{}".format(get_minimalistic())
    paradigm = list()
    for label, tense in COOLJUGATOR_SLICES:
        if label == FUTURE:
            forms = map(lambda x: "θα " + x, get_tense())
        else:
            forms = get_tense()
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


def get_fem_nom_pl(res):
    if res is None:
        return str()
    else:
        return "\n\n<i>Nominativus pluralis:</i> " + res
