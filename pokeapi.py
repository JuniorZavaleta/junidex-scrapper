import requests
import sys

def get_sprite(pokemon):    
    res = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon)
    data = res.json()
    img_data = requests.get(data['sprites']['other']['official-artwork']['front_default']).content
    with open("{}.png".format(pokemon), "wb") as handler:
        handler.write(img_data)

if __name__ == '__main__':
    get_sprite(sys.argv[1].lower())