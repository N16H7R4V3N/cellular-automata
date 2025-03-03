import random


def binary(number: int, digits: int) -> tuple[int]:
    """Convert a natural number into its binary representation.

    Args:
        number (int): natural number, less than 2^digits
        digits (int, optional): number of digits in binary representation

    Returns:
        tuple[int]: binary representation
    """
    assert 0 <= number < 2**digits

    binary_str = bin(number).removeprefix("0b").zfill(digits)
    return tuple(int(i) for i in binary_str)


class Rule:
    def __init__(self, number: int = None, n: int = 3):
        if number is None:
            number = random.randint(0, 2 ** (2**n) - 1)
            print(f"Randomly generated rule #{number} (n={n})")

        assert number < 2 ** (2**n)
        assert n % 2 == 1

        self.number = number
        self.n = n
        self.mapping = self._get_mapping()

    def _get_mapping(self) -> dict[tuple[int] | int]:
        mapping = {}
        for i, value in zip(range(2**self.n), binary(self.number, 2**self.n)):
            key = binary(i, self.n)
            mapping[key] = value

        return mapping

    def get_next_cell(self, interval_cells: tuple[int]) -> int:
        """Generates the next cell value, based on the interval_cells and the rules' mapping.

        Args:
            interval_cells (tuple[int]): the interval of cells with range self.n

        Returns:
            int: next cell value
        """
        assert len(interval_cells) == self.n
        return self.mapping[interval_cells]

    def __str__(self) -> str:
        number_and_n = f"Rule #{self.number} (n={self.n})"
        mappings = "\n".join([f"    {''.join(str(i) for i in key)}: {value}" for key, value in self.mapping.items()])
        return f"{number_and_n}\n{mappings}"


class CellularAutomata:
    SYMBOLS = {0: " ", 1: "#"}

    def __init__(self, size=256):
        self._size = size
        self.cells = None

        self.init_zeroes()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self.init_zeroes()

    def init_zeroes(self):
        """Initializes the cells all to zero."""
        self.cells = [0] * self._size

    def init_single(self, pos: None | int = None):
        """Initializes the cells all to zero, except for one.

        Args:
            pos (None | int, optional): Poisition of the single cell to be one. If None it chooses the the middle position.
        """
        self.cells = [0] * self.size
        if pos is None:
            self.cells[self.size // 2] = 1
        elif isinstance(pos, int):
            assert 0 <= pos < self.size
            self.cells[pos] = 1

    def randomize(self):
        """Intializes the cells to be randomly with zeros and ones."""
        self.cells = [random.randint(0, 1) for _ in range(self.size)]

    def next_generation(self, rule: Rule):
        """Updates the cells with their next generation.

        Args:
            rule (Rule): contains the mapping of intervals for the next generation of cells
        """
        next_cells = []
        margin = rule.n // 2
        for i in range(self.size):
            interval_indices = tuple(range(i - margin, i + margin + 1))
            # rel_i modulo self.size ensures it wraps around cells
            interval_cells = tuple(map(lambda rel_i: self.cells[rel_i % self.size], interval_indices))

            next_cell = rule.get_next_cell(interval_cells)
            next_cells.append(next_cell)

        self.cells = next_cells

    def run(self, rule: Rule, iteration_limit: int = None):
        """Run and print the Cellular Automata's next generations.

        Args:
            rule (Rule): contains the mapping of intervals for the next generation of cells
            iteration_limit (int, optional): limit the number of iterations. If negative will run indefinitely.
        """
        if iteration_limit is None:
            iteration_limit = self.size // 2

        iteration = 0
        while True:
            print(self)
            self.next_generation(rule)

            iteration += 1
            if iteration > iteration_limit > 0:
                break

    def __str__(self):
        return "".join(self.SYMBOLS[cell] for cell in self.cells)


if __name__ == "__main__":
    rule: Rule = Rule(60)  # Sierpinski
    # rule: Rule = Rule(90)  # Sierpinski
    # rule: Rule = Rule(n=5)
    # print(rule)

    cellular_automata = CellularAutomata(size=255)
    cellular_automata.init_single(pos=0)
    # cellular_automata.randomize()

    cellular_automata.run(rule, iteration_limit=127)
