from global_vars import *
from cooljugator_globals import RAW_COOLJUGATOR_PARADIGM_JSON, COOLJUGATOR_PARADIGM_JSON, COOLJUGATOR_FIELDNAMES, \
    FUTURE1, PASTPERFECT1
from helpers import which_watch, read_json_lines, write_json_lines


@which_watch
@write_json_lines
def process_paradigms(final_paradigm_json, raw_paradigm_json=RAW_COOLJUGATOR_PARADIGM_JSON):
    assert final_paradigm_json != raw_paradigm_json, "Unsafe!"
    for line in read_json_lines(raw_paradigm_json):
        yield process_line(line)


def process_line(line):
    return {VERB: line[VERB], TRANSL: line[TRANSL],
            FUTURUM: line[FUTURE1], AORIST: line[PASTPERFECT1],
            PARADIGM: [line[fieldname] for fieldname in COOLJUGATOR_FIELDNAMES]}


if __name__ == '__main__':
    process_paradigms(COOLJUGATOR_PARADIGM_JSON)


