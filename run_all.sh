#!/bin/bash

# Author: Tung Thanh Le 
# ttungl@gmail.com

python interconnect-routing-gym/example/rl_sarsa_example.py & 
wait
python interconnect-routing-gym/example/rl_expected_sarsa_example.py & 
wait
python interconnect-routing-gym/example/rl_QLearning_example.py