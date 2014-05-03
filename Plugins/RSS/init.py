import sqlite3

DATABASE = "Plugins/RSS/RSS.sqlite"

conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS RSSFeeds (id INTEGER PRIMARY KEY AUTOINCREMENT, url VARCHAR(1000), last_modified date DEFAULT (datetime(\'now\')));')
c.execute('CREATE TABLE IF NOT EXISTS RSSEntries (entry_id INTEGER PRIMARY KEY AUTOINCREMENT, url, title, content, date);')
 
conn.commit()