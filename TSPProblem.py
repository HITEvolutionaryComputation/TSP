import numpy as np
import random


class City:
    def __init__(self, x_coordinate: int, y_coordinate: int, seq: int):
        """
        Initial a city. In this class, a city is represented as a pair
        of Euclidean coordinates.
        :param x_coordinate: the x coordinate of this city
        :param y_coordinate: the y coordinate of this city
        :param seq: the city sequence, which is unique in a TSP Problem
        """
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.seq = seq

    def city_distance(self, given_another_city) -> int:
        """
        Calculate the distance between current city and another given city,
        the distance is Euclidean distance.
        :param given_another_city:
        :return: the distance
        """
        x_distance = abs(given_another_city.x_coordinate - self.x_coordinate)
        y_distance = abs(given_another_city.y_coordinate - self.y_coordinate)
        return np.sqrt(x_distance ** 2 + y_distance ** 2)


class Individual:
    def __init__(self, city_list):
        self.city_route = random.sample(city_list, len(city_list))

    def exchange(self, first_index: int, second_index: int) -> None:
        """
        Exchange the city_route value which is correspond to the indices
        :param first_index:
        :param second_index:
        :return:
        """

        if first_index not in range(len(self.city_route)) \
                or second_index not in range(len(self.city_route)):
            raise IndexError("Index is out of boundary")

        self.city_route[first_index], self.city_route[second_index] = \
            self.city_route[second_index], self.city_route[first_index]

    def mutation(self, mutation_method: int) -> None:
        """
        Do the mutation operation.
        :param mutation_method: this parameter represents a mutation method.
        This is the mapping chart:

        mutation_method | real_method
        1 -> insert
        2 -> swap
        3 -> inversion
        4 -> scramble

        The detail information can be seen in https://en.wikipedia.org/wiki/Mutation
        """

        # The insert method
        if mutation_method == 1:
            first_index = random.randint(0, len(self.city_route))
            second_index = random.randint(0, len(self.city_route))
            if first_index == second_index:
                return
            first_index, second_index = min(first_index, second_index), \
                                        max(first_index, second_index)

            for i in range(second_index, first_index + 1, -1):
                self.exchange(i - 1, i)

        # The swap method
        elif mutation_method == 2:
            first_index = random.randint(0, len(self.city_route))
            second_index = random.randint(0, len(self.city_route))
            if first_index == second_index:
                return
            first_index, second_index = min(first_index, second_index), \
                                        max(first_index, second_index)
            self.exchange(first_index, second_index)

        # The Inversion method
        elif mutation_method == 3:
            first_index = random.randint(0, len(self.city_route))
            second_index = random.randint(0, len(self.city_route))
            if first_index == second_index:
                return
            first_index, second_index = min(first_index, second_index), \
                                        max(first_index, second_index)
            self.city_route[first_index:second_index] = \
                reversed(self.city_route[first_index:second_index])

        # The Scramble method
        elif mutation_method == 4:
            fixed_number = random.randint(range(len(self.city_route) + 1))
            fixed_indices = random.sample(range(len(self.city_route)), fixed_number)
            fixed = [(pos, item) for (pos, item) in enumerate(self.city_route) if pos in fixed_indices]
            random.shuffle(self.city_route)

            for pos, item in fixed:
                index = self.city_route.index(item)
                self.exchange(pos, index)

        # Other methods are forbidden
        else:
            raise ValueError("Value is not permitted")


class Population:
    def __init__(self, population_number: int, city_list: list):
        self.individual_list = []
        for i in range(population_number):
            self.individual_list.append(Individual(city_list))

    def crossover(self, crossover_method: int, parent1: Individual, parent2: Individual) -> (Individual, Individual):
        """
        Do the crossover operation.

        Crossover operation occurs within the population.
        :param crossover_method: this parameter represents a crossover method.
        :param parent1: The first parent
        :param parent2: The second parent
        This is the mapping chart:

        crossover_method | real_method
        1 -> Order Crossover
        2 -> PMX Crossover
        3 -> Cycle Crossover
        4 -> Edge Recombination

        :return: a tuple which represents (offspring1, offspring2)
        """

        # OrderCrossover
        if crossover_method == 1:
            # select the start and end point for the crossFragment randomly
            m, n = random.sample(range(len(parent1.city_route)), 2)
            start, end = min(m, n), max(m, n)
            cross1 = parent1.city_route[start: end + 1]
            cross2 = parent2.city_route[start: end + 1]

            # shallow-copy
            offspring1 = []
            for x in parent1.city_route:
                offspring1.append(x)
            offspring2 = []
            for y in parent2.city_route:
                offspring2.append(y)
            size = len(parent1.city_route)

            # sort the elements in parent2 which doesn't in cross1, do the same thing for parent1
            sort2 = []
            sort1 = []
            for i in range(size):
                index2 = (end + 1 + i) % size
                if not (parent2.city_route[index2] in cross1):
                    sort2.append(parent2.city_route[index2])

                index1 = (end + 1 + i) % size
                if not (parent1.city_route[index1] in cross2):
                    sort1.append(parent1.city_route[index1])

            for i in range(len(sort2)):
                p1 = (end + 1 + i) % size
                offspring1[p1] = sort2[i]

                p2 = (end + 1 + i) % size
                offspring2[p2] = sort1[i]

            return Individual(offspring1), Individual(offspring2)

        # PMXCrossover
        elif crossover_method == 2:
            # select the start and end point for the crossFragment randomly
            m, n = random.sample(range(len(parent1.city_route)), 2)
            start, end = min(m, n), max(m, n)
            cross1 = parent1.city_route[start: end + 1]
            cross2 = parent2.city_route[start: end + 1]

            # shallow-copy
            offspring1 = []
            for x in parent1.city_route:
                offspring1.append(x)
            offspring2 = []
            for y in parent2.city_route:
                offspring2.append(y)
            size = len(parent1.city_route)
            # 将cross2中尚未被复制的元素放入offspring1正确的位置,对于cross1相似操作
            # put elements in cross2 which haven't be copied into the right position in offspring1
            for i in range(end + 1 - start):
                # operate for cross2
                if cross2[i] in cross1:
                    continue
                else:
                    tmp = cross1[i]
                    index2 = parent2.city_route.index(tmp)
                    # when the position is taken
                    while start <= index2 <= end:
                        tmp = parent1.city_route[index2]
                        index2 = parent2.city_route.index(tmp)
                    offspring1[index2] = cross2[i]

            # copy the rest elements from parent2 to offspring1
            for i in range(size):
                if (parent2.city_route[i] in cross1) or (parent2.city_route[i] in cross2):
                    continue
                else:
                    offspring1[i] = parent2.city_route[i]

            # do the same thing for cross2
            for j in range(end + 1 - start):
                if cross1[j] in cross2:
                    continue
                else:
                    tmp = cross2[j]
                    index1 = parent1.city_route.index(tmp)
                    while start <= index1 <= end:
                        tmp = parent2.city_route[index1]
                        index1 = parent1.city_route.index(tmp)
                    offspring2[index1] = cross1[j]

            for j in range(size):
                if (parent1.city_route[j] in cross1) or (parent1.city_route[j] in cross2):
                    continue
                else:
                    offspring2[j] = parent1.city_route[j]

            return Individual(offspring1), Individual(offspring2)

        # CycleCrossover
        elif crossover_method == 3:
            x = random.randint(0, len(parent1.city_route) - 1)

            flag = [False] * len(parent1.city_route)
            flag[x] = True

            tmp = parent2.city_route[x]
            while tmp != parent1.city_route[x]:
                p = parent1.city_route.index(tmp)
                flag[p] = True
                tmp = parent2.city_route[p]

            offspring1 = []
            offspring2 = []
            for i in range(len(parent1.city_route)):
                if flag[i]:
                    offspring2.append(parent1.city_route[i])
                    offspring1.append(parent2.city_route[i])
                else:
                    offspring2.append(parent2.city_route[i])
                    offspring1.append(parent1.city_route[i])

            return Individual(offspring1), Individual(offspring2)

        # # EdgeRecombination
        # elif crossover_method == 4:
        # Other methods are forbidden
        else:
            raise ValueError("Value is not permitted")



class TSPProblem:
    def __init__(self, population_number: int, city_list: list):
        self.population = Population(population_number, city_list)
        """
            **YOU SHOULD ADD OTHER PARAMS THAT YOU THINK IS ESSENTIAL**
        """

    # TODO
    def selection(self, selection_method: int) -> Individual:
        """
        Select individual from the population
        :param selection_method: this parameter represents a selection method.
        This is the mapping chart:

        selection_method | real_method
        1 -> fitness-proportional
        2 -> tournament selection
        3 -> elitism

        :return:
        """
        pass

    # TODO
    def begin(self):
        """
        To be continued
        :return:
        """
        pass
