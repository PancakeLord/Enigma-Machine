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
                    cyclometer.set(base_offsets=[i,j,k],rotor_order=order, ring_settings=[0,0,0])
                    # The polish assumed that only the right rotor turned, meaning they had about a 20/26 chance of cracking the enigma.
                    cycle_dict[get_string(base_offsets=[i,j,k], rotor_order=order)] = cyclometer.get_cycles(only_right=True)

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

# Given rotor settings, find the right plugboard.
def find_plugboard(base_offsets: list, ring_settings:list, rotor_order: list, cycles: tuple, plugboard: Plugboard, unsteckered: list, bad_plugs: list, only_right=False) -> Plugboard:
    cyclometer = Cyclometer(base_offsets=base_offsets,ring_settings=ring_settings,rotor_order=rotor_order, plugboard=plugboard)
    curr_cycles = cyclometer.get_cycles(only_right)
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
                return find_plugboard(base_offsets=base_offsets, ring_settings=ring_settings, rotor_order=rotor_order, cycles=cycles, plugboard=plugboard, unsteckered=unsteckered, bad_plugs=bad_plugs, only_right=only_right)
            unsteckered = unsteckered_copy.copy()
            plugboard = plugboard_copy.copy()
            bad_plugs.append((c, character))
    return None

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


# Given Enigma many enigma messages that contain ANX at the beginning, crack enigma.
def crack_enigma(messages: list) -> dict:
    cycles = Cyclometer.messages_to_cycles(messages)
    possible_enigmas = get_card_catalog()[get_cycle_lengths(cycles)]
    print("Checking these base Enigma machines: " + str(possible_enigmas))
    for enigma in possible_enigmas:
        print(enigma + ":")
        base_offsets = [ord(enigma[i]) - ord('A') for i in range(3)]
        print("base_offsets: " + str(base_offsets))
        rotor_order = ["I" * (ord(enigma[i]) - ord('0')) for i in range(3,6)]
        print("rotor_order: " + str(rotor_order))
        plugboard = find_plugboard(base_offsets=base_offsets, rotor_order=rotor_order, ring_settings=[0,0,0], plugboard=Plugboard(), cycles=cycles, unsteckered=[], bad_plugs=[], only_right=True)
        if plugboard is None:
            print("FAILURE: Wrong Enigma")
            continue
        print("SUCCESS! Plugboard: " + str(plugboard))
        for i in range(Enigma.ALPHABET_LEN):
            for j in range(Enigma.ALPHABET_LEN):
                for k in range(Enigma.ALPHABET_LEN):
                    curr_base_offsets = [base_offsets[0] +k, base_offsets[1]+j,base_offsets[2]+i]
                    curr_base_offsets = [x % Enigma.ALPHABET_LEN for x in curr_base_offsets]
                    ring_settings = [k,j,i]
                    enigma_machine = Enigma(base_offsets=curr_base_offsets, ring_settings=ring_settings, plugboard=plugboard,rotor_order=rotor_order)
                    ind = 0
                    for message in messages:
                        decrypted = enigma_machine.decrypt(message)
                        if decrypted[:3] != "ANX":
                            break
                        if decrypted[:3] == "ANX":
                            ind += 1
                        if ind == 4 or ind == len(messages):
                            return {
                                "base_offsets": curr_base_offsets,
                                "rotor_order": rotor_order,
                                "ring_settings": ring_settings,
                                "plugboard": plugboard,
                            }
    print("FAILURE - No Enigma found :(")
card_catalog = get_card_catalog()
base_offsets=[22,7,3]
plugboard= Plugboard([["R","S"], ["Y","Z"], ["I","A"], ["M","H"]])
rotor_order=["II","I","III"]
ring_settings = [15,6,21]
cyclometer = Cyclometer(base_offsets=base_offsets, ring_settings=ring_settings, plugboard=plugboard, rotor_order=rotor_order)
cycles = cyclometer.get_cycles()
enigma = Enigma(base_offsets=base_offsets, ring_settings=ring_settings, plugboard=plugboard, rotor_order=rotor_order)
messages = [enigma.encrypt("AN HERR HITLER ATTACK AT DAWN", [i,i,i]) for i in range(Enigma.ALPHABET_LEN)]
cracked = crack_enigma(messages)
print(cracked)
