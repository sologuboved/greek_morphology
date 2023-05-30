from cooljugator_globals import COOLJUGATOR_SLICES, FUTURE
from global_vars import AORIST, FUTURUM, PARADIGM, TRANSL, VERB, WORDREF_LINK


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
        if not transl:
            separator = str()
        return "{}<a href='{}'>{}</a> - {} - {}{}<i>{}</i>".format(
            newline, WORDREF_LINK.format(word=verb),
            verb,
            aorist,
            futurum,
            separator,
            transl,
        )

    def get_tense():
        return process_sequence(filter(lambda x: x, res[tense]))

    if minimalistic:
        return get_minimalistic()

    res = res[PARADIGM]
    if not res:
        return f"Paradigm is missing\n\n{get_minimalistic()}"
    paradigm = list()
    for label, tense in COOLJUGATOR_SLICES:
        if label == FUTURE:
            forms = map(lambda x: "θα " + x, get_tense())
        else:
            forms = get_tense()
        paradigm.append(f"<b>{label}:</b>\n{', '.join(forms)}")
    return "\n\n".join(paradigm)


def get_fem_nom_pl(res):
    if res is None:
        return str()
    else:
        return "\n\n<i>Nominativus pluralis:</i> " + res
