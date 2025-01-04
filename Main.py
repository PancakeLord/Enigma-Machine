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

def find_plugboard(base_offsets: list, ring_settings: list, rotor_order: list, cycles: tuple, plugboard=Plugboard(), unsteckered = [], bad_plugs=[]) -> Plugboard:
    cyclometer = Cyclometer(base_offsets=base_offsets,ring_settings=ring_settings,rotor_order=rotor_order, plugboard=plugboard)
    curr_cycles = cyclometer.get_cycles()
    if curr_cycles == cycles:
        return plugboard
    useful_cycles = [[cycle for cycle in cycles[i] if (len([c for c in cycle if (c in plugboard or c in unsteckered)]) == 0)] for i in range(len(cycles))]
    curr_useful_cycles = [[cycle for cycle in curr_cycles[i] if (len([c for c in cycle if (c in plugboard or c in unsteckered)]) == 0)] for i in range(len(curr_cycles))]
    cycle_lengths = []
    for i in range(len(curr_useful_cycles)):
        for cycle in curr_useful_cycles[i]:
            cycle_lengths.append((len(cycle), i, cycle))

    cycle_lengths.sort(key=lambda x: (x[0], x[1]))

    cycle = cycle_lengths[0][2]
    c = cycle[0]
    permutation_ind = cycle_lengths[0][1]
    unsteckered_copy = unsteckered.copy()
    plugboard_copy = plugboard.copy()
    for cycle in useful_cycles[permutation_ind]:
        if len(cycle) != cycle_lengths[0][0]:
            continue
        for character in cycle:
            if add_to_plugboard(c1=c, c2=character, cycles=cycles, curr_cycles=curr_cycles, unsteckered=unsteckered, plugboard=plugboard, bad_plugs=bad_plugs):
                return find_plugboard(base_offsets=base_offsets, ring_settings=ring_settings, rotor_order=rotor_order, cycles=cycles, plugboard=plugboard, unsteckered=unsteckered, bad_plugs=bad_plugs)
            unsteckered = unsteckered_copy.copy()
            plugboard = plugboard_copy.copy()
            bad_plugs.append((c, character))
    return plugboard

def add_to_plugboard(c1: chr, c2: chr, cycles: tuple, curr_cycles: tuple, unsteckered: list, plugboard: Plugboard, bad_plugs: list):
    if (c1,c2) in bad_plugs or (c2,c1) in bad_plugs:
        return False
    if (c1 in plugboard and plugboard[c1] != c2) or (c2 in plugboard and plugboard[c2] != c1) or (c1 == c2 and c1 in plugboard):
        return False
    if (c1 == c2 and c1 in unsteckered) or (c1 in plugboard and plugboard[c1] == c2):
        return True
    bool = True
    if c1 == c2:
        unsteckered.append(c1)
    else:
        plugboard.add(c1,c2)
    for cycle, curr_cycle in zip(cycles, curr_cycles):
        bool = bool and add_to_plugboard(c1=apply_cycle(cycle, c1), c2=apply_cycle(curr_cycle, c2), cycles=cycles, curr_cycles=curr_cycles, unsteckered=unsteckered, plugboard=plugboard, bad_plugs=bad_plugs)
        bool = bool and add_to_plugboard(c1=apply_cycle(cycle, c2), c2=apply_cycle(curr_cycle, c1), cycles=cycles, curr_cycles=curr_cycles, unsteckered=unsteckered, plugboard=plugboard, bad_plugs=bad_plugs)
    return bool
def apply_cycle(permutation: tuple, char: chr) -> chr:
    cycle = [c for c in permutation if char in c]
    if len(cycle) == 0:
        return char
    return cycle[0][(cycle[0].index(char)+1) % len(cycle[0])]
card_catalog = get_card_catalog()
base_offsets=[17,5,13]
plugboard= Plugboard([["C","A"], ["D", "V"], ["M", "X"]])
rotor_order=["I","II","III"]
ring_settings = [0,0,0]
cyclometer = Cyclometer(base_offsets=base_offsets, ring_settings=ring_settings, plugboard=plugboard, rotor_order=rotor_order)
cycles = cyclometer.get_cycles()
enigma = Enigma(base_offsets=base_offsets, ring_settings=ring_settings, plugboard=plugboard, rotor_order=rotor_order)
print(find_plugboard(base_offsets=base_offsets, ring_settings=ring_settings, rotor_order=rotor_order, cycles=cycles))