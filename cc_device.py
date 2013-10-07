"""
    Name:     cc_device
    Version:  RC 0.0.1 
    Author:   Antares
    Modified: 07.10.13
    
    #Todo:
"""

import sys
import threading
import datetime
from cc_globals import Globals
from j_connect import TnCiscoAccess

#Don't create pyc files
sys.dont_write_bytecode = True

class Device(threading.Thread):
	def __init__(self, host, ip, commandlist, thread_id, uid, pw):
		threading.Thread.__init__(self)
		self.thread_id = thread_id
		self.host = host
		self.ip = ip
		self.commandlist = commandlist
		self.uid = uid
		self.pw = pw

	def run(self):
		#Prepare and open config file to write
		timestamp = datetime.datetime.now()
		timestamp = timestamp.strftime("%Y_%m_%d_%H%M")
		filename = (self.host + '_' + timestamp)
		fh_config = open (Globals.dir_deviceconfig + filename, 'w')

		#Connect to device
		tn_session = TnCiscoAccess(self.ip, self.host, self.uid, self.pw)
		tn_session.ios_enable_acs_bug(self.host) #acs bug, see j_connect
		fh_config.write(tn_session.run_command(self.commandlist))
		
		tn_session.closeTCA()
		fh_config.close()