### Reinforcement Learning Enabled Routing for High-Performance Networks-on-Chip

Md Farhadur Reza, Tung Thanh Le <br>
IEEE ISCAS, May 2021, Daegu, South Korea. <br>
(Equal Contribution) <br>
[To appear][paper-url] <br>


**Abstract**

> With the increase in cores in the multi-core architectures, the probability of congestion increases because of longer paths among sources and destinations in the network-on-chip (NoC) and because of running multiple applications in a chip. Reactive detection and/or single fixed routing algorithm are not effective to prevent congestion from happening for different traffic patterns in NoC. Therefore, we propose reinforcement learning based proactive routing technique that selects the best routing algorithm from multiple available routing algorithms using NoC utilization and congestion information to improve communication performance. Simulation results demonstrate latency performance improvement while providing robust NoC performance for different NoC states.




### How it works
From the terminal:
* Run all
	```"bash"
	./run_all.sh
	```

* Run individual algorithm
	```"Python"
	python interconnect-routing-gym/example/rl_sarsa_example.py
	```

### Code
The codes are located in the `example` folder.

### Outputs
The results will be stored in the `Inter_Connect_Networks` folder.


## References

1. [Reinforcement Learning based Interconnection Routing for Adaptive Traffic Optimization][NOCS-19-ICN-url]. <br>
Note that we were inspired by this paper's implementation.<br>

2. [Garnet2.0: An On-Chip Network Model for Heterogeneous SoCs][garnet2-url]


<!-- ## Appendix

[CompArch - gem5/garnet tutorial](http://tusharkrishna.ece.gatech.edu/teaching/garnet_gt/)

[Running garnet](http://pwp.gatech.edu/ece-tushar/wp-content/uploads/sites/175/2019/01/Lab1.pdf)

<img src="https://github.com/huckiyang/inconnect-routing-gym/blob/master/ok_1.png" width="400">

### Environment Setup

```"shell"
$sudo apt-get install g++
$sudo apt-get install python
$sudo apt-get install python-dev
$sudo apt-get install swig
$sudo apt-get install zlib
$sudo apt-get install m4

```

### Downloading gem5

Official gem5 from [google git](https://gem5.googlesource.com/)

```
hg clone /nethome/tkrishna3/teaching/simulators/gem5/repo/gem5
```

- ``hg status`` shows what files have been modified in your repository

- ``hg diff`` shows a diff of the modified files.

### How to use it
Import the module in the src directry
* It provides integration with Garnet2.0 in gem5 with the custom-defined RL-alagirithm 
```"python"
from icn_gym import icn_routing_gym as ir-gym
```
### Example
We provide examples of baseline (xy routing)
```
example/Baseline_xyRouting_example.py
```
We provides the example of three RL-alagorithms we present in the paper
```
example/rl_QLearning_example.py
example/rl_sarsa_example.py
example/rl_expected_sarsa_example.py
```
### Example of NoC statistics from Garnet2.0 in gem5
```
network_stats.txt
```
 -->
<!-- MARK DOWN -->
[paper-url]: https://
[NOCS-19-ICN-url]: https://arxiv.org/pdf/1908.04484.pdf
[garnet2-url]: https://www.gem5.org/documentation/general_docs/ruby/garnet-2/


