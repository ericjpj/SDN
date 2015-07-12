'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
''' Add your imports here ... '''

import csv 


log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

''' Add your global variables here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

        self.forbiddenPairList = []; # police list

    def readFromCVS(self):
	    # remove duplication
	    # add reverse entry 
	    print policyFile
	    csvFile = open(policyFile, 'rb');
	    inStream = csv.reader(csvFile, delimiter=',')
            for row in inStream:
		#print row
                self.forbiddenPairList.append(row)

            self.forbiddenPairList.pop(0)

            for item in self.forbiddenPairList:
                item.pop(0)

    def _handle_ConnectionUp (self, event):
        ''' Add your logic here ... '''
        

        '''
        def drop (duration = None):
            """
            Drops this packet and optionally installs a flow to continue
            dropping similar ones for a while
            """
            if duration is not None:
                if not isinstance(duration, tuple):
                  duration = (duration,duration)
                msg = of.ofp_flow_mod()
                msg.match = of.ofp_match.from_packet(packet)
                msg.idle_timeout = duration[0]
                msg.hard_timeout = duration[1]
                msg.buffer_id = event.ofp.buffer_id
                self.connection.send(msg)
            elif event.ofp.buffer_id is not None:
                msg = of.ofp_packet_out()
                msg.buffer_id = event.ofp.buffer_id
                msg.in_port = event.port
                self.connection.send(msg)
        '''

	
        self.readFromCVS()
       	#print self.forbiddenPairList 
	
        for item in self.forbiddenPairList:
            msg = of.ofp_flow_mod()
	    #print item[0], item[1]
            msg.match.dl_src = EthAddr(item[0])
            msg.match.dl_dst = EthAddr(item[1])
            msg.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
            event.connection.send(msg)
            log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))
            log.debug("Link bteween %s to %s is added", item[0], item[1])

	
def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)
