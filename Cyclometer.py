from Enigma import *

class Cyclometer:
    def __init__(self, base_offsets = [0]*Enigma.ROTOR_COUNT, rotor_order = list(range(Enigma.ROTOR_COUNT))):
        self.set(base_offsets, rotor_order)
    def set(self, base_offsets: list, rotor_order: list) -> None:
        self.enigma = Enigma(base_offsets=base_offsets.copy(), rotor_order=rotor_order.copy())

    def get_cycles(self) -> list:
        for i in range(Enigma.ALPHABET_LEN):
            