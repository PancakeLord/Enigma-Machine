import Enigma
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
card_catalog_lengths =  {x: [[len(a) for a in card_catalog[x][i]] for i in range(Enigma.ROTOR_COUNT)] for x in card_catalog.keys()}
def get_possible(cycles: list) -> list:
    cycles_lengths = [[len(a) for a in cycles[i]] for i in range(Enigma.ROTOR_COUNT)]
    relevent_cycles = {x: card_catalog[x] for x in card_catalog_lengths.keys() if card_catalog_lengths[x] == cycles_lengths}
    #print(cycles_lengths)
    #print(len(relevent_cycles))

base_offsets=[20,1,5]
plugboard= Plugboard([["C","A"], ["D", "V"], ["M", "X"], ["N","W"]])
rotor_order=[2,0,1]
cyclometer = Cyclometer(base_offsets=base_offsets, plugboard=plugboard, rotor_order=rotor_order)
cycles = cyclometer.get_cycles()
get_possible(cycles)
enigma = Enigma(base_offsets=base_offsets, plugboard=plugboard, rotor_order=rotor_order)

unique_values = []
for lengths in card_catalog_lengths.values():
    if lengths not in unique_values:
        unique_values.append(lengths)
print(len(unique_values))