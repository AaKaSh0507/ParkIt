import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="021Aryan",
  database="mydatabase"
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE mydatabase")
# mycursor.execute("SHOW DATABASES")

mycursor.execute("CREATE TABLE entrytable (car_number varchar(255) , parking_area varchar(255) , parking_slot int , entry_time datetime , mobile_number varchar(10))")
# mycursor.execute("show tables")
mycursor.execute("SELECT * FROM ENTRYTABLE")
for x in mycursor:
  print(x)
