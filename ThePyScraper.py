import cherrypy
import os.path
import json
import sqlite3 

DATABASE = "Plugins/RSS/RSS.sqlite"

if os.path.isfile(DATABASE): #Does the RSS database exist... if not create it.
	print "Database already exist skipping creation..."
else:
	execfile("Plugins/RSS/init.py")

class ThePyScraper(object):
	@cherrypy.expose
	def index(self):
		return open('ThePyScraper.html', 'r').read() #Return the default indext page.

	@cherrypy.expose
	def addFeed(self, newFeed):
		execfile("Plugins/RSS/addFeed.py")
		return open('ThePyScraper.html', 'r').read()

	@cherrypy.expose
	def getPosts(self, LIM):
		cherrypy.response.headers['Content-Type'] = 'application/json'

		conn = sqlite3.connect(DATABASE, check_same_thread=False)
		conn.row_factory = sqlite3.Row
		c = conn.cursor()

		rows = c.execute('SELECT url, title, content, date FROM RSSEntries ORDER BY date DESC LIMIT 10 OFFSET ?', (LIM,)).fetchall()

		conn.commit()
		conn.close()

		return json.dumps( [dict(ix) for ix in rows] )

	@cherrypy.expose
	def updateFeeds(self):
		return open('ThePyScraper.html', 'r').read()

	@cherrypy.expose
	def quit(self):
		cherrypy.engine.exit()

conf = os.path.join(os.path.dirname(__file__) + "scripts/", 'server.conf')
cherrypy.quickstart(ThePyScraper(),config=conf)