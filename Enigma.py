from Enigma_Parts import *


class Enigma:
    MIN_LETTER = 'A'
    MAX_LETTER = 'Z'
    ALPHABET_LEN = ord(MAX_LETTER) - ord(MIN_LETTER) + 1
    ROTOR_COUNT = 3

    def __init__(self):
        self.rotor_offsets = [0]*self.ROTOR_COUNT
        self.base_offsets = [0]*self.ROTOR_COUNT

    def encrypt(self, message: str)-> str:
        return self._eval(message.upper())

    def decrypt(self, encryption: str)-> str:
        return self._eval(encryption.upper())

    def _reset(self) -> None:
        self.rotor_offsets = self.base_offsets

    def _zero_curr_offset(self) -> None:
        self.rotor_offsets = [0]*self.ROTOR_COUNT

    def set_base_offset(self, offset: int, rotor: int)-> None:
        self.base_offsets[rotor] = offset

    def _eval(self, message: str) -> str:
        result = ""
        for char in message:
            result += self._eval_char(char)
        self._reset()
        return result

    def _eval_char(self, character: chr) -> chr:
        if not str.isalpha(character):
            return character
        e = character
        for i in range(Enigma.ROTOR_COUNT):
            e = self._rotor(e, i)
        e = self._reflector(e)
        for i in reversed(range(Enigma.ROTOR_COUNT)):
            e = self._rotor(e, i, reverse=True)
        self._tick()
        return e

    def _tick(self) -> None:
        self._turn_rotor(0)

    def _rotor(self, character: chr, rotor: int, reverse=False) -> chr:
        offset = self.rotor_offsets[rotor]
        if reverse:
            return chr((ROTORS[rotor].index(character) - offset) % self.ALPHABET_LEN + ord(Enigma.MIN_LETTER))
        char_pos = (ord(character) - ord(Enigma.MIN_LETTER) + offset) % self.ALPHABET_LEN
        return ROTORS[rotor][char_pos]

    def _reflector(self, character: chr) -> chr:
        return REFLECTOR[ord(character) - ord(Enigma.MIN_LETTER)]

    def _turn_rotor(self, rotor:int) -> None:
        self.rotor_offsets[rotor] += 1
        if rotor < Enigma.ROTOR_COUNT:
            if self.rotor_offsets[rotor] == Enigma.ALPHABET_LEN:
                self.rotor_offsets[rotor] = 0
                if rotor < Enigma.ROTOR_COUNT-1:
                    self._turn_rotor(rotor+1)

enigma = Enigma()
encryption = enigma.encrypt("We will intercept the american shipment with our U boats at dawn tommorrow!")
print(encryption)
decryption = enigma.decrypt(encryption)
print(decryption)