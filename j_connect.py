"""
 	Name: 		j_telnet
 	Version:	Dev. 0.0.1 
 	Author:		Memleak13
 	Modified:	03.10.13
 	
 	This module provides access to cisco devices over telnet.
 	To capture the complete output it is important to run the command:
 	terminal length 0 before issuing the actual command.
  
	#Todo:

"""
import time
import re
import telnetlib

class TnCiscoAccess(object):
	"""Creates and establishes telnet session for cisco devices."""
	
	# Defining regular expressions for the different prompts
	ios_unprivPrompt = re.compile ('.*>')
	ios_privPrompt = re.compile ('.*#')
	regexlist = [ios_unprivPrompt, ios_privPrompt, 'Username:', 'Password:', 
				 'username:', 'password:']
	
	def __init__(self, ip, name, uid, password):
		"""stores necessary parameters
		
		args:
			ip, uid, password 
		"""
		self.ip = ip
		self.prompt = name + '#' #read_until prompt (ex. ubr01SHR#)
		self.uid = uid
		self.password = password
		self.telnetoutput = ''

	def no_enable(self, host):
		"""direct access to priviledged mode, no enable password used"""
		self.tn = telnetlib.Telnet(self.ip, 23, 5)
		self.tn.expect(TnCiscoAccess.regexlist)
		self.tn.write(self.uid + "\n")
		self.tn.expect(TnCiscoAccess.regexlist)
		self.tn.write(self.password + "\n")
		self.tn.expect(TnCiscoAccess.regexlist)
		#print host #debug

	def run_command(self,commands, host): #debug
		"""runs one or more commands on a device
		
		and returns the output
		
		args:
			commands: list of commands to be run
		"""
		#print host #debug
		output = ''
		for command in commands:
			#IMPORTANT: REMOVE NEWLINE FIRST!!!
			self.tn.write(command.strip() + "\n")
			print ("host: " + host + " command: " + command) #debug
			output += self.tn.read_until(self.prompt)
			#print ("host: " + host + " command: " + command) #debug
		return output

	def closeTCA(self):
		"""close connection"""
		self.tn.close()