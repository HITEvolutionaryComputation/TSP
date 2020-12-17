import random

import numpy as np


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
    def __init__(self, city_list, randomly=True):
        if randomly:
            self.city_route = random.sample(city_list, len(city_list))
        else:
            self.city_route = city_list

    def route_distance(self) -> int:
        dist = 0
        for i in range(len(self.city_route)-1):
            dist += self.city_route[i].city_distance(self.city_route[i],self.city_route[i+1])
        return dist

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
            first_index = random.randint(0, len(self.city_route) - 1)
            second_index = random.randint(0, len(self.city_route) - 1)
            if first_index == second_index:
                return
            first_index, second_index = min(first_index, second_index), \
                                        max(first_index, second_index)

            for i in range(second_index, first_index + 1, -1):
                self.exchange(i - 1, i)

        # The swap method
        elif mutation_method == 2:
            first_index = random.randint(0, len(self.city_route) - 1)
            second_index = random.randint(0, len(self.city_route) - 1)
            if first_index == second_index:
                return
            first_index, second_index = min(first_index, second_index), \
                                        max(first_index, second_index)
            self.exchange(first_index, second_index)

        # The Inversion method
        elif mutation_method == 3:
            first_index = random.randint(0, len(self.city_route) - 1)
            second_index = random.randint(0, len(self.city_route) - 1)
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

            return Individual(offspring1, False), Individual(offspring2, False)

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

            return Individual(offspring1, False), Individual(offspring2, False)

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

            return Individual(offspring1, False), Individual(offspring2, False)

        # EdgeRecombination
        elif crossover_method == 4:
            # construct the Table of Edges
            table = []
            size = len(parent1.city_route)
            for i in range(size):
                element = parent1.city_route[i]
                edges = [parent1.city_route[(i + 1) % size], parent1.city_route[(i - 1) % size]]
                index = parent2.city_route.index(element)
                edges.append(parent2.city_route[(index + 1) % size])
                edges.append(parent2.city_route[(index - 1) % size])
                table.append(edges)
            # choose the start city randomly
            offspring1 = []
            offspring2 = []
            start1, start2 = random.sample(range(size), 2)
            startElement1 = parent1.city_route[start1]
            startElement2 = parent1.city_route[start2]
            offspring1.append(startElement1)
            offspring2.append(startElement2)

            nextElement = None
            shortest = 5
            # generate 2 offspring based on the Table of Edges
            while len(offspring1) != size:
                if len(offspring1) == 1:
                    choices = list(filter(lambda k: k not in offspring1, table[start1]))
                else:
                    choices = list(filter(lambda k: k not in offspring1, table[parent1.city_route.index(nextElement)]))
                haveCommonEdge = False
                shortest = 5
                if len(choices) == 1:
                    nextElement = choices[0]
                    offspring1.append(nextElement)
                    continue

                for i in range(len(choices)):
                    choice = choices[i]
                    for j in range(i + 1, len(choices)):
                        otherChoice = choices[j]
                        if choice == otherChoice and i != j:
                            haveCommonEdge = True
                            break
                    if haveCommonEdge:
                        nextElement = choice
                        break
                    else:
                        entityChoices = list(
                            filter(lambda k: k not in offspring1, table[parent1.city_route.index(choice)]))
                        entityChoices = list(set(entityChoices))
                        length = len(entityChoices)
                        if length < shortest:
                            shortest = length
                            nextElement = choice

                offspring1.append(nextElement)

            while len(offspring2) != size:
                if len(offspring2) == 0:
                    choices = list(filter(lambda k: k not in offspring2, table[start2]))
                else:
                    choices = list(filter(lambda k: k not in offspring2, table[parent1.city_route.index(nextElement)]))
                haveCommonEdge = False
                shortest = 5
                if len(choices) == 1:
                    nextElement = choices[0]
                    offspring2.append(nextElement)
                    continue

                for choice in choices:
                    for otherChoice in choices:
                        if choice == otherChoice and choices.index(choice) != choices.index(otherChoice):
                            haveCommonEdge = True
                            break
                    if haveCommonEdge:
                        nextElement = choice
                        break
                    else:
                        entityChoices = list(
                            filter(lambda k: k not in offspring2, table[parent1.city_route.index(choice)]))
                        entityChoices = list(set(entityChoices))
                        length = len(entityChoices)
                        if length < shortest:
                            shortest = length
                            nextElement = choice

                offspring2.append(nextElement)
            return Individual(offspring1, False), Individual(offspring2, False)

        # Other methods are forbidden
        else:
            raise ValueError("Value is not permitted")

# TEST for crossover
# if __name__ == "__main__":
#     c1 = City(1, 1, 1)
#     c2 = City(0, 2, 2)
#     c3 = City(0, 3, 3)
#     c4 = City(0, 4, 4)
#     c5 = City(0, 5, 5)
#     c6 = City(0, 6, 6)
#     c7 = City(0, 7, 7)
#     c8 = City(0, 8, 8)
#     c9 = City(0, 9, 9)
#     city_list1 = [c1, c2, c3, c4, c5, c6, c7, c8, c9]
#     city_list2 = [c9, c3, c7, c8, c2, c6, c5, c1, c4]
#     parent1 = Individual(city_list1, False)
#     parent2 = Individual(city_list2, False)
#     population = Population(10, city_list1)
#     offspring1, offspring2 = population.crossover(4, parent1, parent2)
#     list1 = []
#     for i in range(len(parent1.city_route)):
#         list1.append(offspring1.city_route[i].seq)
#     list2 = []
#     for i in range(len(parent1.city_route)):
#         list2.append(offspring2.city_route[i].seq)
#
#     print(list1)
#     print(list2)


class TSPProblem:
    def __init__(self, population_number: int, city_list: list):
        self.population = Population(population_number, city_list)
        self.fitness = self.all_fits()
        self.rate = 0.5 # Self-setting select rate
        self.tournament_size = 2  # Self-setting tournament_size
        self.elitism = 0.2  # Self-setting elitism para

    # Determine the fitness function
    def all_fits(self) -> list:
        fits = []
        for i in self.population.individual_list:
            fits.append(1./i.route_distance())
        return fits

    # Calculate fitness sum
    def sum(self) -> int:
        total = 0
        for i in range(len(self.fitness)):
            total += self.fitness[i]
        return total

    def selection(self, selection_method: int):
        """
        Select individual from the population
        :param selection_method: this parameter represents a selection method.
        This is the mapping chart:

        selection_method | real_method
        1 -> fitness-proportional
        2 -> tournament selection
        3 -> elitism
        """
        # fitness proportionate selection (roulette wheel selection)
        if selection_method == 1:
            fitness = np.array(self.fitness)
            possibility = fitness / sum(fitness)
            size = int(len(fitness) * self.rate)
            best = np.random.choice([i for i in self.population.individual_list], size=size, p=possibility)

        # tournament selection
        elif selection_method == 2:
            if self.tournament_size >= len(self.population):
                raise ValueError("Tournament size is larger than population size")
            # competitors = random.sample(self.population.individual_list, self.tournament_size)
            # dist = self.all_fits(competitors)
            # mindist = min(dist)
            # for i in range(len(competitors)):
            #     if mindist == dist[i]:
            #         best = competitors[i]
            best = []
            while len(best) < len(self.fitness) * self.rate:
                x, y = random.sample(range(len(self.fitness)), self.tournament_size)
                if self.fitness[x] >= self.fitness[y]:
                    best.append(self.population.individual_list[x])
                else:
                    best.append(self.population.individual_list[y])

        # elitism
        elif selection_method == 3:
            best = []
            # Serial numbers correspond to fitness
            it = {i: self.fitness[i] for i in range(len(self.fitness))}
            # sorted by fitness
            sorted_fitness = sorted(it.items(), key=lambda x: (x[1], x[0]), reverse=True)
            size = int(len(self.fitness) * self.rate)
            ilist = [sorted_fitness[: size][i][0] for i in range(size)]
            for i in range(size):
                best.append(self.population.individual_list[ilist[i]])
        else:
            raise ValueError("Value is not permitted")
        return sorted(best)

    # TODO
    def begin(self):
        """
        To be continued
        :return:
        """
        pass
