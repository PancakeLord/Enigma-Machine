import Enigma
from Enigma import *
from Enigma_Parts import *
from Cyclometer import *
import json
def create_cycle_dict():
    permutations = [["I","II","III"],["I","III","II"],["II","I","III"],["III","I","II"],["II","III","I"],["III","II","I"]]
    cyclometer = Cyclometer()
    cycle_dict = {}
    for i in range(Enigma.ALPHABET_LEN):
        for j in range(Enigma.ALPHABET_LEN):
            for k in range(Enigma.ALPHABET_LEN):
                for order in permutations:
                    cyclometer.set(base_offsets=[i,j,k],rotor_order=order)
                    cycle_dict[get_string(base_offsets=[i,j,k], rotor_order=order)] = cyclometer.get_cycles()

    with open("cycle_dict.json", 'w') as data:
        json.dump(cycle_dict, data)
    return cycle_dict
def get_cycle_dict():
    with open("cycle_dict.json", 'r') as data:
        return json.load(data)

def get_cycle_lengths(cycles: tuple) -> tuple:
    return tuple([tuple([len(a) for a in b]) for b in cycles])
def get_card_catalog():
    cycle_dict = get_cycle_dict()
    card_catalog = {}
    for key in cycle_dict:
        cycle_lengths = get_cycle_lengths(cycle_dict[key])
        if cycle_lengths in card_catalog:
            card_catalog[cycle_lengths].append(key)
        else:
            card_catalog[cycle_lengths] = [key]
    return card_catalog

card_catalog = get_card_catalog()
base_offsets=[17,5,14]
plugboard= Plugboard([["C","A"], ["D", "V"], ["M", "X"], ["N","W"]])
rotor_order=["I","II","III"]
ring_settings = [0,0,1]
cyclometer = Cyclometer(base_offsets=base_offsets, ring_settings=ring_settings, plugboard=plugboard, rotor_order=rotor_order)
cycles = cyclometer.get_cycles()
enigma = Enigma(base_offsets=base_offsets, ring_settings=ring_settings, plugboard=plugboard, rotor_order=rotor_order)
print(card_catalog[get_cycle_lengths(cycles)])
print(enigma.encrypt("", offsets=[8,7,11]))
