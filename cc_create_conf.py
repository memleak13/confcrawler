"""
 	Name: 		cc_create_conf
 	Version:	0.1 
 	Author:		Antares
 	Modified:	22.10.13
 	
 	Standalone script to create xml configuration layout using the 
 	device list. This needs to be done before the application is 
 	run the first time !!!

 	This script uses the lxml module wich needs to be installed first.

  	#Todo: 

"""
from lxml import etree
from cc_dbaccess import XMLConfig

def run():
	"""Creates the conf.xml file

		For each entry in the device list, it creates the device element and
		adds an ip and an empty last_change element. The last change element 
		contains the filename of the configuration file when it was last changed 
		(ex. ubr01SHR_2013_10_20_2355).
	"""
	root = etree.Element("conf")
	with open('./conf/devicelist', 'r') as fh_devlist:
		for line in fh_devlist:
			devicedata = line.split()
			device = etree.SubElement(root, 'device', name = devicedata[0])
			ip = etree.SubElement(device, 'ip')
			ip.text = devicedata[1]
			last = etree.SubElement(device, 'last_change')
			last.text = ''
	tree = etree.ElementTree(root)
	tree.write('./conf/conf.xml', pretty_print=True, method='xml', 
		xml_declaration=True)
	#print(etree.tostring(tree, pretty_print=True, method='xml', xml_declaration=
	#		True))
	
	#Following code is only used to test the dbaccess locally without 
	#connecting to any devices:
	#search = root.find(".//device[@name='ubr01SHR']")
	#for child in search:
	#	print ("{} : {}".format(child.tag, child.text))
	
	#db = XMLConfig()
	#db.set_last_change("ubr01SHR", "Lets see how well this works")
	#db.set_last_change("bgr01SHR", "Test1")
	#print (db.get_last_change("ubr01SHR"))

if __name__ == "__main__": 
    run()