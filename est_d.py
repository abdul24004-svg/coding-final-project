import sqlite3

db_name = "tomat.db"

connect = sqlite3.connect(db_name, check_same_thread=False)
cursor = connect.cursor()
cursor.execute('SELECT * FROM mc_data')
data = cursor.fetchall()
connect.close()
print(data)