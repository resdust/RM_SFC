from scipy import stats
import random
import os
import random
import gym
from collections import deque

import numpy as np
import tensorflow as tf
from keras import Sequential
from keras.layers import Input, Dense, Lambda, concatenate
from keras.models import Model
from keras.optimizers import Adam
import keras.backend as K

np.random.seed(1)
tf.set_random_seed(1)

from DQN_movan import DeepQNetwork
from network_env import Env

def run_env(history):
    his_reward = []
    his_suc_rate = []
    episode = 400
    batch = 32

    update_timestep = 10  # update policy every n timesteps

    for i in range(episode):
        print('********episode', i, "*********")
        reward_i = 0
        zero_sum = 0

        for step in range(128):
            print('----step', step, "----")
            # state, state_ = model.RequestArrive() # poison distribution

            # observation, state = env.RequestArrive()  # state为服务请求 possion 到达状态  处理 state 输入
            observation, state = env.RequestArrive()
            observation = np.array(observation)

            print('state:', state)
            action = RL.choose_action(observation)
            print('action', action, env.action_set[action])

            observation_, reward = env.step(action, state)
            RL.store_transition(observation, action, reward, observation_)

            if (step > batch) and (step % update_timestep == 0):
                RL.learn()

                reward_i += reward
                # if reward != 0:
                his_suc_rate.append(reward)

                if reward == 0:
                    zero_sum += 1

        his_reward.append(reward_i)

        history['episode'].append(i)
        history['Episode_reward'].append(reward_i)

        print('Episode: {}/{} | reward: {} | loss: {:.3f}'.format(i, episode, reward_i, sum(RL.cost_his)))

    plot(his_reward)
    plot(his_suc_rate,'Success Rate')

def plot(data,name='Reward'):
        import matplotlib.pyplot as plt
        with open('logs/'+name+'.log','w') as f:
            contents = [str(d)+'\n' for d in data]
            f.writelines(contents)
        plt.plot(np.arange(len(data)), data)
        plt.ylabel(name)
        plt.xlabel('training steps')
        plt.show()

if __name__ == '__main__':
    ############## Hyperparameters ##############
    lr = 0.005
    gamma = 0.9  # discount factor
    random_seed = 123
    e_greedy=0.05
    e_greedy_rate=0.99
    replace_target_iter=200
    memory_size=3000
    #############################################

    log_dict = {'episode': [], 'Episode_reward': [], 'Loss': []}
    env = Env(action_dir='results10',net_file='network_10.txt',attack_num=1) # 10 nodes 'results10'
    # en_action_processs2()  # generate the action set

    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=lr,
                      reward_decay=gamma,
                      e_greedy=e_greedy,
                      e_greedy_rate=e_greedy_rate,
                      replace_target_iter=replace_target_iter,
                      memory_size=memory_size,
                    #   output_graph=True
                      )
    # env.after(100, run_env)
    run_env(log_dict)
    # env.mainloop()
    RL.save()
    RL.plot_cost()
    
def plot_smooth(data_file):
    from scipy.ndimage import gaussian_filter1d
    import matplotlib.pyplot as plt
    import numpy as np
    with open(data_file) as f:
        datas = f.readlines()
    datas = [float(data.strip()) for data in datas]
    y_smoothed = gaussian_filter1d(datas, sigma=5)
    plt.plot(np.arange(len(y_smoothed)), y_smoothed)
    plt.show()

    