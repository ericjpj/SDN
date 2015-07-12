#! /usr/bin/python
'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net  import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log  import setLogLevel
class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        coreSwitch = self.addSwitch('c1')
	aggSwitchCounter = 1;
	edgeSwitchCounter = 1;
	hostCounter = 1;
	for aggIndex in irange(1, fanout):
		aggSwitch = self.addSwitch('a%s'%aggSwitchCounter)
		aggSwitchCounter += 1
		self.addLink(aggSwitch,coreSwitch,**linkopts1)
		for edgeIndex in irange(1, fanout):
			edgeSwitch = self.addSwitch('e%s'%edgeSwitchCounter)
			edgeSwitchCounter += 1
			self.addLink(edgeSwitch, aggSwitch, **linkopts2)
			for hostIndex in irange(1, fanout):
				host = self.addHost('h%s'%hostCounter)
				hostCounter += 1
				self.addLink(host, edgeSwitch, **linkopts3)
def test():
	l1 = dict(bw=10,delay='1ms')
	l2 = dict(bw=5,delay='3ms')
	l3 = dict(bw=1,delay='5ms', loss=1)
	topo = CustomTopo(l1,l2,l3,3)
	net = Mininet(topo=topo, link=TCLink)
	net.start()
	print "Dump host connections" 
	dumpNodeConnections(net.hosts)
	print "Test connectivity"
	net.pingAll()
if __name__ == '__main__':
	setLogLevel('info')
	test()
	
#topos = { 'custom': ( lambda: CustomTopo() ) }
