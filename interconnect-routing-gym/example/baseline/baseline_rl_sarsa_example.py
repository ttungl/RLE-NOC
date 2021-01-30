### Original
# RL def code was drived from Xiaoli Ma Group, IEEE Fellow, Georgia Tech ECE
# RL-Telecom Project (GlobeCom19) by C.-H. Huck Yang

### Modification
# Author: Tung Thanh Le 
# ttungl@gmail.com
###

import random
import os
from collections import defaultdict, deque
import numpy as np
import matplotlib as mpl
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import csv
from icn_gym import *

path = "/home/tungthanhle/gem5/interconnect-routing-gym/"

## Global Parameters
topologies = ["Mesh_XY","Mesh_XY", "Mesh_XY", "Mesh_westfirst"]
actions = ["table","xy", "random_oblivious", "west_first"]
a_size = len(actions) # space size of action
Q = defaultdict(lambda: np.zeros(a_size)) # Q-Table
dicts = defaultdict(list)
action_index = random.randint(0, 100)%4
action = actions[action_index]
topology = topologies[action_index] ## TL added 082620

# iter_step = 10 # injection from 0.1 to 0.9
# total_episodes = 50 # Game Playing times

iter_step = 6 # injection from 0.1 to 0.9
total_episodes = 30 # Game Playing times


epsilon = 1.0       # exploration rate
eps_min = 0.01
eps_decay = 0.999

### Plot Notebooks
time_history = []
rew_history = []
act_history = []

Q = defaultdict(lambda: np.zeros(a_size))

for i_episode in range(total_episodes):
	state = 0.1
	# state = np.reshape(int(100*state), [1, iter_step]) # iter_step = state_size
	policy_s = epsilon_greedy_probs(Q[state], i_episode)
	action_index = np.random.choice(np.arange(a_size), p = abs(policy_s))
	action = actions[action_index]
	topology = topologies[action_index] ## TL added 082620

	rewardsum = 0
	for i in range(1, iter_step):
		print("Baseline Sarsa, i_episode {}; injection_rate {}".format(i_episode, state))

		next_state = (i+1)*1.0/10.0 # get next state
		dicts = icn_routing_gym(i_episode, state, action, topology) ## TL added 082620

		# reward = reward_f(dicts) # get reward from original action
		reward = reward_baseline_latency_f(dicts) ## TL added 090720
		rewardsum += reward # Sum of Reward for this episode

		if epsilon > eps_min: epsilon *= eps_decay
		
		# if not done: # Env-Game on going
		# get epsilon-greedy action probabilities
		policy_s = epsilon_greedy_probs(Q[next_state], i_episode)
		
		# pick next action A'
		next_action_index = np.random.choice(np.arange(a_size), p=policy_s)
		
		# update TD estimate of Q
		Q[state][action_index] = update_Q(Q[state][action_index], Q[next_state][next_action_index], 
		                                reward, .01, epsilon)
		action_index = next_action_index
		action = actions[action_index] # get next action
		topology = topologies[action_index] ## TL added 090720
		state = next_state
		# action = actions[random.randint(0, 100)%2]
		
	rew_history.append(rewardsum) # Recording rewards


print('Q-Table:', Q)

print('Reward:', rew_history)

############
## tables ##
############
csv_columns = ['sim_seconds','average_flit_latency','average_packet_queueing_latency','average_flit_network_latency','average_flit_queueing_latency','packets_injected', 'average_packet_network_latency', 'average_hops',  'flits_injected', 'packets_received',  'flits_received', 'average_packet_latency']
csvfile = path + "Inter_Connect_Networks/Tables/Baseline_SARSA_"+str(iter_step)+'_'+str(total_episodes)+".csv"

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

####################
## reward history ##
####################
# csv_rew_hist = path + "Inter_Connect_Networks/Rewards_Hist/Reward_history_rl_sarsa_{}_{}.csv".format(iter_step, total_episodes)

# with open(csv_rew_hist, 'w') as csv_file1:  
# 	writer1 = csv.writer(csv_file1)
# 	for value1 in rew_history:
# 		writer1.writerow(value1)

np.savetxt(path + "Inter_Connect_Networks/Rewards_Hist/Baseline_Reward_history_rl_sarsa.csv", rew_history, delimiter=",")


### Plotting 
# print("Learning Performance")
mpl.rcdefaults()
mpl.rcParams.update({'font.size': 16})

fig, ax = plt.subplots(figsize=(10,4))
#plt.grid(True, linestyle='--')
plt.title('ICNs Learning')
# plt.plot(range(len(time_history)), time_history, label='Steps', marker="^", linestyle=":")#, color='red')
plt.plot(range(len(rew_history)), rew_history, label='Reward', marker="", linestyle="-")#, color='k')
plt.xlabel('Iterations') # Episodes
# plt.xlabel('Episodes')
plt.ylabel('Reward')
plt.savefig(path + 'Inter_Connect_Networks/Figures/Baseline_SARSA_'+str(iter_step)+'_'+str(total_episodes)+'_ICN.png', bbox_inches='tight')