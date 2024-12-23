from Enigma import *
from Enigma_Parts import *
from Cyclometer import *
import json
def create_card_catalog():
    permutations = [[0,1,2],[0,2,1],[1,0,2],[2,0,1],[1,2,0],[2,1,0]]
    cyclometer = Cyclometer()
    new_card_catalog = {}
    for i in range(Enigma.ALPHABET_LEN):
        for j in range(Enigma.ALPHABET_LEN):
            for k in range(Enigma.ALPHABET_LEN):
                for order in permutations:
                    cyclometer.set(base_offsets=[i,j,k],rotor_order=order)
                    new_card_catalog[get_string(base_offsets=[i,j,k], rotor_order=order)] = cyclometer.get_cycles()

    with open("card_catalog.json", 'w') as data:
        json.dump(new_card_catalog, data)
def get_card_catalog():
    with open("card_catalog.json", 'r') as data:
        return json.load(data)
card_catalog = get_card_catalog()
card_catalog_lengths =  {x: [[len(a) for a in card_catalog[x][i]] for i in range(3)] for x in card_catalog.keys()}
def get_possible(cycles: list) -> list:
