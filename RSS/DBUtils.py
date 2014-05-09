import sqlite3
import queue
import feedparser
import time
from time import strftime

def openSQLConnection(DATABASE, THREAD):
	conn = sqlite3.connect(DATABASE, check_same_thread=THREAD)
	conn.row_factory = sqlite3.Row
	return conn

def commitSQLConnection(DBConnection):
	DBConnection.commit()

def closeSQLConnection(DBConnection):
	DBConnection.close()

def SQLExecute(DBCursor, SQLStatement):
	DBCursor.execute(SQLStatement)

def fetchAndProcessFeed(feed_url, feed_date, DBConnection):
    print("Thread opened with: " + feed_url + ", " + feed_date)
    feedparser._HTMLSanitizer.acceptable_elements.update(['iframe','embed'])
    feed = feedparser.parse(feed_url, modified=feed_date)

    if feed.status != 304:
        if hasattr(feed, "modified"):
            DBConnection.cursor().execute("UPDATE RSSFeeds SET date=? WHERE url=?;", (strftime("%Y-%m-%d %H:%M:%S %Z",feed.modified_parsed, feed_url)))
        else:
            DBConnection.cursor().execute("UPDATE RSSFeeds SET date=? WHERE url=?;", (strftime("%Y-%m-%d %H:%M:%S %Z",time.gmtime()), feed_url))
        storeEntries(feed.entries, DBConnection)
    else:
        print("SKIPPING: " + feed_url)

def storeEntries(Entries, DBConnection):
    for entry in Entries:
        post = len(DBConnection.cursor().execute('SELECT entry_id from RSSEntries WHERE url=?', (entry.link,)).fetchall())
        postContent = ""
        if hasattr(entry, "content"):
            postContent = entry.content[0].value
        else:
            postContent = entry.summary
        if post == 0:
            DBConnection.cursor().execute('INSERT INTO RSSEntries (url, title, content, date) VALUES (?,?,?,?)', (entry.link, entry.title, postContent, strftime("%Y-%m-%d %H:%M:%S %Z",entry.updated_parsed)))