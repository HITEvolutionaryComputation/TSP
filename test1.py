from TSPProblem import *
from EvolutionaryAlgorithm import EvolutionaryAlgorithm
filenames=['eil51', 'eil76', 'eil101', 'st70', 'kroA100', 'kroC100', 'kroD100', 'lin105', 'pcb442', 'pr2392']
sizes=[10, 20, 50, 100]
generations = [5000, 10000, 20000]
algorithms=[[3, 1, 1], [3, 1, 2], [3, 2, 1]]


test1=open('test1/test1.txt','w')#open“test1”
for filename in filenames:
    file_name='test1/'+filename+'.txt'
    log=open(file_name,'w')
    file__name=filename+'.tsp'#open".tsp"
    for size in sizes:
        for algorithm in algorithms:
            test1.write(filename+' algorithm:'+"".join('%s' %id for id in algorithm)+' size:'+str(size))#向“test1” 输入 问题：算法：size：
            test1.write('\n')
            log.write(filename+' algorithm:'+"".join('%s' %id for id in algorithm)+' size:'+str(size))
            log.write('\n')

            Problem=TSPProblem(file__name, size)
            temp=EvolutionaryAlgorithm(Problem,algorithm)
            for gen in range(20000):
                temp.run()
                if gen%100==0:#output result per hundred iteration
                    solution,cost=Problem.population.findLeastCost()
                    log.write(solution)
                    log.write('\n')
                if gen==4999:#report when 5k、10k、20k
                    solution, cost = Problem.population.findLeastCost()
                    test1.write(str(cost)+' ')
                if gen==9999:
                    solution, cost = Problem.population.findLeastCost()
                    test1.write(str(cost)+' ')
                if gen==19999:
                    solution, cost = Problem.population.findLeastCost()
                    test1.write(str(cost)+' ')
                    log.write('\r\n')

            test1.write('\r\n')
            log.write('\r\n')
            log.flush()
            test1.flush()

    log.close()
test1.close()









