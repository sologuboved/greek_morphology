COOLJUGATOR_LIST_JSON = 'cooljugator_list.json'
RAW_COOLJUGATOR_PARADIGM_JSON = 'cooljugator_paradigm_raw.json'
COOLJUGATOR_PARADIGM_JSON = 'cooljugator_paradigm.json'
COOLJUGATOR_DO_TRANSL = 'cooljugator_do_transl.json'

INFINITIVE0 = 'infinitive0'
COMMANDIMPERFECT2 = 'commandimperfect2'
COMMANDIMPERFECT4 = 'commandimperfect4'
COMMANDPERFECT2 = 'commandperfect2'
COMMANDPERFECT4 = 'commandperfect4'
FUTURE1 = 'future1'
FUTURE2 = 'future2'
FUTURE3 = 'future3'
FUTURE4 = 'future4'
FUTURE5 = 'future5'
FUTURE6 = 'future6'
PASTIMPERFECT1 = 'pastimperfect1'
PASTIMPERFECT2 = 'pastimperfect2'
PASTIMPERFECT3 = 'pastimperfect3'
PASTIMPERFECT4 = 'pastimperfect4'
PASTIMPERFECT5 = 'pastimperfect5'
PASTIMPERFECT6 = 'pastimperfect6'
PASTPERFECT1 = 'pastperfect1'
PASTPERFECT2 = 'pastperfect2'
PASTPERFECT3 = 'pastperfect3'
PASTPERFECT4 = 'pastperfect4'
PASTPERFECT5 = 'pastperfect5'
PASTPERFECT6 = 'pastperfect6'
PRESENT2 = 'present2'
PRESENT3 = 'present3'
PRESENT4 = 'present4'
PRESENT5 = 'present5'
PRESENT6 = 'present6'

COOLJUGATOR_FIELDNAMES = [
    INFINITIVE0,
    PRESENT2, PRESENT3, PRESENT4, PRESENT5, PRESENT6,
    FUTURE1, FUTURE2, FUTURE3, FUTURE4, FUTURE5, FUTURE6,
    PASTPERFECT1, PASTPERFECT2, PASTPERFECT3, PASTPERFECT4, PASTPERFECT5, PASTPERFECT6,
    PASTIMPERFECT1, PASTIMPERFECT2, PASTIMPERFECT3, PASTIMPERFECT4, PASTIMPERFECT5, PASTIMPERFECT6,
    COMMANDIMPERFECT2, COMMANDIMPERFECT4, COMMANDPERFECT2, COMMANDPERFECT4
]

FUTURE = 'future'

COOLJUGATOR_SLICES = (
    ('Present', slice(0, 6)),
    (FUTURE, slice(6, 12)),
    ('Aorist', slice(12, 18)),
    ('Imperfect', slice(18, 24)),
    ("Imperfective Imperative", slice(24, 26)),
    ('Perfective Imperative', slice(26, 28))
)
