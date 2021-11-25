import mysql.connector

db_conn = mysql.connector.connect(host="lab3855api.westus.cloudapp.azure.com", user="user",
                                  password="password", database="events")

db_cursor = db_conn.cursor()


db_cursor.execute('''
          CREATE TABLE Orders
          (id INT NOT NULL AUTO_INCREMENT, 
           device_id VARCHAR(250) NOT NULL, 
           ordersreceived INT NOT NULL,
           shippingPriority VARCHAR(100) NOT NULL, 
           shippingCompany VARCHAR(50) NOT NULL,
           address VARCHAR(30) NOT NULL,
           name VARCHAR(50) NOT NULL,
           deliveryDate VARCHAR(50) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT id_pk PRIMARY KEY (id))
          ''')

db_cursor.execute('''
          CREATE TABLE Inventory
          (id INT NOT NULL AUTO_INCREMENT, 
           device_id VARCHAR(250) NOT NULL, 
           quantity INT NOT NULL, 
           trackingId VARCHAR(100) NOT NULL, 
           Itemname VARCHAR(100) NOT NULL,
           manufacturer VARCHAR(100) NOT NULL,
           weight VARCHAR(50) NOT NULL,
           wishlisted INT NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT id_pk PRIMARY KEY (id))
          ''')

db_conn.commit()
db_cursor.close()
