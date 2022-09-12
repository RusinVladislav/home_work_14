import sqlite3

data_SQL = "netflix.db"
con = sqlite3.connect("netflix.db")
con.row_factory = sqlite3.Row
cur = con.cursor()

query = "SELECT * FROM netflix LIMIT 5"

cur.execute(query)
result = cur.fetchall()

item = result[4]

for key in item.keys():
    print(key, ": ", item[key])

con.close()
