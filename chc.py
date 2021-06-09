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
        print(self.genome)
        # Приспособленность индивида
        self.fitness = 0
        # Передача функции приспособленности (целевая функция)
        self.fitness_function = fitness_function
        # Считаем приспособленность индивида
        self.calculate_fitness()

    def calculate_fitness(self):
        """ Функция для пересчета значения приспособленности индивида"""
        self.fitness = self.fitness_function(self.genome)

    def mutate_cataclysm(self):
        """ Функция для мутации индивида, при которой меняется примерно треть генов"""
        for i in range(self.genome.shape[0]):
            for j in range(self.genome.shape[1]):
                if random.random() <= 1 / 3:
                    self.genome[i, j] = not (self.genome[i, j])
        print(self.genome)


class Genetic:
    """ Класс, отвечающий за реализацию генетического алгоритма"""

    def __init__(self,
                 individuals_number,
                 fitness_function,
                 top_rate,
                 m,
                 n,
                 delta
                 ):
        # Размер популяции
        self.individuals_number = individuals_number
        # Целевая функция
        self.fitness_function = fitness_function
        # Доля лучших, что дадут потомство и перейдут в следуюущую популяцию
        self.top_rate = top_rate
        # Размеры матрицы (генома)
        self.m = m
        self.n = n
        # Пороговое значение для рассояния
        self.delta = delta

        # Лучшее значение, которое было в нашей популяции
        self.best_fitness = None
        # Геном лучшего значения
        self.best_genome = None

    def crossing(self, parent_1: Individual, parent_2: Individual):
        """ Функция для скрещивания двух родителей """
        if self.calculate_distance(parent_1, parent_2) > self.delta:
            # TODO половина несовпадающих значений от каждого родителя
            temp = 2

    def calculate_distance(self, parent_1: Individual, parent_2: Individual):
        """ Функция для вычисления расстояния между родителями"""
        result = 0
        # TODO передавать и этот параметр? Проверить его влияние
        d = 1

        for i in range(self.m):
            for j in range(self.n):
                if random.random() <= 1 / 3:
                    result += abs(parent_1.genome[i, j] - parent_2.genome[i, j]) ** d

        return result / parent_1.genome.size

    def start_genetic(self):
        """ Запуск отбора"""
