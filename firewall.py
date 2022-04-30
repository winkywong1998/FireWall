from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os

log = core.getLogger()

class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):
        ''' Add your logic here ... '''
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

	block_address = of.ofp_match()
	block_address.dl_src = EthAddr("00:00:00:00:00:02")
	block_address.dl_dst = EthAddr("00:00:00:00:00:03")
	of_msg = of.ofp_flow_mod()
	of_msg.match = block_address
	of_msg.priority = 33000  #

	log.debug(event.connection)
	event.connection.send(of_msg)

def launch ():
    core.registerNew(Firewall)
