from Enigma import *
from card_catalog import *

class Cyclometer:
    def __init__(self, base_offsets = [0]*Enigma.ROTOR_COUNT, rotor_order = list(range(Enigma.ROTOR_COUNT))):
        self.set(base_offsets, rotor_order)
    def set(self, base_offsets: list, rotor_order: list) -> None:
        self.enigma = Enigma(base_offsets=base_offsets.copy(), rotor_order=rotor_order.copy())

    def get_cycles(self) -> list:
        AD = {}
        BE = {}
        CF = {}
        for i in range(Enigma.ALPHABET_LEN):
            message = self.enigma.encrypt("",[i,i,i])
            AD[message[0]] = message[3]
            BE[message[1]] = message[4]
            CF[message[2]] = message[5]
        cycle_dicts = [AD,BE,CF]
        cycles = [[],[],[]]
        for i in range(3):
            alphabet = [chr(x) for x in range(ord(Enigma.MIN_LETTER), ord(Enigma.MAX_LETTER)+1)]
            cycle_num = 0
            while len(alphabet) != 0:
                cycles[i].append([])
                start = alphabet[0]
                curr = start
                ind = 0
                while curr != start or ind == 0:
                    alphabet.remove(curr)
                    cycles[i][cycle_num].append(curr)
                    curr = cycle_dicts[i][curr]
                    ind += 1
                cycle_num += 1
        return cycles
def get_string(base_offsets, rotor_order):
    ans = ""
    for x in base_offsets:
        ans += chr(x+ord(Enigma.MIN_LETTER))
    for x in rotor_order:
        ans += str(x)
    return ans

permutations = [[0,1,2],[0,2,1],[1,0,2],[2,0,1],[1,2,0],[2,1,0]]
cyclometer = Cyclometer()
# card_catalog = {}
# for i in range(Enigma.ALPHABET_LEN):
#     for j in range(Enigma.ALPHABET_LEN):
#         for k in range(Enigma.ALPHABET_LEN):
#             for order in permutations:
#                 cyclometer.set(base_offsets=[i,j,k],rotor_order=order)
#                 card_catalog[get_string(base_offsets=[i,j,k], rotor_order=order)] = cyclometer.get_cycles()
#
# with open("card_catalog.py", 'w') as data:
#     data.write("card_catalog = " + str(card_catalog))
card_catalog_lengths =  {x: [[len(a) for a in card_catalog[x][i]] for i in range(3)] for x in card_catalog.keys()}
print(card_catalog_lengths)