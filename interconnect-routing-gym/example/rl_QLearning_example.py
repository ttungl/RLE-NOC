##
# Author: Tung Thanh Le 
# ttungl@gmail.com
##

from collections import defaultdict, deque
from icn_gym import *

import numpy as np
import random
import csv
import os

import matplotlib as mpl
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


## Global Parameters
path = "/home/tungthanhle/gem5/interconnect-routing-gym/"
# topologies = ["Mesh_XY", "Mesh_XY", "Mesh_westfirst"]

topologies = ["Mesh_XY", "Mesh_XY", "Mesh_XY"]
actions = ["xy", "random_oblivious", "west_first"]

a_size = len(actions) # space size of action
Q = defaultdict(lambda: np.zeros(a_size)) # Q-Table
dicts = defaultdict(list)
action_index = random.randint(0, 100)%3
action = actions[action_index]
topology = topologies[action_index] ## TL added 082620

# iter_step = 9 # injection from 0.1 to 0.8
# total_episodes = 50 # Game Playing times
iter_step = 12 # injection from 0.05 to 0.6, step 0.05;
total_episodes = 50 # Game Playing times
# max_state = iter_step/9.0

epsilon = 1.0       # exploration rate
eps_min = 0.01
eps_decay = 0.999

rew_history = []

for i_episode in range(1, total_episodes+1):
	state = 0.05 # = Injection_rate initialized
	rewardsum = 0

	for i in np.arange(0.05, 0.65, 0.05):
		print("QLearning, i_episode {}; injection_rate {}".format(i_episode, state))
		
		# next_state = (state+0.1) # get next state
		next_state = (state*1.0 + 0.05)
		# get epsilon-greedy action probabilities
		# policy_s = epsilon_greedy_probs(Q[next_state], i_episode*1.0)
		policy_s = epsilon_greedy_probs(Q[state], i_episode*1.0) # choose action a from state s
		action_index = np.random.choice(np.arange(a_size), p = abs(policy_s)) ## TL updated 090520
		action = actions[action_index]
		topology = topologies[action_index] ## TL added 082620

		dicts = icn_routing_gym(i_episode, state, action, topology) ## get params updated ## TL added 082620

		reward = reward_f(dicts) # get reward latency from original action 
		# reward = reward_uf(dicts) # get reward throughput from original action

		rewardsum += reward # Sum of Reward for this episode
		if epsilon > eps_min: epsilon *= eps_decay
		# update TD estimate of Q
		Q[state][action_index] = update_Q(Q[state][action_index], np.max(Q[next_state]), \
													reward, .01, epsilon) 
		# update state 
		state = next_state
		
	rew_history.append(rewardsum) # Recording rewards

print('Q-Table = ', Q)

print('Reward = ', rew_history)

# csv_columns = ['average_flit_latency','average_packet_queueing_latency','packets_injected', 'average_packet_network_latency', 'average_hops',  'flits_injected', 'packets_received',  'flits_received', 'average_packet_latency']
csvfile = path + 'Inter_Connect_Networks/Tables/QL_xy_'+str(iter_step)+'_'+str(total_episodes)+ '.csv'

## TL added 082820
# ## read back csvfile
# with open(csvfile) as csv_file:
# 	reader = csv.reader(csv_file)
# 	mydict = dict(reader)

## write dicts
with open(csvfile, 'w') as csv_file:  
	writer = csv.writer(csv_file)
	for key, value in dicts.items():
		writer.writerow([key]+value)

np.savetxt(path + "Inter_Connect_Networks/Rewards_Hist/Reward_history_qlearning_xy.csv", rew_history, delimiter=",")

### Plotting 
mpl.rcdefaults()
mpl.rcParams.update({'font.size': 16})

fig, ax = plt.subplots(figsize=(10,4))
#plt.grid(True, linestyle='--')
plt.title('RLE-NOC Learning')
# plt.plot(range(len(time_history)), time_history, label='Steps', marker="^", linestyle=":")#, color='red')
plt.plot(range(len(rew_history)), rew_history, label='Reward', marker="", linestyle="-")#, color='k')
plt.xlabel('Episodes')
plt.ylabel('Reward')
plt.savefig(path + 'Inter_Connect_Networks/Figures/QL_xy_'+str(iter_step)+'_'+str(total_episodes)+'_RLNOC.png', bbox_inches='tight')
