from TSPProblem import *
class EvolutionaryAlgorithm:
    def __init__(self,Problem:TSPProblem,Algorithm):
        self.Problem=Problem
        self.Algorithm=Algorithm
        self.mutationRate=0.4
    def run(self):
        temp=self.Problem.selection(int(self.Algorithm[0]))
        offsprings = []
        while len(offsprings) < self.Problem.size:
            x, y = random.sample(range(len(temp)), 2)
            indi1=self.Problem.population.getindi(x)
            indi2=self.Problem.population.getindi(y)
            cross1, cross2=self.Problem.population.crossover(self.Algorithm[1],indi1,indi2)

            rand = random.random()
            if rand <= self.mutationRate:
                cross1 = cross1.mutation(self.Algorithm[2])

            rand = random.random()
            if rand <= self.mutationRate:
                cross1 = cross1.mutation(self.Algorithm[2])

            offsprings.append(cross1)
            offsprings.append(cross2)

        self.Problem.population.change(offsprings)


