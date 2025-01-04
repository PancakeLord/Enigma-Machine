class Plugboard:
    def __init__(self, relations = []):
        self.plugs = {}
        for r in relations:
            self.plugs[r[0]] = r[1]
            self.plugs[r[1]] = r[0]

    def __contains__(self, character: chr):
        return character in self.plugs.keys()

    def __getitem__(self, item: chr) -> chr:
        if item in self.plugs.keys():
            return self.plugs[item]
        return item

    def __str__(self):
        return str(self.plugs)

    def __iter__(self):
        return iter(self.plugs.keys())

    def add(self, char1: chr, char2: chr):
        if char1 not in self.plugs.keys() and char2 not in self.plugs.keys() and char1 != char2:
            self.plugs[char1] = char2
            self.plugs[char2] = char1

    def pop(self, char: chr):
        if char in self.plugs.keys():
            self.plugs.pop(self.plugs.pop(char))

    def copy(self):
        copy = self.plugs.copy()
        return Plugboard([x, copy[x]] for x in copy.keys())

