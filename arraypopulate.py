import mysql.connector
import numpy as np
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="021Aryan",
  database="mydatabase"
)
mycursor = mydb.cursor()
mycursor.execute("select * from one_a;")
count = mycursor.rowcount

for x in mycursor:
    print(x)
    count = count+1
print(count)
mycursor.reset()
mycursor.execute("select group_concat(slot separator ',') from one_a;")
if count>0:
    for x in mycursor:
        one_a_list = x

    one_a_list_string = one_a_list[0].replace(',','')
    print(one_a_list_string)
    one_a_array = []
    one_a = [0]*18
    print(one_a)

    for i in range(len(one_a_list_string)):
        one_a_array.append(int(one_a_list_string[i]))

    print(one_a_array)
        
    for i in range(len(one_a_array)):
        print(one_a_array[i])
        print(i)
        value = one_a_array[i]
        one_a[value-1] = 1

    print(one_a)