"""
	Version:	Dev. 0.0.1 
	Author:		Antares
	Modified:	07.10.13

	This is the main webpy file. It loads the filenames found in 
	../device_configs into a drop down menu. Once chosen, it will compare both
	files.

	Important:  
	1. For additional modules like customform 
		"WSGIPythonPath /home/tbsadmin/projects/confcrawler/web" needs to be set 
		in the virtualhost file.

	2. Create a softlink for the device_configs directory (which is located one
		level higher) 
"""

import os
import web
from customform import CustomForm

#Set absolute path for apache
root = os.path.dirname(__file__)
render = web.template.render(os.path.join(root, 'templates'), cache=False)

urls = (
	'/', 'index',
	'/test', 'test'
	)
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc() #when using mod_wsgi

class index:
	def __init__(self):
		"""prepare and create drop down menues

		fetch the names of all stored configs and stores them as tupples in
		a list. Use this list to create the drop down elements.
		"""
		#fetching names of available network configs
		device_configs = os.path.join(root, 'device_configs')
		dir = os.listdir(device_configs)
		configs = [] 
		for entry in dir:
			t = entry, entry
			configs.append(t)
		configs.sort()

		#defining form elements
		self.dd_source = CustomForm(web.form.Dropdown('source', configs))
		self.dd_target = CustomForm(web.form.Dropdown('target', configs))
		self.bu_compare = CustomForm(web.form.Button('compare'))

	def GET(self):
		"""HTTP GET request"""
		source = self.dd_source()
		target = self.dd_target()
		compare = self.bu_compare()
		return render.index(source,target,compare)

class test:
	def GET(self):
		params = web.input()
		source = params.source
		target = params.target
		return (source, target)
