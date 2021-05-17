"""
Action                          Reward
select a set of action          1 - hit/len(self.action_set[action_num])
select action with wrong reqs   0
"""
import random 
from attack import Attack
from attack import CrossFire
import tkinter as tk

class Env(tk.Tk, object):
    def __init__(self,action_dir='data/results10',net_file='data/network_10.txt',attack_num=1):
        self.action_dir = action_dir
        self.attack_num = attack_num
        self.net_file = net_file
        self.action_set = []
        self.action_total = []
        self.state = []
        self.state_size = 7 ### for 3 types of requests
        self.matrix = [[0 for i in range(100)] for i in range(100)]
        self.degree_list = [0 for i in range(100)]
        self.degree_change_list = [0 for i in range(100)]
        self.posibility_list = [0 for i in range(100)]
        self.temp_posibility_list = [0 for i in range(100)]
        self.degree_change_list = [0 for i in range(100)]
        flag = 0
        for i in range(self.state_size):
            self.state.append([i, 0, 0])  # [服务编号，状态，状态保持时间]

        self.n_actions = self._action_process()
        self.n_features = self.state_size

    def _action_process(self):
        action_total = {}
        actionset = []

        for r in range(7):
            contents = []
            uni = []
            if r == 0:
                my_file = open(self.action_dir+'/results_1.txt', 'r+')
                service_num = 1
            if r == 1:
                my_file = open(self.action_dir+'/results_2.txt', 'r+')
                service_num = 1
            if r == 2:
                my_file = open(self.action_dir+'/results_3.txt', 'r+')
                service_num = 1
            if r == 3:
                my_file = open(self.action_dir+'/results_12.txt', 'r+')
                service_num = 2
            if r == 4:
                my_file = open(self.action_dir+'/results_13.txt', 'r+')
                service_num = 2
            if r == 5:
                my_file = open(self.action_dir+'/results_23.txt', 'r+')
                service_num = 2
            if r == 6:
                my_file = open(self.action_dir+'/results_123.txt', 'r+')
                service_num = 3

            content = my_file.readline()
            no_line = 0
            while(content):
                # print(content)
                try:
                    node = int(content[0]) # only read the lines begin with number
                except ValueError:
                    if content[0] == 'M':
                        break
                    content = my_file.readline()
                    continue
                line = content.strip()
                nodes = line.split('->')

                nodes = [int(n) for n in nodes]

                j = int(no_line / service_num)
                # try:
                #     contents[j]
                # except IndexError:
                #     contents.append([])
                # for n in nodes:
                #     contents[j].append(int(n))
                    # contents[j].append(node)
                if no_line % service_num == 0:
                    contents.append([])
                contents[j].append(nodes)

                if nodes not in uni:
                    uni.append(nodes)

                no_line = no_line + 1
                content = my_file.readline()

            # action_total.append(uni)
            action_total[r] = contents

        self.action_total = action_total

        for r in action_total:
            actions_state = action_total[r]
            for actions in actions_state:
                action_node = []
                for a in actions:
                    action_node.extend(a)
                actionset.append(action_node)
        self.action_set = actionset ### each action contains only the node indexes
        self.action_total = action_total ### dict map the net state into actionset

        return len(actionset)

    def RequestArrive(self):
        state = [0, 0, 0, 0, 0, 0, 0]
        p = [0.101, 0.101, 0.101, 0.0253, 0.0253, 0.0253,  0.0127]
        p = [0.258, 0.258, 0.258, 0.064, 0.064, 0.064, 0.032]
        p = [0.156, 0.156, 0.156, 0.118, 0.118, 0.118, 0.178]
        r = random.random()
        for i in range(len(p)):
            if i == 0:
                if r <= p[0]:
                    state_num = 0
            else:
                if sum(p[:i]) < r and sum(p[:i+1]) >= r:
                    state_num = i

        state[state_num] = 1
        return state, state_num
    
    def random_pick(self, some_list):
        x = random.uniform(0, 1)
        cumulative_probability = 0.0
        for item, item_probability in zip(some_list, self.posibility_list):
            cumulative_probability += item_probability
            if x < cumulative_probability:
                break
        return item

    def step(self, action_value, state):  # 这里算出reward, 并return 出来
        reward = 0
        zero = 0
        attack = CrossFire(net_file=self.net_file)
        attack_nodes = attack.selectNodes(num=self.attack_num)

        # attacker = CrossFire()
        # test_nodeC = attacker.selectNodes(7)

        index = []
        hit = 0

        # test_node2 = [0, 58, 7, 6, 3, 2, 10]

        for t in attack_nodes:
            if t in self.action_set[action_value]:
                hit += 1
            #     reward = 0
            # else:
            #     reward = 10

        reward = 1 - hit/len(self.action_set[action_value])
        suc_rate = reward

        ### selected wrong action set with incorrect number of req
        no_last = 0
        no_begin = 0
        for i in range(self.state_size):
            for j in range(len(self.action_total[i])):
                no_last = no_last + 1
            if state == i:
                if action_value >= no_last or action_value < no_begin:
                    reward = zero
                break
            no_begin = no_last

        # if state == 0 and action_value > 37:
        #         reward = zero
        # elif state == 1:
        #     if action_value < 38 or action_value > 81:
        #         reward = zero
        # elif state == 2:
        #     if action_value < 82 or action_value > 117:
        #         reward = zero
        # elif state == 3:
        #     if action_value < 118 or action_value > 167:
        #         reward = zero
        # elif state == 4:
        #     if action_value < 168 or action_value > 217:
        #         reward = zero
        # elif state == 5:
        #     if action_value < 218 or action_value > 267:
        #         reward = zero
        # elif state == 6:
        #     if action_value < 268:
        #         reward = zero

        ### update state
        state_, state_num_ = self.RequestArrive()

        return state_, reward

        # observation_, reward, done
if __name__=="__main__":
    import matplotlib.pyplot as plt

    s = []
    env = Env(action_dir='results10')
    for i in range(100):
        state, state_num = env.RequestArrive()
        s.append(state_num)
    # state_, reward = env.step(12,3)

    plt.hist(s,8,normed=True)
    plt.show()