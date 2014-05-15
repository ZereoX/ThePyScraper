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

DATABASE = "RSS.sqlite" #Name of SQLite database.
THREAD_LIMIT = 20		#Maximum # of threads for feed updates

if os.path.isfile(DATABASE):	#Check if SQLite database already exists...
	print("Database already exist skipping creation...")
else: #If it doesn't exist create database.
	DBConnection = openSQLConnection(DATABASE, 1) #Open Database Connection
	SQLExecute(DBConnection.cursor(), 'CREATE TABLE IF NOT EXISTS RSSFeeds (feed_id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(1000), url VARCHAR(1000), category VARCHAR(1000) DEFAULT \'Uncategorized\', date DEFAULT (datetime(\'now\')));')
	commitSQLConnection(DBConnection) #Commit table(RSSFeeds) to allow referencial integrity in table(RSSEntries)
	SQLExecute(DBConnection.cursor(), 'CREATE TABLE IF NOT EXISTS RSSEntries (entry_id INTEGER PRIMARY KEY AUTOINCREMENT, feed_id INTEGER, url VARCHAR(1000), title, content, date, FOREIGN KEY(feed_id) REFERENCES RSSFeeds(feed_id));')
	commitSQLConnection(DBConnection) #Commit table(RSSEntries).
	closeSQLConnection(DBConnection) #Close Connection

class ThePyScraper(object):
	@cherrypy.expose
	def index(self):
		return open('ThePyScraper.html') #Return default page.

	@cherrypy.expose
	def addAFeed(self, feed_url): #Get feed from user.
		DBConnection = openSQLConnection(DATABASE, 1) #Open Database Connection
		feed_url_parsed = feedparser.parse(feed_url) #Parse feed_url, is it a feed?

		if feed_url_parsed.bozo == 0: #If feed_url was parsable
			doesFeedExist = len(DBConnection.cursor().execute('SELECT feed_id from RSSFeeds WHERE title=?', (feed_url_parsed.feed.title,)).fetchall()) #Check if feed already exists. Checks feed title to bypass any url formating differences.

			if doesFeedExist == 0: #If the feed doesn't already exist.
				DBConnection.cursor().execute("INSERT INTO RSSFeeds(url, title) VALUES(?,?);", (feed_url, feed_url_parsed.feed.title)) #Add feed to table(RSSFeeds).

				feed_id = DBConnection.cursor().execute('SELECT feed_id from RSSFeeds WHERE url=?', (feed_url,)).fetchone()[0]

				commitSQLConnection(DBConnection) #Commit new feed to table(RSSFeeds).
				closeSQLConnection(DBConnection) #Close Connection
				raise cherrypy.HTTPRedirect('/updateFeeds?feed_id=' + str(feed_id)) #Redirect to updateFeeds for added feed.

			closeSQLConnection(DBConnection)
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
	@cherrypy.tools.json_out()
	def getFeeds(self):
		DBConnection = openSQLConnection(DATABASE, 1)

		rows = DBConnection.cursor().execute('SELECT url, title, content, date FROM RSSFeeds ORDER BY date DESC LIMIT 10 OFFSET ?', (LIM,)).fetchall()

		commitSQLConnection(DBConnection)
		closeSQLConnection(DBConnection)

		return json.dumps( [dict(ix) for ix in rows] )


	@cherrypy.expose
	def updateFeeds(self, feed_id):
		DBConnection = openSQLConnection(DATABASE, 0)

		if feed_id == "0": #If feed_id is 0 update all feeds.
			feeds = DBConnection.cursor().execute('SELECT feed_id, url, date FROM RSSFeeds').fetchall()
		else: #Otherwise, update only the feed matching the value of feed_id
			feeds = DBConnection.cursor().execute('SELECT feed_id, url, date FROM RSSFeeds WHERE feed_id=?', (feed_id,)).fetchall()

		with concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_LIMIT) as threadPool:
			for info in feeds:
				print("Launching Thread ID#:" + str(info['feed_id']) + " = " + info['url'] + ", " + info['date'] + ".")
				threadPool.submit(fetchAndProcessFeed, info['feed_id'], info['url'], info['date'], DBConnection)

		commitSQLConnection(DBConnection)
		closeSQLConnection(DBConnection)
		
		raise cherrypy.HTTPRedirect('/')

	@cherrypy.expose
	def quit(self):
		cherrypy.engine.exit()

conf = os.path.join(os.path.dirname(__file__) + "scripts/", 'server.conf')
cherrypy.quickstart(ThePyScraper(),config=conf)