# 𝑨– активности, коррелированные с вектором динамической размерности;
# 𝑿"–" характеристики потенциала учащегося, множество вещественных чисел;
# 𝒀"–" компетентносная модель дисциплины, множество вещественных чисел;
# 𝑮"–" геном, пространство поиска для потенциальных решений;
# 𝑷^𝒕 "–" популяция t, состоящая из множество потенциальных решений, особей;
# 𝑾(𝒑)"–" целевая функция;
# 𝒇(𝒊,𝒋)"–" эвристика, функция линейной регрессии;
# 𝒑^∗ "–" искомое решение, особь с определенным набором генов;
# 𝒔𝒆𝒍𝒆𝒄𝒕𝒊𝒐𝒏"–" оператор селекции для отбора особей в следующее поколение;
# 𝒄𝒓𝒐𝒔𝒔𝒊𝒏𝒈"–" оператор скрещивания для создания множества новых особей;
# 𝒄𝒂𝒕𝒂𝒄𝒍𝒚𝒔𝒎 𝒎𝒖𝒕𝒂𝒕𝒊𝒐𝒏"–" оператор мутации, при котором меняется треть генов.

# m - кол-во характеристик
# n - кол-во доступных активностей в пуле
import random
import numpy as np


class Individual:
    """ Класс одного индивида в популяции"""

    def __init__(self, m, n, fitness_function):
        # Потенциальное решение (геном) - первый раз задается случайно
        self.genome = np.random.randint(0, 2, (m, n), dtype=bool)
        # Приспособленность индивида
        self.fitness = 0
        # Размеры матрицы (генома)
        self.m = m
        self.n = n
        # Передача функции приспособленности (целевая функция)
        self.fitness_function = fitness_function
        # Считаем приспособленность индивида
        self.calculate_fitness()

    def calculate_fitness(self):
        """ Функция для пересчета значения приспособленности индивида"""
        self.fitness = self.fitness_function(self.genome)

    def mutate_cataclysm(self):
        """ Функция для мутации индивида, при которой меняется примерно треть генов"""
        for i in range(self.m):
            for j in range(self.n):
                if random.random() <= 1 / 3:
                    self.genome[i, j] = not (self.genome[i, j])


class Genetic:
    """ Класс, отвечающий за реализацию генетического алгоритма"""

    def __init__(self,
                 individuals_number,
                 fitness_function,
                 crossover_rate,
                 m,
                 n,
                 delta,
                 number_lives
                 ):
        # Размер популяции
        self.individuals_number = individuals_number
        # Целевая функция
        self.fitness_function = fitness_function
        # Доля лучших, что дадут потомство и перейдут в следуюущую популяцию (в % соотношении)
        self.crossover_rate = crossover_rate
        # Размеры матрицы (генома)
        self.m = m
        self.n = n
        # Пороговое значение для рассояния
        self.delta = delta
        # сколько раз будет появляться новое поколение (сколько раз будет выполняться алгоритм)
        self.number_lives = number_lives

        # Лучшее значение, которое было в нашей популяции
        self.best_fitness = float('inf')
        # Геном лучшего значения
        self.best_genome = None

    def crossing(self, parent_1: Individual, parent_2: Individual):
        """ Функция для скрещивания двух родителей """

        # создаем 2х новых детей
        child_1 = Individual(self.m, self.n, self.fitness_function)
        child_2 = Individual(self.m, self.n, self.fitness_function)

        for i in range(self.m):
            for j in range(self.n):
                if parent_1.genome[i, j] == parent_2.genome[i, j]:
                    child_1.genome[i, j] = parent_1.genome[i, j]
                    child_2.genome[i, j] = parent_1.genome[i, j]
                else:
                    if random.random() > 0.5:
                        child_1.genome[i, j] = parent_1.genome[i, j]
                        child_2.genome[i, j] = parent_2.genome[i, j]
                    else:
                        child_2.genome[i, j] = parent_1.genome[i, j]
                        child_1.genome[i, j] = parent_2.genome[i, j]

        return child_1, child_2

    def calculate_distance(self, parent_1: Individual, parent_2: Individual):
        """ Функция для вычисления расстояния между родителями"""

        result = 0
        # TODO передавать и этот параметр? Проверить его влияние
        d = 1

        for i in range(self.m):
            for j in range(self.n):
                result += abs(int(parent_1.genome[i, j]) - int(parent_2.genome[i, j])) ** d

        return result / parent_1.genome.size

    def start_genetic(self):
        """ Запуск отбора"""

        # создаем стартовую популяцию
        pack = [self.m, self.n, self.fitness_function]
        population = [Individual(*pack) for _ in range(self.individuals_number)]
        retry_count = 0

        # ЗАпускаем алгоритм
        for _ in range(self.number_lives):

            crossing_count = 0
            new_population = population.copy()
            for individual_1 in population:
                population.remove(individual_1)
                # находим случайную пар
                if population.__len__() == 0:
                    break
                individual_2 = random.choice(population)
                population.remove(individual_2)
                if self.calculate_distance(individual_1, individual_2) < self.delta:
                    child_1, child_2 = self.crossing(individual_1, individual_2)
                    child_1.calculate_fitness()
                    child_2.calculate_fitness()
                    new_population.append(child_1)
                    new_population.append(child_2)
                    crossing_count = crossing_count + 1

            #print(crossing_count)
            # отбираем лучших индивидов
            population = sorted(new_population, key=lambda item: item.fitness)
            if population.__len__() > self.individuals_number:
                population = population[:self.individuals_number]

            if population.__len__() == 0:
                break
            if population.__len__() == 1:
                break

            # теперь проверим значение функции лучшего индивида на наилучшее значение экстремума
            if population[0].fitness < self.best_fitness:
                self.best_fitness = population[0].fitness
                self.best_genome = population[0].genome.copy()

            if crossing_count == 20:
                retry_count = retry_count + 1
            if retry_count == 100:
                retry_count = 0
                for i in range(population.__len__() - 1):
                    population[i + 1].mutate_cataclysm()
