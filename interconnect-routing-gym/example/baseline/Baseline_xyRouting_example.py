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

# from icn_gym import icn_routing_gym

# path = '/home/tungthanhle/gem5/'


## Global Parameters
# actions = ["xy", "random_oblivious", "turn_model_oblivious", "turn_model_adaptive"]
# actions = [0, 1] # TL added 072520: 0: weight-based table, 1: XY routing, 2: custom
topologies = ["Mesh_XY","Mesh_XY", "Mesh_XY", "Mesh_westfirst"]
actions = ["table","xy", "random_oblivious", "west_first"]
a_size = len(actions) # space size of action
Q = defaultdict(lambda: np.zeros(a_size)) # Q-Table
dicts = defaultdict(list)
# action_index = random.randint(0, 100)%2
# action = actions[action_index]

action_index = random.randint(0, 100)%4
action = actions[action_index]

iter_step = 6 # injection from 0.1 to 0.6
# total_episodes = 1 # Game Playing times
total_episodes = 5 # Game Playing times

epsilon = 1.0       # exploration rate
eps_min = 0.01
eps_decay = 0.999

### Plot Notebooks
time_history = []
rew_history = []
Q = defaultdict(lambda: np.zeros(a_size))

state = 0.1 # = Injection_rate as reset state env.reset()
i_episode = 1

for i in range(iter_step):
	state = (i+1.0)*1.0/10.0 ## injection rate 
	action_index = random.randint(0, 100)%4
	action = actions[action_index]
	topology = topologies[action_index]
	dicts = icn_routing_gym(i_episode, state, action, topology) ## ICN_env = icn_routing_gym
	# action = actions[random.randint(0, 100)%4]

rew_history.append(0) # Recording rewards

print('Q-Table = ', Q)

print('Reward = ', rew_history)

# print('Dicts = ',dicts)

csv_columns = ['average_flit_latency','average_packet_queueing_latency','average_flit_network_latency','average_flit_queueing_latency','packets_injected', 'average_packet_network_latency', 'average_hops',  'flits_injected', 'packets_received',  'flits_received', 'average_packet_latency']
csv_file = path + 'Inter_Connect_Networks/Tables/env_base_'+str(iter_step)+'_' +str(total_episodes)+ '.csv'

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

np.savetxt(path + "Inter_Connect_Networks/Rewards_Hist/Reward_history_baseline_xy_routing.csv", rew_history, delimiter=",")

### Plotting 
# print("Learning Performance")
mpl.rcdefaults()
mpl.rcParams.update({'font.size': 16})

fig, ax = plt.subplots(figsize=(10,4))
#plt.grid(True, linestyle='--')
plt.title('ICNs Learning')
# plt.plot(range(len(time_history)), time_history, label='Steps', marker="^", linestyle=":")#, color='red')
plt.plot(range(len(rew_history)), rew_history, label='Reward', marker="", linestyle="-")#, color='k')
# plt.xlabel('Iterations') # Episodes
plt.xlabel('Episodes')
plt.ylabel('Reward')
plt.savefig(path + 'Inter_Connect_Networks/Figures/env_base_'+str(iter_step)+'_'+str(total_episodes)+'_ICN.png', bbox_inches='tight')