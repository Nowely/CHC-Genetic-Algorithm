import numpy as np

# Press Shift+F10 to execute it or replace it with your code.
from chc import Individual, Genetic


def print_hi():
    print(np.random.randint(0, 2, (4, 5), dtype=bool))
    # print(np.zeros((2, 3), dtype=bool))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    testChild = Individual(4, 5, None)
