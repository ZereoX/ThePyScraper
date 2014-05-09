import cherrypy
import os.path
import json
import sqlite3 
import queue
import threading
import time
from RSS.DBUtils import *
from time import strftime
import feedparser
import concurrent.futures

DATABASE = "RSS.sqlite"
THREAD_LIMIT = 20

if os.path.isfile(DATABASE): #Does the RSS database exist... if not create it.
	print("Database already exist skipping creation...")
else:
	DBConnection = openSQLConnection(DATABASE, 1)
	SQLExecute(DBConnection.cursor(), 'CREATE TABLE IF NOT EXISTS RSSFeeds (feed_id INTEGER PRIMARY KEY AUTOINCREMENT, url VARCHAR(1000), date DEFAULT (datetime(\'now\')));')
	SQLExecute(DBConnection.cursor(), 'CREATE TABLE IF NOT EXISTS RSSEntries (entry_id INTEGER PRIMARY KEY AUTOINCREMENT, url VARCHAR(1000), title, content, date);')
	commitSQLConnection(DBConnection)
	closeSQLConnection(DBConnection)

class ThePyScraper(object):
	@cherrypy.expose
	def index(self):
		return open('ThePyScraper.html')
	@cherrypy.expose
	def addFeed(self, newFeed):
		raise cherrypy.HTTPRedirect('/')

	@cherrypy.expose
	@cherrypy.tools.json_out()
	def getPosts(self, LIM):

		DBConnection = openSQLConnection(DATABASE, 1)

		rows = DBConnection.cursor().execute('SELECT url, title, content, date FROM RSSEntries ORDER BY date DESC LIMIT 10 OFFSET ?', (LIM,)).fetchall()

		commitSQLConnection(DBConnection)
		closeSQLConnection(DBConnection)

		return json.dumps( [dict(ix) for ix in rows] )

	@cherrypy.expose
	def updateFeeds(self):
		DBConnection = openSQLConnection(DATABASE, 0)

		feeds = DBConnection.cursor().execute('SELECT url, date FROM RSSFeeds').fetchall()

		with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_LIMIT) as threadPool:
			for info in feeds:
				print("Launching Thread with: " + info['url'] + ", " + info['date'])
				threadPool.submit(fetchAndProcessFeed, info['url'], info['date'], DBConnection)

		commitSQLConnection(DBConnection)
		closeSQLConnection(DBConnection)
		
		raise cherrypy.HTTPRedirect('/')

	@cherrypy.expose
	def quit(self):
		cherrypy.engine.exit()

conf = os.path.join(os.path.dirname(__file__) + "scripts/", 'server.conf')
cherrypy.quickstart(ThePyScraper(),config=conf)