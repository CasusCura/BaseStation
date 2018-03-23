# Relise on the mysql.connector library (pip3 install mysql-connector)
import mysql.connector

conn = mysql.connector.connect(user='<username>', password='<password>', host='localhost', database='<database>')

# To close the connection use conn.close()
