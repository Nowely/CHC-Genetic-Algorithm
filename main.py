import numpy as np

# Press Shift+F10 to execute it or replace it with your code.
from chc import Individual, Genetic


def print_hi():
    print(np.random.randint(0, 2, (4, 5), dtype=bool))
    # print(np.zeros((2, 3), dtype=bool))


def sum_func(genome):
    return genome.sum()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a = Genetic(individuals_number=60, fitness_function=sum_func, crossover_rate=0.4, m=12, n=14, delta=0.5,
                number_lives=500)
    a.start_genetic()
    print("Оптимизированное значение:", a.best_fitness, a.best_genome)
