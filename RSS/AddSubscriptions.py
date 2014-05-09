import sqlite3

DATABASE = "RSS.sqlite"

conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("INSERT INTO RSSFeeds(url) VALUES('http://blog.us.playstation.com/feed/');")
c.execute("INSERT INTO RSSFeeds(url) VALUES('http://kotaku.com/rss');")
 
conn.commit()