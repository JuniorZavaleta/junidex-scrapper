import requests

from bs4 import BeautifulSoup


class NotPokemonException(Exception):
    pass


# Get Names
r = requests.get('https://pokemon.fandom.com/es/wiki/Lista_de_Pok%C3%A9mon')
soup = BeautifulSoup(r.text, 'lxml')

names = set()
raw_tds = soup.select('.tabpokemon tbody td a')
for raw_td in raw_tds:
    try:
        name = raw_td['href'].split('/')[-1]
        if 'Tipo' in name or 'Especial' in name or '#' in name:
            raise NotPokemonException

        names.add(name)
    except KeyError:
        print(raw_td)
    except NotPokemonException:
        print("No es un pokemon xd")

print("Pokemon encontrados: {}".format(len(names)))

for name in names:
    r = requests.get('https://pokemon.fandom.com/es/wiki/{}'.format(name))
    soup = BeautifulSoup(r.text, 'lxml')

    try:
        sprite3D = soup.select('table.galeria-sprites.cmod3D a img', limit=1)[0]

        img_src = sprite3D['data-src']
        print("Downloading: {}".format(img_src))

        img_data = requests.get(img_src).content
        with open("{}.gif".format(name), 'wb') as handler:
            handler.write(img_data)
    except Exception as e:
        print(e)
        print(name + " no encontrado en 3D chevere")
