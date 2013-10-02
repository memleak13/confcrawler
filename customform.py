
import web
from web import net,utils

class CustomForm(web.form.Form):
	"""Custom webpy form.
	
	The original form wraps the elements into a table.
	This way the elements are wrapped into div tags.

	Original author: 
		http://cloud101.eu/blog/2012/04/24/python-for-the-web-with-webpy/
	"""
	def render(self):
		"""
		# with <div> 
		out = '<div id="form">'
		for i in self.inputs:
			html = (utils.safeunicode(i.pre) + i.render() 
			+ self.rendernote(i.note) + utils.safeunicode(i.post))
			out += ('<div id="%s_div"> %s %s</div>' % 
				(i.id, net.websafe(i.description), html))
		out += "</div>"
		return out
		"""
		#without <div>
		out = ''
		for i in self.inputs:
			html = (utils.safeunicode(i.pre) + i.render() 
			+ self.rendernote(i.note) + utils.safeunicode(i.post))
			out += ('%s %s' % (net.websafe(i.description), html))
		#out += "</div>"
		return out
		