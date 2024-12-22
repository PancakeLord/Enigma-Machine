class Cycle:
    def __init__(self):
        self.cycle = {}

    def run(self, c: chr) -> chr:
        if c in self.cycle.keys():
            return self.cycle[c]
        return c
    def add_2_cycle(self, chr1: chr, chr2: chr) -> None:
        self.cycle[chr1] = chr2
        self.cycle[chr2] = chr1
    def multiply_cycle(self, cycle: Cycle):