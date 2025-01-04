from Enigma import *

class Cyclometer:
    def __init__(self, base_offsets = [0]*Enigma.ROTOR_COUNT, ring_settings=[0]*Enigma.ROTOR_COUNT, rotor_order = list(ROTORS.keys()), plugboard = Plugboard()):
        self.set(base_offsets, rotor_order, ring_settings, plugboard)
    def set(self, base_offsets: list, rotor_order: list, ring_settings: list, plugboard = Plugboard()) -> None:
        self.enigma = Enigma(base_offsets=base_offsets.copy(), ring_settings=ring_settings, rotor_order=rotor_order.copy(), plugboard=plugboard)

    def get_cycles(self) -> tuple:
        messages = [self.enigma.encrypt("", [i, i, i]) for i in range(Enigma.ALPHABET_LEN)]
        return Cyclometer.messages_to_cycles(messages)
    def messages_to_cycles(messages: list) -> tuple:
        AD = {}
        BE = {}
        CF = {}
        for message in messages:
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
                cycles[i][cycle_num] = tuple(cycles[i][cycle_num])
                cycle_num += 1
            cycles[i].sort(key=len, reverse=True)
            cycles[i] = tuple(cycles[i])
        return tuple(cycles)
def get_string(base_offsets, rotor_order):
    ans = ""
    for x in base_offsets:
        ans += chr(x+ord(Enigma.MIN_LETTER))
    for x in rotor_order:
        ans += str(len(x))
    return ans