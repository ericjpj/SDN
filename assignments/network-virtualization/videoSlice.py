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


class VideoSlice (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        core.openflow_discovery.addListeners(self)

        # Adjacency map.  [sw1][sw2] -> port from sw1 to sw2
        self.adjacency = defaultdict(lambda:defaultdict(lambda:None))

        '''
        The structure of self.portmap is a four-tuple key and a string value.
        The type is:
        (dpid string, src MAC addr, dst MAC addr, port (int)) -> dpid of next switch
        '''
	'''
        self.portmap = {
                        ('00-00-00-00-00-01', EthAddr('00:00:00:00:00:01'),
                         EthAddr('00:00:00:00:00:03'), 80): '00-00-00-00-00-03',

                        """ Add your mapping logic here"""

                        }
	'''
    def _handle_LinkEvent (self, event):
        l = event.link
        sw1 = dpid_to_str(l.dpid1)
        sw2 = dpid_to_str(l.dpid2)

        log.debug ("link %s[%d] <-> %s[%d]",
                   sw1, l.port1,
                   sw2, l.port2)

        self.adjacency[sw1][sw2] = l.port1
        self.adjacency[sw2][sw1] = l.port2


    def _handle_PacketIn (self, event):
        """
        Handle packet in messages from the switch to implement above algorithm.
        """
        packet = event.parsed
        tcpp = event.parsed.find('tcp')
	ethp = event.parsed.find('ethernet')
	destToPort = {'00:00:00:00:00:01':3, '00:00:00:00:00:02':4,'00:00:00:00:00:03':3,'00:00:00:00:00:04':4}
	def showPktInfo(event, packet):
		ethp = event.parsed.find('ethernet')
		tcpp = event.parsed.find('tcp')
		print("PKTINFO: form %s:%d to %s:%d, on switch %s, in_port: %d" 
			%(ethp.src.toStr(), tcpp.srcport, ethp.dst.toStr(), tcpp.dstport,  dpid_to_str(event.dpid), event.port))
		
		
        def install_fwdrule(event,packet,outport):
            msg = of.ofp_flow_mod()
            msg.idle_timeout = 10
            msg.hard_timeout = 30
            msg.match = of.ofp_match.from_packet(packet, event.port)
            msg.actions.append(of.ofp_action_output(port = outport))
            msg.data = event.ofp
            msg.in_port = event.port
            event.connection.send(msg)

        def forward (message = None):
            this_dpid = dpid_to_str(event.dpid)

            if packet.dst.is_multicast:
                flood()
                return
            else:
                #print("At %s Got unicast packet to %s, in_port %d:" %( dpid_to_str(event.dpid), packet.dst, event.port))
		print ("Unicaset pakcet")
                try:
			'''
			if event.dpid == 1 or event.dpid == 4:
				print("Pakect is at %s" %this_dpid)
				if event.port == 3 or event.port == 4:
					print ("in_port: %d, out_port: 2" %event.port)
					install_fwdrule(event,packet,2);
				else: 
					dstMAC =  packet.dst.toStr()
					print ("in_port: %d, dstMAC: %s , out_port: %d" %(event.port, dstMAC, destToPort[dstMAC]))
					install_fwdrule(event, packet, destToPort[dstMAC]);
			else:	
				print("Pakect is at %s, in_port %d" %(this_dpid, event.port))
				install_fwdrule(event,packet,of.OFPP_FLOOD)
			'''
                except AttributeError:
                    print("packet type has no transport ports, flooding")
		    showPktInfo(event, packet)	
                    # flood and install the flow table entry for the flood
                    install_fwdrule(event,packet,of.OFPP_FLOOD)

        # flood, but don't install the rule
        def flood (message = None):
            """ Floods the packet """
            msg = of.ofp_packet_out()
            msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
            msg.data = event.ofp
            msg.in_port = event.port
            event.connection.send(msg)

        forward()


    def _handle_ConnectionUp(self, event):
        dpid = dpidToStr(event.dpid)
        print("Switch %s has come up." %dpid)
	h1 = {'MAC':EthAddr('00:00:00:00:00:01'), 'swport': 3}
	h2 = {'MAC':EthAddr('00:00:00:00:00:02'), 'swport': 4}
	h3 = {'MAC':EthAddr('00:00:00:00:00:03'), 'swport': 3}
	h4 = {'MAC':EthAddr('00:00:00:00:00:04'), 'swport': 4}
	
	def install_fwdrule_by_packet(event, inport, outport, destMAC = None, tcpport = None):
		if tcpport is None:
            		msg = of.ofp_flow_mod()
			print ("no tcp port rule")
			msg.match.dl_dst = destMAC	
            		msg.match.in_port = inport
           		msg.actions.append(of.ofp_action_output(port = outport))
            		event.connection.send(msg)
			print("Intall a non-video rule")
		elif tcpport == 80:
			print ("tcp port %d rule" %tcpport)
			msg1 = of.ofp_flow_mod()
			msg1.match.nw_proto=6
			msg1.match.dl_type = 0x0800
			msg1.match.tp_src = 80
			msg1.match.dl_dst = destMAC	
            		msg1.match.in_port = inport
           		msg1.actions.append(of.ofp_action_output(port = outport))
            		event.connection.send(msg1)
			print("Intall a video inport 80 rule")
			msg2 = of.ofp_flow_mod()
			msg2.match.nw_proto=6
			msg2.match.dl_type = 0x0800
			msg2.match.tp_dst = 80
			msg2.match.dl_dst = destMAC	
            		msg2.match.in_port = inport
           		msg2.actions.append(of.ofp_action_output(port = outport))
            		event.connection.send(msg2)	
			print("Intall a video inport 80 rule")

	if event.dpid == 1:
		print("Connection from  %s" %dpid)
	
		#in_port 2			
		install_fwdrule_by_packet(event,2,3,h1['MAC'], 80)
		install_fwdrule_by_packet(event,2,4,h2['MAC'], 80)
		install_fwdrule_by_packet(event,1,3,h1['MAC'])
		install_fwdrule_by_packet(event,1,4,h2['MAC'])
		
		#h1
		install_fwdrule_by_packet(event,3,2,h3['MAC'],80)
		install_fwdrule_by_packet(event,3,2,h4['MAC'],80)	
		install_fwdrule_by_packet(event,3,1,h3['MAC'])
		install_fwdrule_by_packet(event,3,1,h4['MAC'])	
		install_fwdrule_by_packet(event,3,4,h2['MAC'])

		# h2	
		install_fwdrule_by_packet(event,4,2,h3['MAC'],80)
		install_fwdrule_by_packet(event,4,2,h4['MAC'],80)
		install_fwdrule_by_packet(event,4,1,h3['MAC'])
		install_fwdrule_by_packet(event,4,1,h4['MAC'])
		install_fwdrule_by_packet(event,4,3,h1['MAC'])	
	if event.dpid == 4:
		print("Connection from  %s" %dpid)

		#h3:
		install_fwdrule_by_packet(event,3,2, h1['MAC'], 80)		
		install_fwdrule_by_packet(event,3,2, h2['MAC'], 80)	
		install_fwdrule_by_packet(event,3,1, h1['MAC'])		
		install_fwdrule_by_packet(event,3,1, h2['MAC'])	
		install_fwdrule_by_packet(event,3,4, h4['MAC'])
	
		#in port 2
		install_fwdrule_by_packet(event,2, h3['swport'], h3['MAC'], 80)
		install_fwdrule_by_packet(event,2, h4['swport'], h4['MAC'], 80)
		install_fwdrule_by_packet(event,1, h3['swport'], h3['MAC'])
		install_fwdrule_by_packet(event,1, h4['swport'], h4['MAC'])


		#h4	
		install_fwdrule_by_packet(event,4,2, h1['MAC'], 80)	
		install_fwdrule_by_packet(event,4,2, h2['MAC'], 80)	
		install_fwdrule_by_packet(event,4,1, h1['MAC'])	
		install_fwdrule_by_packet(event,4,1, h2['MAC'])		
		install_fwdrule_by_packet(event,4,3, h3['MAC'])				
	if event.dpid == 2:
		print("Connection from  %s" %dpid)
		install_fwdrule_by_packet(event,1,2)
		install_fwdrule_by_packet(event,2,1)
	if event.dpid == 3:
		print("Connection from  %s" %dpid)
		install_fwdrule_by_packet(event,1,2)
		install_fwdrule_by_packet(event,2,1)


def launch():
    # Run spanning tree so that we can deal with topologies with loops
    pox.openflow.discovery.launch()
    pox.openflow.spanning_tree.launch()

    '''
    Starting the Video Slicing module
    '''
    core.registerNew(VideoSlice)
