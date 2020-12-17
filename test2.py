from TSPProblem import *
from EvolutionaryAlgorithm import EvolutionaryAlgorithm
import numpy as np
filenames=['eil51', 'eil76', 'eil101', 'st70', 'kroA100', 'kroC100', 'kroD100', 'lin105', 'pcb442', 'pr2392']
size=50
algorithm=[3, 1, 1]#根据test1结果修改
repeat=10

test2=open('test2/test2.txt','w')#打开“test2”
for filename in filenames:
    file_name = 'test2/' + filename + '.txt'  # 打开一个新的“log（问题名）”文件
    log = open(file_name, 'w')
    file__name = filename + '.tsp'  # tsp文件
    test2.write(filename+' algorithm:'+"".join('%s' %id for id in algorithm)+' size:'+str(size))#向“test2” 输入 问题：算法：size：
    Problem=TSPProblem(file__name, size)
    cost_list=[]
    for r in range(repeat):
        for gen in range(10000):
            EvolutionaryAlgorithm(algorithm,Problem)
            if gen % 100 == 0:  # 每100次gen，向“log”写入一个route
                solution, cost = Problem.population.best_individual()
                log.write(solution)

        solution, cost = Problem.population.best_individual()
        cost_list.append(cost)#每次repeat的cost结果存入列表
        test2.write(np.mean(cost_list)+np.var(cost_list,ddof=1))   #根据得到的10个结果计算平均值、方差
log.close()
test2.close()
