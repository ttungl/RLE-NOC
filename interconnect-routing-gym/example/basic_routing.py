# Author: Tung Thanh Le 
# ttungl@gmail.com

from collections import defaultdict, deque
from icn_gym import *

import numpy as np
import csv


## Global Parameters
path = "/home/tungthanhle/gem5/interconnect-routing-gym/"

topologies = ["Mesh_XY", "Mesh_XY", "Mesh_XY"]
actions = ["xy", "random_oblivious", "west_first"]

i_episode = 0
iter_step = 12 # injection from 0.1 to 0.6
# state = 0.1 # = Injection_rate initialized
# dicts = defaultdict(list) # reset

for action, topology in zip(actions, topologies):

	dicts = defaultdict(list) ## initialized/reset.
	state = 0.05 # = Injection_rate initialized

	for i in np.arange(0.05, 0.65, 0.05):
		print("Basic Routing {}, topology {}, i_episode {}; injection_rate {}".format(action, topology, i_episode, state))
		
		next_state = (state*1.0 + 0.05) # get next state/injrate

		dicts = icn_routing_gym(i_episode, state, action, topology) ## get params updated ## TL added 082620

		# update state 
		state = next_state
		
	csvfile = path + 'Inter_Connect_Networks/Tables/BasicRouting_topoXY_'+str(action)+'_'+str(iter_step)+'_'+str(i_episode)+  '.csv'

	## write dicts
	with open(csvfile, 'w') as csv_file:  
		writer = csv.writer(csv_file)
		for key, value in dicts.items():
			writer.writerow([key]+value)
	

