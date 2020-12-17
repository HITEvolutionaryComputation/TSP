from TSPProblem import *
from EvolutionaryAlgorithm import EvolutionaryAlgorithm
filenames=['eil51', 'eil76', 'eil101', 'st70', 'kroA100', 'kroC100', 'kroD100', 'lin105', 'pcb442', 'pr2392']
sizes=[10, 20, 50, 100]
generations = [5000, 10000, 20000]
algorithms=[[3, 1, 1], [3, 1, 2], [3, 2, 1]]


test1=open('test1/test1.txt','w')#打开“test1”
for filename in filenames:
    file_name='test1/'+filename+'.txt'# 打开一个新的“log（问题名）”文件
    log=open(file_name,'w')
    file__name=filename+'.tsp'#tsp文件
    for size in sizes:
        for algorithm in algorithms:
            test1.write(filename+' algorithm:'+"".join('%s' %id for id in algorithm)+' size:'+str(size))#向“test1” 输入 问题：算法：size：
            test1.write('\n')
            Problem=TSPProblem(file__name, size)
            temp=EvolutionaryAlgorithm(Problem,algorithm)
            for gen in range(20000):
                temp.run()
                if gen%100==0:#每100次gen，向“log”写入一个route
                    solution,cost=Problem.population.best_individual()
                    log.write(solution)
                    log.write('\n')
                if gen==5000:#5k、10k、20k处报告cost
                    solution, cost = Problem.population.best_individual()
                    test1.write(cost+' ')
                if gen==10000:
                    solution, cost = Problem.population.best_individual()
                    test1.write(cost+' ')
                if gen==20000:#20k cost处提行
                    solution, cost = Problem.population.best_individual()
                    test1.write(cost+' ')
                    log.write('\r\n')
            test1.write('\r\n')
    log.close()
test1.close()








