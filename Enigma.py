from Enigma_Parts import *
from Plugboard import *

class Enigma:
    MIN_LETTER = 'A'
    MAX_LETTER = 'Z'
    ALPHABET_LEN = ord(MAX_LETTER) - ord(MIN_LETTER) + 1
    ROTOR_COUNT = 3
    ROTOR_OFFSET_REPEAT = 2

    def __init__(self, base_offsets=[0] * ROTOR_COUNT, ring_settings=[0]*ROTOR_COUNT, plugboard=Plugboard(), rotor_order=list(ROTORS.keys())):
        self.rotor_offsets = base_offsets.copy()
        self.base_offsets = base_offsets.copy()
        self.ring_settings = ring_settings.copy()
        self.plugboard = plugboard.copy()
        self.rotor_order = rotor_order.copy()
        self.rotor_order.reverse()
        self.rotor_offsets.reverse()
        self.base_offsets.reverse()
        self.ring_settings.reverse()

    def encrypt(self, message: str, offsets=[0] * ROTOR_COUNT, only_right=False)-> str:
        start_message = ''.join([chr((x % Enigma.ALPHABET_LEN)+ord(Enigma.MIN_LETTER)) for x in offsets]) * Enigma.ROTOR_OFFSET_REPEAT
        start_encryption = self.eval(start_message, only_right)
        self.rotor_offsets = offsets.copy()
        self.rotor_offsets.reverse()
        encryption = self.eval(message.upper(), only_right)
        return start_encryption + encryption

    def decrypt(self, encryption: str, only_right=False) -> str:
        start_encryption = encryption[:Enigma.ROTOR_COUNT*Enigma.ROTOR_OFFSET_REPEAT]
        actual_encryption = encryption[Enigma.ROTOR_COUNT*Enigma.ROTOR_OFFSET_REPEAT:]
        start_decrypted = self.eval(start_encryption, only_right)
        self.rotor_offsets = [(ord(start_decrypted[i])-ord(Enigma.MIN_LETTER)) for i in range(Enigma.ROTOR_COUNT)]
        self.rotor_offsets.reverse()
        decrypted = self.eval(actual_encryption,only_right)
        return decrypted

    def add_plugboard_connection(self, char1: chr, char2: chr) -> None:
        if char1 != char2 and char1 not in self.plugboard.keys() and char2 not in self.plugboard.keys():
            self.plugboard.add(char1, char2)

    def remove_plugboard_connection(self, char: chr) -> None:
        self.plugboard.pop(self, char)

    def _reset(self) -> None:
        self.rotor_offsets = self.base_offsets.copy()

    def _zero_curr_offset(self) -> None:
        self.rotor_offsets = [0]*self.ROTOR_COUNT

    def set_base_offset(self, offset: int, rotor: str) -> None:
        self.base_offsets[self.rotor_order.index(rotor)] = offset

    def eval(self, message: str, only_right=False) -> str:
        result = ""
        for char in message:
            result += self._eval_char(char, only_right)
        self._reset()
        return result



    def _eval_char(self, character: chr, only_right=False) -> chr:
        if not str.isalpha(character):
            # In truth, messages on the enigma would not include special characters at all. Sometimes SPACE would be
            # represented by X, so HELLO WORLD -> ENC(HELLOXWORLD)
            if character == " ":
                return self._eval_char("X")
            return character
        if only_right:
            self.rotor_offsets[0] += 1
            self.rotor_offsets[0] %= Enigma.ALPHABET_LEN
        else:
            self._tick()
        e = ord(self._plugboard(character)) - ord(Enigma.MIN_LETTER)
        for i in self.rotor_order:
            e = self._rotor(e, i)
        e = self._reflector(e)
        for i in reversed(self.rotor_order):
            e = self._rotor(e, i, reverse=True)
        return self._plugboard(chr(e+ord(Enigma.MIN_LETTER)))

    def _tick(self) -> None:
        self._turn_rotor(0)

    def _rotor(self, val: int, rotor: str, reverse=False) -> int:
        ind = self.rotor_order.index(rotor)
        offset = self.rotor_offsets[ind] - self.ring_settings[ind]
        if reverse:
            return (ROTORS[rotor].index(chr(ord(Enigma.MIN_LETTER) + ((val+offset) % self.ALPHABET_LEN))) - offset) % self.ALPHABET_LEN
        char_pos = (val + offset) % self.ALPHABET_LEN
        return (ord(ROTORS[rotor][char_pos]) - ord(Enigma.MIN_LETTER) - offset) % self.ALPHABET_LEN

    def _reflector(self, val: int) -> int:
        return ord(REFLECTOR[val])-ord(Enigma.MIN_LETTER)
    def _plugboard(self, character: chr) -> chr:
        return self.plugboard[character]

    def _turn_rotor(self, ind: int) -> None:
        rotor = self.rotor_order[ind]
        self.rotor_offsets[ind] = (self.rotor_offsets[ind]+1) % self.ALPHABET_LEN
        if ind < Enigma.ROTOR_COUNT-1:
            if self.rotor_offsets[ind] == ROTOR_TURNOVER[rotor]:
                self._turn_rotor(ind+1)
