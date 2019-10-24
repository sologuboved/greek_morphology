from global_vars import DIACRITICS, DIACRITICALS


def guess_stress(verb):
    for diacritical in DIACRITICALS:
        if diacritical in verb:
            return [verb]
    conjectures = list()
    for indx in range(len(verb)):
        char = verb[indx]
        if char in DIACRITICS:
            for diacritical in DIACRITICS[char]:
                conjecture = verb[:indx] + diacritical
                try:
                    conjecture += verb[indx + 1:]
                except IndexError:
                    pass
                conjectures.append(conjecture)
    return conjectures


if __name__ == '__main__':
    for v in ('αγοραζομαι', 'αγυρντιζω', 'εντυπωσιάζομαι', 'ηχογραφω'):
        res = guess_stress(v)
        for r in res:
            print(r)
        print()

