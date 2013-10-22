"""
 	Name: 		j_connect
 	Version:	0.1 
 	Author:		Antares
 	Modified:	22.10.13
 	
 	This module provides access to devices over telnet.

 	Supported devices: Cisco
  
	#Todo:

"""
import re
import telnetlib

class TnCiscoAccess(object):
	"""Creates and establishes telnet session for cisco devices.

	To capture the complete output it is important to run the command:
 	terminal length 0 before issuing the actual command for cisco devices.
	"""
	
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
		self.unpriv_prompt = name + '>' # (ex. ubr01SHR>)
		self.priv_prompt = name + '#' #read_until prompt (ex. ubr01SHR#)
		self.uid = uid
		self.password = password
		self.telnetoutput = ''

	def ios_no_enable(self, host):
		"""direct access to priviledged mode, no enable password"""
		self.tn = telnetlib.Telnet(self.ip, 23, 5)
		self.tn.expect(TnCiscoAccess.regexlist)
		self.tn.write(self.uid + "\n")
		self.tn.expect(TnCiscoAccess.regexlist)
		self.tn.write(self.password + "\n")
		self.tn.expect(TnCiscoAccess.regexlist)
		#print host #debug

	def ios_enable(self, host):
		"""unpriv -> en -> priv, using enable password"""
		self.tn = telnetlib.Telnet(self.ip, 23, 5)
		self.tn.expect(TnCiscoAccess.regexlist)
		self.tn.write(self.uid + "\n")
		self.tn.expect(TnCiscoAccess.regexlist)
		self.tn.write(self.password + "\n")
		self.tn.expect(TnCiscoAccess.regexlist)
		self.tn.write("enable\n")
		self.tn.expect(TnCiscoAccess.regexlist)
		self.tn.write(self.password + "\n")
		self.tn.expect(TnCiscoAccess.regexlist)

	def ios_enable_acs_bug(self, host):
		"""unpriv -> en -> priv, using enable password

		I came accross an issue with the acs server when direct
		access to priv mode is enabled. However for some reason this sometimes
		does not work and it will only grant access to unpriv mode. In this
		case the enable password first needs to be entered...
		"""
		self.tn = telnetlib.Telnet(self.ip, 23, 5)
		self.tn.expect(TnCiscoAccess.regexlist)
		self.tn.write(self.uid + "\n")
		self.tn.expect(TnCiscoAccess.regexlist)
		self.tn.write(self.password + "\n")
		enable = self.tn.expect(TnCiscoAccess.regexlist)
		#Check what mode I am in (priv, unpriv):
		if self.unpriv_prompt in enable[2]:
			print (host + ": unpriv !!!\n") #debug
			self.tn.write("enable\n")
			self.tn.expect(TnCiscoAccess.regexlist)
			self.tn.write(self.password + "\n")
			self.tn.expect(TnCiscoAccess.regexlist)

	def run_command(self,commands):
		"""runs one or more commands on a device and returns the output
		
		args:
			commands: list of commands to be run
		"""
		output = ''
		for command in commands:
			#IMPORTANT: REMOVE NEWLINE FIRST!!!
			self.tn.write(command.strip() + "\n")
			output += self.tn.read_until(self.priv_prompt)
			#print ("host: " + host + " command: " + command) #debug
		return output

	def closeTCA(self):
		"""close connection"""
		self.tn.close()