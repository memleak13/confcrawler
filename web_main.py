#!/usr/bin/python
"""
	Version:	Dev. 0.0.1 
	Author:		Memleak13
	Modified:	02.10.13
"""
import os
import web
from customform import CustomForm

render = web.template.render('templates/')
urls = ('/', 'index',)

class index:
	def __init__(self):
		"""prepares and creates drop down menues

		fetches the names of all stored configs and stores them as tupples in
		a list. This list is used to create the drop down elements.
		"""
		#fetching names of available network configs
		dir = os.listdir('./device_configs')
		configs = []
		for entry in dir:
			t = entry, entry
			configs.append(t)

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

if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run()    