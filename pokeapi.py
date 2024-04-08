import requests
import sys
import os.path
import json 

POKEDEX_ID = 30
PLA_VERSION_NAME = "legends-arceus"
SPANISH_CODE = 'es'


def generate_dex():
    URL_LIST = "https://pokeapi.co/api/v2/pokedex/{}".format(POKEDEX_ID)
    pokemon_list = {}

    res = requests.get(URL_LIST)
    data = res.json()
    for entry in data['pokemon_entries']:
        pokemon = entry['pokemon_species']['name']
        # get_sprite(pokemon)
        details = get_pokemon_details(pokemon)
        pokemon_list[pokemon] = {
            "name": pokemon,
            "description": get_description(details),
            "title": get_title(details)
        }
        with open('data.json', 'w') as fp:
            json.dump(pokemon_list, fp)


def get_sprite(pokemon):
    # check file before trying to download
    if not os.path.isfile("{}.png".format(pokemon)):
        print('Request Pokemon {} from PokeAPI'.format(pokemon))
        res = requests.get("https://pokeapi.co/api/v2/pokemon/{}".format(pokemon))

        if res.status_code == 404:
            print("{} was not found".format(pokemon))
            return

        data = res.json()
        print('Getting sprite...')
        img_data = requests.get(data['sprites']['other']['official-artwork']['front_default']).content
        with open("{}.png".format(pokemon), "wb") as handler:
            handler.write(img_data)
    else:
        print("Image already exists, skipping {}".format(pokemon))


def get_pokemon_details(pokemon):
    print('Request Pokemon {} detail from PokeAPI'.format(pokemon))
    res = requests.get("https://pokeapi.co/api/v2/pokemon-species/{}".format(pokemon))
    data = res.json()
    return data


def get_description(data):
    for entry in data['flavor_text_entries']:
        if entry['version']['name'] == PLA_VERSION_NAME:
            return entry['flavor_text']            

    return ''


def get_title(data):
    for entry in data['genera']:
        if entry['language']['name'] == SPANISH_CODE:
            return entry['genus']

    return ''

if __name__ == '__main__':
    generate_dex()
