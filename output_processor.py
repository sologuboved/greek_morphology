from cooljugator_globals import COOLJUGATOR_SLICES


def process_verb_output(res, minimalistic):
    if minimalistic:
        return "{} - {} - {}\n<i>{}</i>".format(*res)
    return "\n\n".join(
        ["<b>{}:</b>\n{}".format(label, ", ".join(res[tense])) for label, tense in COOLJUGATOR_SLICES]
    )


def get_links(word):
    return 'https://www.wordreference.com/gren/{}\n\n' \
           'https://el.wiktionary.org/wiki/{}\n\n' \
           'https://en.wiktionary.org/wiki/{}'.format(*[word] * 3)
