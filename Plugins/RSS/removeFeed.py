import sqlite3

DATABASE = "Plugins/RSS/RSS.sqlite"

conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("DELETE FROM RSSFeeds WHERE id = 1;")
 
conn.commit()