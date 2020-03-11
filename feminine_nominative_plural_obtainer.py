import requests
from bs4 import BeautifulSoup


def obtain_fem_nom_pl(noun):
    if noun.endswith('η') or noun.endswith('ή'):
        try:
            return BeautifulSoup(
                requests.get('https://el.wiktionary.org/wiki/' + noun).content, 'lxml'
            ).find_all('td', align='left')[1].find('a').get('title').strip()
        except (IndexError, AttributeError):
            return


if __name__ == '__main__':
    print(obtain_fem_nom_pl('επιτροπή'))

