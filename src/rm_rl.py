from DQN_movan import DeepQNetwork
from network_env import Env
import action2sqlite
from action2sqlite import Service

import numpy as np
import time

def execAction(act_num, actions,services): 
    # an action contains services
    for ser_num in range(len(services)):
        delService(ser_num+1, services)
    for ser_num in actions[act_num]:
        execService(ser_num, services)

def execService(num,services):
    # add flow
    for service in services:
        if service.number == num:
            service.execute()
            break

def delService(num,services):
    # del flow
    for service in services:
        if service.number == num:
            service.delete()
            break

def run():
    actions,services = action2sqlite.actionTransfer()
    his_reward = []
    batch = 32
    update_timestep = 10  # update policy every n timesteps
    step = 0
    last_cost = 0

    while(True):
        time.sleep(10)
        print('********step', step, "*********")

        observation, state = env.RequestArrive()
        observation = np.array(observation)

        print('state:', state)
        # action = RL.choose_action(observation)
        action = np.random.randint(0, len(env.action_set))
        print('action', action, env.action_set[action])
        execAction(action,actions,services)


        # actions[action]

        # observation_, reward = env.step(action, state)
        # RL.store_transition(observation, action, reward, observation_)

        # if (step > batch) and (step % update_timestep == 0):
        #     RL.learn()

        # his_reward.append(reward)

        # print('Episode: {} | reward: {} | loss: {:.3f}'.format(step, reward, sum(RL.cost_his)-last_cost))
        # last_cost = sum(RL.cost_his)

if __name__ == "__main__":
    checkpoint_path = 'RL/checkpoint'
    env = Env(action_dir='data/results10',net_file='data/network_10.txt',attack_num=1) # 10 nodes 'results10'
    RL = DeepQNetwork(env.n_actions, env.n_features)
    # RL.load_weights(checkpoint_path)
    # actions = action2sqlite.actionTransfer()
    run()
