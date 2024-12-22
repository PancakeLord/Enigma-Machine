from Enigma import *


class Cyclometer:
    def __init__(self, base_offsets = [0]*Enigma.ROTOR_COUNT, rotor_order = list(range(Enigma.ROTOR_COUNT))):
        self.set(base_offsets, rotor_order)
    def set(self, base_offsets: list, rotor_order: list) -> None:
        self.enigma = Enigma(base_offsets=base_offsets.copy(), rotor_order=rotor_order.copy())

    def get_cycles(self) -> list:
        AD = {chr(x):chr(x) for x in range(ord(Enigma.MIN_LETTER), ord(Enigma.MAX_LETTER)+1)}
        BE = {chr(x):chr(x) for x in range(ord(Enigma.MIN_LETTER), ord(Enigma.MAX_LETTER)+1)}
        CF = {chr(x):chr(x) for x in range(ord(Enigma.MIN_LETTER), ord(Enigma.MAX_LETTER)+1)}
        for i in range(Enigma.ALPHABET_LEN):
            message = self.enigma.encrypt("",[i,i,i])
            AD[message[0]] = AD[message[4]]
            BE[message[1]]=  BE[message[5]]
            CF[message[2]] = CF[message[6]]
        cycle_dicts = [AD,BE,CF]
        cycles = []
        for i in range(3):
            alphabet = [chr(x) for x in range(ord(Enigma.MIN_LETTER), ord(Enigma.MAX_LETTER)+1)]
            while len(alphabet) != 0:
                start = alphabet.pop(0)

