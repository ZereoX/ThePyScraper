import sqlite3 
import json
  
DATABASE = "Plugins/RSS/RSS.sqlite"

conn = sqlite3.connect(DATABASE, check_same_thread=False)
conn.row_factory = sqlite3.Row
c = conn.cursor()

rows = c.execute('SELECT url, title, content, date FROM RSSEntries ORDER BY entry_id DESC').fetchall()

conn.commit()
conn.close()

print json.dumps( [dict(ix) for ix in rows] ) #CREATE JSON