import sqlite3
import threading
import time
import Queue
from time import strftime
 
import feedparser     # available at http://feedparser.org
 
 
THREAD_LIMIT = 20
jobs = Queue.Queue(0)
rss_to_process = Queue.Queue(THREAD_LIMIT)
 
DATABASE = "Plugins/RSS/RSS.sqlite"

conn = sqlite3.connect(DATABASE, check_same_thread=False)
conn.row_factory = sqlite3.Row
c = conn.cursor()
 
feeds = c.execute('SELECT id, url, last_modified FROM RSSFeeds').fetchall()
 
def store_feed_items(id, items):
    """ Takes a feed_id and a list of items and stored them in the DB """
    for entry in items:
        c.execute('SELECT entry_id from RSSEntries WHERE url=?', (entry.link,))
        post = ""
        if hasattr(entry, "content"):
            post = entry.content[0].value
        else:
            post = entry.summary
        if len(c.fetchall()) == 0:
            c.execute('INSERT INTO RSSEntries (url, title, content, date) VALUES (?,?,?,?)', (entry.link, entry.title, post, strftime("%Y-%m-%d %H:%M:%S %Z",entry.updated_parsed)))
 
def thread():
    while True:
        try:
            id, feed_url, last_modified = jobs.get(False) # False = Don't wait
        except Queue.Empty:
            return
 
        feedparser._HTMLSanitizer.acceptable_elements.update(['iframe','embed'])
        feed = feedparser.parse(feed_url, modified=last_modified)

        if feed.status != 304:
            entries = feed.entries
            if hasattr(feed, "modified"):
                c.execute("UPDATE RSSFeeds SET last_modified=? WHERE url=?;", (strftime("%Y-%m-%d %H:%M:%S %Z",feed.modified_parsed, feed_url))
            else:
                c.execute("UPDATE RSSFeeds SET last_modified=? WHERE url=?;", (strftime("%Y-%m-%d %H:%M:%S %Z",time.gmtime()), feed_url))
            rss_to_process.put((id, entries), True) # This will block if full
        else:
            print "SKIPPING: " + feed_url
 
for info in feeds: # Queue them up
    jobs.put([info['id'], info['url'], info['last_modified']])
 
for n in xrange(THREAD_LIMIT):
    t = threading.Thread(target=thread)
    t.start()
 
while threading.activeCount() > 1 or not rss_to_process.empty():
    # That condition means we want to do this loop if there are threads
    # running OR there's stuff to process
    try:
        id, entries = rss_to_process.get(False, 1) # Wait for up to a second
    except Queue.Empty:
        continue
 
    store_feed_items(id, entries)
 
conn.commit()