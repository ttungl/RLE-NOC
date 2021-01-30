##
# Author: Tung Thanh Le 
# ttungl@gmail.com
##

from extract_network_stats import Extract_Network
from collections import defaultdict, deque

import numpy as np
import random
import csv
import os

# featslist = ['sim_seconds','packets_injected::total', 'packets_received::total', 'average_packet_queueing_latency', \
#              'average_packet_network_latency', 'average_packet_latency', \
#              'flits_injected::total', 'flits_received::total', \
#              'average_flit_queueing_latency', 'average_flit_network_latency', \
#              'average_flit_latency', 'average_hops'] 

featslist = ['sim_seconds', 'average_packet_latency', 'flits_received::total'] 

# synthetic_traffic = ['uniform_random', 'tornado', 'bit_complement', \
#                            'bit_reverse', 'bit_rotation', 'neighbor', \
#                             'shuffle', 'transpose']

path = '/home/tungthanhle/gem5/'
extnet = Extract_Network(path) # TL added 072520

# topologies = ["Mesh_XY", "Mesh_XY", "Mesh_westfirst"]
topologies = ["Mesh_XY", "Mesh_XY", "Mesh_XY"]
actions = ["xy", "random_oblivious", "west_first"]

a_size = len(actions) # space size of action
dicts = defaultdict(list)
# action_index = random.randint(0, 100)%3
# action = actions[action_index]

## hyperparameters
# alpha: learning rate.
# gamma: discount factor; [1.0; 0.9; 0.8]; the higher value, the less discounting.
# Max[Q(s/, A)] gives a maximum value of Q for all possible actions in the next state.
##

def update_Q(Qsa, Qsa_next, reward, alpha = 0.01, gamma = 0.9):
	""" updates the action-value function estimate using the most recent time step """
	return Qsa + (alpha * (reward + (gamma * Qsa_next) - Qsa))

def epsilon_greedy_probs( Q_s, i_episode, eps = None):
	""" obtains the action probabilities corresponding to epsilon-greedy policy """
	epsilon = 1.0 / (i_episode+1)
	if eps is not None:
		epsilon = eps
	policy_s = np.ones(a_size) * epsilon / a_size
	policy_s[np.argmax(Q_s)] = 1 - epsilon + (epsilon / a_size)
	return abs(policy_s)

def reward_f(d):
	return -round(float(d['average_packet_latency'][-1]), 2) ## mininize latency

def reward_uf(d):
	return round(throughput_f(d), 2) ## maximize throughput

def throughput_f(d): ## TL added 090620
	throughput = float(d["flits_received"][-1]) * 16.0 * 8.0 / float(d["sim_seconds"][-1]) / 1e+9
	return throughput

def latency_f(d): ## TL added 090620
	latency = float(d["average_packet_latency"][-1])
	return latency

def icn_routing_gym(ith_eps, injrate, action, topology):     

	os_command = "/home/tungthanhle/gem5/build/NULL/gem5.debug /home/tungthanhle/gem5/configs/example/garnet_synth_traffic.py \
					--network=garnet2.0 --num-cpus=64 --num-dirs=64 --topology={} --mesh-rows=8 \
					--sim-cycles=20000 --inj-vnet=0 --injectionrate={:f} \
					--synthetic=uniform_random --routing-algorithm={}".format(topology, injrate, action) 
	## 'uniform_random', 'tornado', 'bit_complement', 'bit_reverse', 'bit_rotation', 'neighbor', 'shuffle', 'transpose'
	os.system(os_command)
	
	extnet.parse_features(feat_list=featslist) # TL added 072420
	extnet.write_to_file() # TL added 072520

	with open(path + "interconnect-routing-gym/network_stats.txt", "r") as fd:
		for line in fd:
			key, val = line.split(" = ")
			val = val.strip()
			dicts[key].append(float(val))

	## for analysis ## TL added 090620
	dicts["injrate"].append(float(injrate))
	dicts["action"].append(action)
	dicts["topology"].append(topology)
	dicts["episode"].append(ith_eps)
	dicts["throughput"].append(throughput_f(dicts))
	dicts["latency"].append(latency_f(dicts))

	return dicts

