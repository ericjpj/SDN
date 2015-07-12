'''
Coursera:
- Software Defined Networking (SDN) course
-- Network Virtualization

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
from collections import defaultdict

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree

from pox.lib.revent import *
from pox.lib.util import dpid_to_str
from pox.lib.util import dpidToStr
from pox.lib.addresses import IPAddr, EthAddr
from collections import namedtuple
import os

log = core.getLogger()


class TopologySlice (EventMixin):	
    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Slicing Module")
    	#self.group1 = [IPAddr("10.0.0.1"),IPAddr("10.0.0.3")]
    	#self.group2 = [IPAddr("10.0.0.2"),IPAddr("10.0.0.4")]
    
    """This event will be raised each time a switch will connect to the controller"""
    def _handle_ConnectionUp(self, event):
        # Use dpid to differentiate between switches (datapath-id)
        # Each switch has its own flow table. As we'll see in this
        # example we need to write different rules in different tables.
        dpid = dpidToStr(event.dpid)
        print("Switch %s has come up."%dpid)
	h1Info = {'MAC':EthAddr("00:00:00:00:00:01"),'IP':IPAddr("10.0.0.1"), 'inPort':3, 'swtich':1}
	h2Info = {'MAC':EthAddr("00:00:00:00:00:02"),'IP':IPAddr("10.0.0.2"), 'inPort':4, 'swtich':1}
	h3Info = {'MAC':EthAddr("00:00:00:00:00:03"),'IP':IPAddr("10.0.0.3"), 'inPort':3, 'swtich':4}
	h4Info = {'MAC':EthAddr("00:00:00:00:00:04"),'IP':IPAddr("10.0.0.4"), 'inPort':4, 'swtich':4}
	#group1 = [IPAddr("10.0.0.1"),IPAddr("10.0.0.3")]
    	#group2 = [IPAddr("10.0.0.2"),IPAddr("10.0.0.4")]
	#h2Info = IPAddr("10.0.0.2")
	#h3Info = IPAddr("10.0.0.3")
	#h4Info = IPAddr("10.0.0.4")
	#wildCardIP = (IPAddr("10.0.0.0"),24)
	#group1 = [IPAddr("10.0.0.1"),IPAddr("10.0.0.3")]
    	#group2 = [IPAddr("10.0.0.2"),IPAddr("10.0.0.4")]
    

        """ Add your logic here """
   	
	'''	
	def addBlockRule(srcIP, group, event):
		for destIPAddr in group:
			msg = of.ofp_flow_mod()
			#print item[0], item[1]
			msg.match.nw_src = srcIP
			msg.match.nw_dst = destIPAddr
			msg.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
			#event.connection.send(msg) 
			core.openflow.getConnection(event.dpid).send(msg)
			print("A rule installed on %s" %dpidToStr(event.dpid))
			print("Link bteween %s to %s is blocked" % (str(srcIP), str(destIPAddr)))
	'''
	'''
	def addPassRule(srcIP, destIP, outPort, event):
			msg = of.ofp_flow_mod()
			#print item[0], item[1]
			msg.match.nw_src = srcIP
			msg.match.nw_dst = destIP
			msg.actions.append(of.ofp_action_output(port = outPort))
			#event.connection.send(msg) 
			#core.openflow.sendToDPID(event.dpid, msg)
			#event.getConnection(event.dpid).send(msg)
            		event.connection.send(msg)
			print("A rule installed on %s"  %dpidToStr(event.dpid))
			print("%s talks to %s through %s by %s" %(str(srcIP), str(destIP), dpid, str(outPort)))
	'''		
	def addPassRuleByPort(inPort, outPort, event):
		msg = of.ofp_flow_mod()
		msg.match.in_port = inPort
		msg.actions.append(of.ofp_action_output(port = outPort))
            	#event.connection.send(msg)
		core.openflow.sendToDPID(event.dpid, msg)
		print("On %s, port %s is linked to port %s" %(dpid, str(inPort),str(outPort)))
	def addDoublePassRuleByPort(inPort, outPort, event):
		addPassRuleByPort(inPort,outPort,event)
		addPassRuleByPort(outPort,inPort,event)	

	if event.dpid == 1 or event.dpid == 4: # switch 1
		print("Adding rules for switch %s" %dpid)
		addDoublePassRuleByPort(1,3,event)
		addDoublePassRuleByPort(4,2,event)
	

		'''
		msg = of.ofp_flow_mod()
		#msg.match.in_port = 3
		msg.match.nw_src = IPAddr("10.0.0.1")
		msg.actions.append(of.ofp_action_output(port = 4))
            	event.connection.send(msg)

		msg = of.ofp_flow_mod()
		#msg.match.in_port = 4
		msg.match.nw_src = IPAddr("10.0.0.2")
		msg.actions.append(of.ofp_action_output(port = 3))
            	event.connection.send(msg)
		'''
		
		#addRule(IPAddr("10.0.0.1"),self.group2,event)
		#addRule(IPAddr("10.0.0.2"),self.group1,event)	
		#addPassRule(h1IP,h2IP,4,event)
		#addPassRule(h1IP,h3IP,1,event)
		#addPassRule(h1IP,h4IP,2,event)

		#addPassRule(h2IP,h1IP,3,event)
		#addPassRule(h2IP,h3IP,1,event)
		#addPassRule(h2IP,h4IP,2,event)

		#addPassRule(h3IP,h1IP,3,event)
	#	addPassRule(h3IP,h2IP,4,event)
	#	addPassRule(h4IP,h1IP,3,event)
	#	addPassRule(h4IP,h2IP,4,event)
				
	
	#if event.dpid == 4: # switch 4 	
	#	print("Adding rules for switch %s" %dpid)
	#	addDoublePassRuleByPort(1,2,event)
		#addRule(IPAddr("10.0.0.3"),self.group2,event)
		#self.addRule(IPAddr("10.0.0.4"),self.group1,event)
	#	addPassRule(h3IP,h1IP,1,event)
	#	addPassRule(h3IP,h2IP,2,event)
	#	addPassRule(h3IP,h4IP,4,event)

	#	addPassRule(h4IP,h1IP,1,event)
	#	addPassRule(h4IP,h3IP,3,event)
	#	addPassRule(h4IP,h2IP,2,event)

	#	addPassRule(h1IP,h3IP,3,event)
	#	addPassRule(h1IP,h4IP,4,event)
	#	addPassRule(h2IP,h3IP,3,event)
	#	addPassRule(h2IP,h4IP,4,event)
	if event.dpid == 2 or event.dpid == 3:
		print("Adding rules for switch %s" %dpid)
		addDoublePassRuleByPort(1,2,event)
	#	addPassRule(wildCardIP,h1IP,1,event);
	#	addPassRule(wildCardIP,h2IP,1,event);
	#	addPassRule(wildCardIP,h3IP,2,event);
	#	addPassRule(wildCardIP,h4IP,2,event);
			



def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Topology Slicing module
    '''
    core.registerNew(TopologySlice)
