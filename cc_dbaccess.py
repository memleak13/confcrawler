"""
 	Name: 		cc_dbaccess
 	Version:	0.1 
 	Author:		Antares
 	Modified:	22.10.13
 
 	This module controlls access to the db, in this case ./conf/conf.xml.
 	It uses lxml which needs to be installed first

  	#Todo: 
"""
from cc_globals import Globals
from lxml import etree

class XMLConfig(object):
	def __init__(self):
		#Globals.dir_deviceconfig = './conf/' #only used for debugging
		#self.tree = etree.parse(Globals.dir_deviceconfig + 'conf.xml')
		self.tree = etree.parse(Globals.file_configuration)
		self.root = self.tree.getroot()
		
	def search(self, device):
		""" Searche and return an element """
		#Just an example how to search for an element
		#In Python 2.6, you need indices in the format specs - {0}
		xpath_expr = ".//device[@name='{0}']".format(device)
		element = self.root.find(xpath_expr)
		"""
		print "name:{}".format(search.attrib['name'])
		for child in search:
			print ("{}:	{}".format(child.tag, child.text))
		"""
		return element

	def set_last_snap(self, device, filename):
		""" Set the "last_change" child element to the filename """
		el_device = self.search(device)
		#print "name:	{}".format(el_device.attrib['name'])
		for child in el_device: 
			if child.tag == 'last_change':
				child.text = filename
		self.tree.write(Globals.file_configuration, pretty_print=True, method='xml', 
			xml_declaration=True)

	def get_last_snap(self, device):
		""" Return the filename of the last change """
		el_device = self.search(device)
		for child in el_device: 
			if child.tag == 'last_change':
				return child.text





		

