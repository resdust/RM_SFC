import random

class Attack:
    def __init__(self,net_file='network_100.txt'):
        self.netfile = net_file
        self.matrix = [[0 for i in range(100)] for i in range(100)]
        self.degree_list = [0 for i in range(100)]
        self.degree_change_list = [0 for i in range(100)]
        self.posibility_list = [0 for i in range(100)]
        self.temp_posibility_list = [0 for i in range(100)]
        self.degree_change_list = [0 for i in range(100)]
        self.importFigure()
        self.calculateDegree()
        self.degreeChange()
        self.buildingModel()

    def importFigure(self):  # 载入网络拓扑
        i = 0
        j = 0
        my_file = open(self.netfile, 'r')
        content = my_file.readline()
        while (content):
            # content = my_file.readline()
            nodes = content.split()
            self.matrix[int(nodes[0])][int(nodes[1])] = 1
            self.matrix[int(nodes[1])][int(nodes[0])] = 1
            content = my_file.readline()
        # print("matrix", self.matrix)
        return self.matrix

    def calculateDegree(self):  # 计算节点的度 （节点所连边的个数）

        self.matrix = self.importFigure()
        # print("matrix: ", self.matrix)
        global degree_list
        i = 0
        j = 0
        degree = 0
        while (i < 100):
            while (j < 100):
                if (self.matrix[i][j] == 1):
                    degree = degree + 1
                j = j + 1
                self.degree_list[i] = degree
            i = i + 1
            j = 0
            degree = 0
        # print("degree list: ", self.degree_list)
        return self.degree_list

    def degreeChange(self):
        i = 0
        while (i < 100):
            if (self.degree_list[i] >= 7):
                self.degree_change_list[i] = self.degree_list[i] * 10000
            if (self.degree_list[i] < 7 and self.degree_list[i] >= 6):
                self.degree_change_list[i] = self.degree_list[i] * 1000
            if (self.degree_list[i] < 6):
                self.degree_change_list[i] = self.degree_list[i] / 10000
            i = i + 1

    def buildingModel(self):
        sum = 0
        i = 0
        while (i < 100):
            sum = sum + self.degree_change_list[i]
            i = i + 1
        i = 0
        while (i < 100):
            self.posibility_list[i] = float(self.degree_change_list[i] / sum)
            i = i + 1

    def random_pick(self, some_list):
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for item, item_probability in zip(some_list, self.posibility_list):
            cumulative_probability += item_probability
            if x < cumulative_probability:
                break
        return item

    def selectNodes(self,num=5):  # 选取被攻击的点
        pickingNodes = [0 for i in range(num)]
        selecting = 0
        selecting_list = [i for i in range(100)]
        # i = 0
        # while (i < 100):
        #     selecting_list[i] = i
        #     i = i + 1
        # selecting = 0
        x = 0

        for i in range(100):
            self.temp_posibility_list[i] = self.posibility_list[i]

        while (selecting < num):
            x = self.random_pick(selecting_list)
            pickingNodes[selecting] = x
            p = selecting_list.index(x)
            # selecting_list.pop(p)
            self.renewPossibilities(p)
            selecting = selecting + 1

        for i in range(100):
            self.posibility_list[i] = self.temp_posibility_list[i]

        print('picking nodes:', pickingNodes)

        return pickingNodes

    def renewPossibilities(self, p):  # 根据权重分配已经消失的概率,消失的是0.8，0.8根据权重分配到每个元素中，权重计算为0.05/0.2,0.05/0.2,0.02/0.2,0.08/0.2
        temp = self.posibility_list[p]
        for i in range(self.posibility_list.__len__()):
            # 先计算权重,如果不等于P，则计算公式为posibility_list[i] = posibility_list[i] + posibility_list[p]*(posibility_list[i]/(1-posibility_list[p])
            if (i == p):
                self.posibility_list[i] = 0
            else:
                self.posibility_list[i] = self.posibility_list[i] + \
                                          temp * (self.posibility_list[i] / (1 - temp))

class CrossFire:
    def __init__(self,net_file='network-brand.txt'):
        self.netfile = net_file
        self.edges, _ = self.load_edges()
        self.attackedAreas = 0

    # load two-way topology
    def load_edges(self):
        file = self.netfile
        edges = {} 
        B = {}
        topo = [] # topo[i] concludes the nodes connected to node i
        with open(file) as f:
            datas = f.readlines()
    
        for d in datas:
            d = d.split()
            d = [int(x) for x in d]
            i,j = d[0],d[1]
            if i in edges:
                edges[i].append(j)
            else:
                edges[i] = [j]
            if j in edges:
                edges[j].append(i)
            else:
                edges[j] = [i]
            
        i = 0
        keys = list(edges.keys())
        keys.sort()
        for key in keys:
            while(i!= key):
                i = i+1
                topo.append([])
            topo.append([j for j in edges[key]])
            # B[key] = [j[1] for j in edges[key]]
            i = i+1

        print('===Loaded topology with '+str(len(topo))+' nodes===')
        return topo,B
        
    # randomly select a start node and return the largest scale of its linked nodes
    def selectNodes(self, num=6):
        import random

        edges = self.edges
        all_nodes = set()
        attack_all = [[]]
        start = random.choice(list(range(len(edges))))
        all_nodes.add(start)

        area = 0
        attack_all[area] = set()
        attack_all[area].add(start)

        while (sum([len(a) for a in attack_all]) < num):
            new_nodes = set()
            for s in attack_all[area]:
                for n in edges[s]:
                    new_nodes.add(n)
            attacks = list(new_nodes)
            for a in attack_all:
                attacks = attacks + list(a)
            if len(set(attacks)) <= num:
                attack_all[area] = new_nodes
                all_nodes = set(list(new_nodes) + list(all_nodes))
            else:
                area = area + 1
                attack_all.append(set())
                new_start = random.choice(list(range(len(edges))))
                attack_all[area].add(new_start)
                all_nodes.add(new_start)

        self.attackedAreas = area
        return list(all_nodes)
