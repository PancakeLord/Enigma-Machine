from Enigma_Parts import *


class Enigma:
    MIN_LETTER = 'A'
    MAX_LETTER = 'Z'
    ALPHABET_LEN = ord(MAX_LETTER) - ord(MIN_LETTER) + 1
    ROTOR_COUNT = 3
    ROTOR_OFFSET_REPEAT = 2

    def __init__(self, rotor_offsets = [0] * ROTOR_COUNT, base_offsets = [0] * ROTOR_COUNT, plugboard = {}, rotor_order = list(range(ROTOR_COUNT))):
        self.rotor_offsets = rotor_offsets.copy()
        self.base_offsets = base_offsets.copy()
        self.plugboard = plugboard.copy()
        self.rotor_order = rotor_order.copy()

    def encrypt(self, message: str, offsets = [0] * ROTOR_COUNT)-> str:
        start_message = ''.join([chr((x % Enigma.ALPHABET_LEN)+ord(Enigma.MIN_LETTER)) for x in offsets]) * Enigma.ROTOR_OFFSET_REPEAT
        start_encryption = self._eval(start_message)
        self.rotor_offsets = offsets.copy()
        encryption = self._eval(message.upper())
        return start_encryption + encryption

    def decrypt(self, encryption: str)-> str:
        start_encryption = encryption[:Enigma.ROTOR_COUNT*Enigma.ROTOR_OFFSET_REPEAT]
        actual_encryption = encryption[Enigma.ROTOR_COUNT*Enigma.ROTOR_OFFSET_REPEAT:]
        start_decrypted = self._eval(start_encryption)
        self.rotor_offsets = [(ord(start_decrypted[i])-ord(Enigma.MIN_LETTER)) for i in range(Enigma.ROTOR_COUNT)]
        decrypted = self._eval(actual_encryption)
        return start_decrypted + decrypted

    def add_plugboard_connection(self, chr1: chr, chr2: chr) -> None:
        if chr1 != chr2 and chr1 not in self.plugboard.keys() and  chr2 not in self.plugboard.keys():
            self.plugboard[chr1] = chr2
            self.plugboard[chr2] = chr1

    def remove_plugboard_connection(self, chr: chr) -> None:
        if chr in self.plugboard.keys():
            self.plugboard.pop(self.plugboard.pop(chr))

    def _reset(self) -> None:
        self.rotor_offsets = self.base_offsets.copy()

    def _zero_curr_offset(self) -> None:
        self.rotor_offsets = [0]*self.ROTOR_COUNT

    def set_base_offset(self, offset: int, rotor: int) -> None:
        self.base_offsets[rotor] = offset

    def _eval(self, message: str) -> str:
        result = ""
        for char in message:
            result += self._eval_char(char)
        self._reset()
        return result

    def _eval_char(self, character: chr) -> chr:
        if not str.isalpha(character):
            # In truth, messages on the enigma would not include special characters at all. Sometimes SPACE would be
            # represented by X, so HELLO WORLD -> ENC(HELLOXWORLD)
            return character
        e = self._plugboard(character)
        for i in range(Enigma.ROTOR_COUNT):
            e = self._rotor(e, i)
        e = self._reflector(e)
        for i in reversed(range(Enigma.ROTOR_COUNT)):
            e = self._rotor(e, i, reverse=True)
        self._tick()
        return self._plugboard(e)

    def _tick(self) -> None:
        self._turn_rotor(0)

    def _rotor(self, character: chr, rotor: int, reverse=False) -> chr:
        offset = self.rotor_offsets[rotor]
        actual_rotor = self.rotor_order[rotor]
        if reverse:
            return chr((ROTORS[actual_rotor].index(character) - offset) % self.ALPHABET_LEN + ord(Enigma.MIN_LETTER))
        char_pos = (ord(character) - ord(Enigma.MIN_LETTER) + offset) % self.ALPHABET_LEN
        return ROTORS[actual_rotor][char_pos]

    def _reflector(self, character: chr) -> chr:
        return REFLECTOR[ord(character) - ord(Enigma.MIN_LETTER)]
    def _plugboard(self, character: chr) -> chr:
        if (not str.isalpha(character)) or character not in self.plugboard.keys():
            return character
        return self.plugboard[character]

    def _turn_rotor(self, rotor:int) -> None:
        self.rotor_offsets[rotor] += 1
        if rotor < Enigma.ROTOR_COUNT:
            if self.rotor_offsets[rotor] == Enigma.ALPHABET_LEN:
                self.rotor_offsets[rotor] = 0
                if rotor < Enigma.ROTOR_COUNT-1:
                    self._turn_rotor(rotor+1)


enigma = Enigma(plugboard={"A":"C", "C":"A"}, rotor_order=[0,2,1])
encryption = enigma.encrypt("We will intercept the american shipment with our U boats at dawn tomorrow!", [6,13,19])
print(encryption)
decryption = enigma.decrypt(encryption)
print(decryption)