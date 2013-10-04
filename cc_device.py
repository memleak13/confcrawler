"""
    Name:     cc_device
    Version:  Dev. 0.0.1 
    Author:   Memleak13
    Modified: 04.10.13
    
    #Todo:
"""

import threading
import datetime
from j_connect import TnCiscoAccess

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
		fh_config = open ('./device_configs/' + filename, 'w')

		#Connect to device
		tn_session = TnCiscoAccess(self.ip, self.host, self.uid, self.pw)
		tn_session.no_enable(self.host) #debug

		#print (tn_session.run_command(self.commandlist))
		fh_config.write(tn_session.run_command(self.commandlist, self.host)) #debug
		#print ('wrote: ' + filename) #debug
		
		tn_session.closeTCA()
		fh_config.close()