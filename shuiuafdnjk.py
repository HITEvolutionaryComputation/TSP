file=open("delete.txt",'w')
file.write("delete")
file.write('\n')#提行
file.write('reel')
# log.write('\r\n')#隔行

# def __init__(self, file_name):
#
#
# self.fitness = self.all_fits()  # 用于selection 有问题
# self.tournament_size = 2  # Self-setting tournament_size
# self.rate = 0.5  # Self-setting select rate
# self.elitism = 0.2  # Self-setting elitism para
#
# problem = open(file_name, 'r')
# self.n = int(linecache.getline(file_name, 4).split()[2])
# loc = [[0 for col in range(2)] for row in range(self.n)]
# for i in range(self.n):
#     x, y = linecache.getline(file_name, i + 7).split()[1:]
#     loc[i] = int(x), int(y)
#     # loc[i][0]=int(x)
#     # loc[i][1]=int(y)
# self.dist = [[0 for col in range(self.n)] for row in range(self.n)]
# for i in range(self.n):
#     for j in range(self.n):
#         self.dist[i][j] = pow(pow(loc[i][0] - loc[j][0], 2) + pow(loc[i][1] - loc[j][1], 2), 0.5)
# self.population = Population(self.n, [n for n in range(1, self.n + 1)])