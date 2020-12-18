from TSPProblem import *
from EvolutionaryAlgorithm import EvolutionaryAlgorithm
import numpy as np
filenames=['eil51', 'eil76', 'eil101', 'st70', 'kroA100', 'kroC100', 'kroD100', 'lin105', 'pcb442', 'pr2392']
size=50
generation=10000
algorithm=[3, 1, 1]  # depend on test1
repeat=10

test2=open('test2/test2.txt','w')  # open“test2”
for filename in filenames:
    file_name = 'test2/' + filename + '.txt'
    log = open(file_name, 'w')
    file__name = filename + '.tsp'  # open".tsp"
    test2.write(filename+' algorithm:'+"".join('%s' %id for id in algorithm)+' size:'+str(size))
    log.write(filename + ' algorithm:' + "".join('%s' % id for id in algorithm) + ' size:' + str(size))
    log.write('\n')
    cost_list = []
    for r in range(repeat):
        Problem = TSPProblem(file__name, size)
        temp = EvolutionaryAlgorithm(Problem, algorithm)
        for gen in range(generation):
            temp.run()
            if gen % 1000 == 0:  # output result per hundred iteration
                solution, cost = Problem.population.findLeastCost()
                log.write(solution)
                log.write('\n')
        solution, cost = Problem.population.findLeastCost()
        cost_list.append(cost)  # generate cost_list
    test2.write(filename+' average cost:'+str(np.mean(cost_list))+' standard deviation:'+str(np.std(cost_list, ddof=1)))   #repeat10次后，根据得到的10个结果计算平均值、方差
    test2.write('\n')
    test2.flush()
    log.close()
test2.close()
