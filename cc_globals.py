"""
    Name:     cc_globals
    Version:  0.1 
    Author:   Antares
    Modified: 22.10.13
    
    Contains global variables, need to be accessible form all modules

    #Todo:
"""

class Globals(object):
	dir_rootdir = ''
	dir_deviceconfig = ''
	file_devicelist = ''
	file_commandlist = ''
	file_configuration = ''
	
	def print_globals(self):
		print Globals.dir_rootdir
		print Globals.dir_deviceconfig
		print Globals.file_devicelist
		print Globals.file_commandlist
		print Globals.file_configuration
		
