from cooljugator_globals import (
    COOLJUGATOR_FIELDNAMES,
    FUTURE1,
    PASTPERFECT1,
    RAW_COOLJUGATOR_PARADIGM_JSON,
)
from global_vars import AORIST, FUTURUM, PARADIGM, TRANSL, VERB
from helpers import read_json_lines, which_watch, write_json_lines


@which_watch
@write_json_lines
def process_paradigms(final_paradigm_json, raw_paradigm_json=RAW_COOLJUGATOR_PARADIGM_JSON):
    assert final_paradigm_json != raw_paradigm_json, "Unsafe!"
    for line in read_json_lines(raw_paradigm_json):
        yield process_line(line)


def process_line(line):
    return {
        VERB: line[VERB],
        TRANSL: line[TRANSL],
        FUTURUM: "θα {}".format(line[FUTURE1]),
        AORIST: line[PASTPERFECT1],
        PARADIGM: [line[fieldname] if line[fieldname] else None for fieldname in COOLJUGATOR_FIELDNAMES],
    }
