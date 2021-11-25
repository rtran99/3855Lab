import mysql.connector

db_conn = mysql.connector.connect(host="lab3855api.westus.cloudapp.azure.com", user="user",
                                  password="password", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
          DROP TABLE Orders; 
          ''')

db_cursor.execute('''
          DROP TABLE Inventory; 
          ''')

db_conn.commit()
db_cursor.close()
