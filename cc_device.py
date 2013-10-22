"""
    Name:     cc_device
    Version:  0.1 
    Author:   Antares
    Modified: 22.10.13

    This class represents the device. It is used as a thread to connect to the
    device, retrieve and compare the configuration. Only if the configuration 
    has been changed it writes it back to disk. To do this it compares the last
    snapshot (filename is stored in xml config) and the current one.
    
    #Todo:
"""

import sys
import threading
import datetime
import re
from cc_globals import Globals
from j_connect import TnCiscoAccess

#Don't create pyc files
sys.dont_write_bytecode = True

class Device(threading.Thread):
	def __init__(self, host, ip, commandlist, thread_id, uid, pw, db_config):
		threading.Thread.__init__(self)
		self.thread_id = thread_id
		self.host = host
		self.ip = ip
		self.commandlist = commandlist
		self.uid = uid
		self.pw = pw
		self.db_config = db_config

	def run(self):
		#Prepare and open config file to write
		timestamp = datetime.datetime.now()
		timestamp = timestamp.strftime("%Y_%m_%d_%H%M")
		filename = (self.host + '_' + timestamp)

		#Connect to device
		tn_session = TnCiscoAccess(self.ip, self.host, self.uid, self.pw)
		tn_session.ios_enable_acs_bug(self.host) #acs bug, see j_connect
		terminal_output = tn_session.run_command(self.commandlist)
		tn_session.closeTCA()
		now_snap = terminal_output.splitlines(True) #Creates list from string
		
		#Compare the last and the actual snapshot
		#If changed update db with new "last" snapshot
		if not self.compare_config(now_snap): 
			self.db_config.set_last_snap(self.host, filename)
			with open (Globals.dir_deviceconfig + filename, 'w') as fh_config:
				fh_config.write(terminal_output) #need to write back string
			print ('Configuration has changed: {0}'.format(self.host))
		else:
			print ('Configuration is the same: {0}'.format(self.host))

	def compare_config(self, now_snap):
		"""Compare the last snapshot with actual snapshot"""
		#Get and load last snapshot
		filename = self.db_config.get_last_snap(self.host)
		if not filename:
			print('No last configuration available...')
			return False
		last_snap = open (Globals.dir_deviceconfig + filename).readlines()

		#check if length of both files are the same, if not something
		#has changed -> return false (not equal)
		len_now, len_last = len(now_snap), len(last_snap)
		if len_now != len_last: return False

		#check files line for line if anything changed,
		#ignore lines which match a filter, these always change
		filter = re.compile (r'.*ntp.*|.*uptime.*|.*last.*|.*nvram.*', re.I)
		for index in range(0, len_now):
			if now_snap[index] != last_snap[index]:
				if not re.search(filter, now_snap[index]):
					return False #Configurations are not the same
		return True
