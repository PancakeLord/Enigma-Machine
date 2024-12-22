from Enigma import *


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


cyclometer = Cyclometer()
print(cyclometer.get_cycles())