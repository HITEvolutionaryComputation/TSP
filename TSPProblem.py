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

    # TODO
    def crossover(self, selection_method: int) -> None:
        """
        Do the crossover operation.

        Crossover operation occurs within the population.
        :param selection_method: this parameter represents a crossover method.
        This is the mapping chart:

        crossover_method | real_method
        1 -> Order Crossover
        2 -> PMX Crossover
        3 -> Cycle Crossover
        4 -> Edge Recombination

        :return:
        """
        pass


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
