from datetime import datetime
from secrets import choice
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import os
from twilio.rest import Client
import csv
import pandas as pd
from datetime import timedelta
import time
import mysql.connector
import easyocr

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="021Aryan",
  database="mydatabase"
)

mycursor = mydb.cursor()

dir_path = r'photos'
car_len = (len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))

account_sid = 'ACe2fe5ecc0bcb8dbeab87b5824761c81d'
auth_token = '315929b2a65797dad8c5769f6211333c'
client = Client(account_sid, auth_token)

parkedcars = 0

one_a = [0]*8
two_a = [0]*6
three_a = [0]*10
towers = [0]*14

mycursor.execute("select * from one_a;")
count = mycursor.rowcount

for x in mycursor:
    
    count = count+1

mycursor.reset()

mycursor.execute("select group_concat(slot separator ',') from one_a;")


if count>0:
        for x in mycursor:
            one_a_list = x

        one_a_list_string = one_a_list[0].replace(',','')
        one_a_array = []

        for i in range(len(one_a_list_string)):
            one_a_array.append(int(one_a_list_string[i]))
            
        for i in range(len(one_a_array)):
            value = one_a_array[i]
            one_a[value-1] = 1

mycursor.reset()
mycursor.execute("select * from two_a;")
count = mycursor.rowcount

for x in mycursor:
   
    count = count+1

mycursor.reset()
mycursor.execute("select group_concat(slot separator ',') from two_a;")


if count>0:
        for x in mycursor:
            two_a_list = x

        two_a_list_string = two_a_list[0].replace(',','')
        two_a_array = []

        for i in range(len(two_a_list_string)):
            two_a_array.append(int(two_a_list_string[i]))


        for i in range(len(two_a_array)):
            value = two_a_array[i]
            two_a[value-1] = 1

mycursor.reset()
mycursor.execute("select * from three_a;")
count = mycursor.rowcount

for x in mycursor:
    
    count = count+1

mycursor.reset()
mycursor.execute("select group_concat(slot separator ',') from three_a;")

if count>0:
        for x in mycursor:
            three_a_list = x

        three_a_list_string = three_a_list[0].replace(',','')

        three_a_array = []

        for i in range(len(three_a_list_string)):
            one_a_array.append(int(three_a_list_string[i]))

            
        for i in range(len(three_a_array)):
            value = three_a_array[i]
            three_a[value-1] = 1

mycursor.reset()
mycursor.execute("select group_concat(slot separator ',') from towers;")
count = mycursor.rowcount
if count>0:
        for x in mycursor:
            towers_list = x

        towers_list_string = towers_list[0].replace(',','')

        towers_array = []
        print(towers)

        for i in range(len(towers_list_string)):
            towers_array.append(int(towers_list_string[i]))

            
        for i in range(len(towers_array)-1):
        
            value = towers_array[i]
            towers[value-1] = 1
mycursor.reset()    
    
print(f"1A:{one_a}")
print(f"2A:{two_a}")
print(f"3A:{three_a}")
print(f"towers:{towers}")

def numberextraction(img):
    # cam = cv2.VideoCapture(0)
    # cv2.namedWindow("test")
    # img_counter = 0
    # while True:
    #     ret, frame = cam.read()
    #     if not ret:
    #         print("failed to grab frame")
    #         break
    #     cv2.imshow("test", frame)

    #     k = cv2.waitKey(1)
    #     if k%256 == 27:
    #         # ESC pressed
    #         print("Escape hit, closing...")
    #         break
    #     elif k%256 == 32:
    #         # SPACE pressed
    #         img_name = f"photos/image{img_counter+5}.jpg".format(img_counter)
    #         cv2.imwrite(img_name, frame)
    #         print(f"{img_name} written!")
    #         img_counter += 1

    # cam.release()

    cv2.destroyAllWindows()
    img = cv2.imread(f'photos/image{img}.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection
    # plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0,255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    # plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    # plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))


    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    number = result[0][-2]
    return number

def no_blank(fd):
    try:
        while True:
            line = next(fd)
            if len(line.strip()) != 0:
                yield line
    except:
        return

right_one_a = []
left_one_a = []


def entry(img):

    global parkedcars
    global fullslots
    global one_a,two_a,three_a,towers

    number=numberextraction(img)
    print(f"\n\nhello {number}")
    parkedcars = parkedcars+1
    phone_number = input(("\nplease enter your phone number\n"))
    carentry = 0
    slot = 0

    # [1,1,0,0,0,1,1,1,0,0]
    # [1    1
    #  1    1
    #  0    1
    #  0    0
    #  0    0 ]

    #current array = [1,1,0,0,1,1,1,0,0]

    choice = input(f"\n\nwhere do you want to park?\n1A\n2A\n3A\nTowers\nenter : ")


    if(choice=="1A"):
        right_one_a = []
        left_one_a = []
        for i in range(int(len(one_a)/2)):
            left_one_a.append(int(one_a[i]))

        print(left_one_a)
        first_empty_slot_left = left_one_a.index(0)
        print(first_empty_slot_left)

        for i in range(int(len(one_a)/2),len(one_a)):
            right_one_a.append(int(one_a[i]))

        first_empty_slot_right = right_one_a.index(0)
        print(right_one_a)
        print(first_empty_slot_right)

        if(first_empty_slot_left>first_empty_slot_right):
            right_one_a[first_empty_slot_right] = 1
            slot = first_empty_slot_right+len(left_one_a)

        if(first_empty_slot_left<=first_empty_slot_right):
            left_one_a[first_empty_slot_left] = 1
            slot = first_empty_slot_left

        one_a = np.concatenate([left_one_a,right_one_a])
        print(f"one a :{one_a}")





    if(choice=="2A"):
        right_two_a = []
        left_two_a = []


        for i in range(int(len(two_a)/2)):
            left_two_a.append(int(two_a[i]))

        # print(left_two_a)
        first_empty_slot_left_two_a = left_two_a.index(0)
        # print(first_empty_slot_left_two_a)

        for i in range(int(len(two_a)/2),len(two_a)):
            right_two_a.append(int(two_a[i]))

        first_empty_slot_right_two_a = right_two_a.index(0)
        # print(right_two_a)
        # print(first_empty_slot_right_two_a)

        if(first_empty_slot_left>first_empty_slot_right):
            right_two_a[first_empty_slot_right_two_a] = 1

        if(first_empty_slot_left<=first_empty_slot_right):
            left_two_a[first_empty_slot_left_two_a] = 1

        two_a = np.concatenate([left_two_a,right_two_a])
        print(f"two a :{two_a}")  
       

    if(choice=="3A"):
        right_three_a = []
        left_three_a = []


        for i in range(int(len(three_a)/2)):
            left_one_a.append(int(three_a[i]))

        # print(left_three_a)
        first_empty_slot_left_three_a = left_three_a.index(0)
        # print(first_empty_slot_left_three_a)

        for i in range(int(len(three_a)/2),len(three_a)):
            right_three_a.append(int(three_a[i]))

        first_empty_slot_right_three_a = right_three_a.index(0)
        # print(right_three_a)
        # print(first_empty_slot_right_three_a)

        if(first_empty_slot_left_three_a>=first_empty_slot_right_three_a):
            right_three_a[first_empty_slot_left_three_a] = 1

        if(first_empty_slot_left_three_a<first_empty_slot_right_three_a):
            left_three_a[first_empty_slot_left_three_a] = 1

        three_a = np.concatenate([left_three_a,right_three_a])
        print(f"three a :{three_a}")



    if(choice=="TOWERS"):
        right_towers = []
        left_towers = []


        for i in range(int(len(towers)/2)):
            left_towers.append(int(towers[i]))

        # print(left_towers)
        first_empty_slot_left_towers = left_towers.index(0)
        # print(first_empty_slot_left_towers)

        for i in range(int(len(towers)/2),len(towers)):
            right_towers.append(int(towers[i]))

        first_empty_slot_right_towers = right_towers.index(0)
        # print(right_towers)
        # print(first_empty_slot_right_towers)

        if(first_empty_slot_left_towers>=first_empty_slot_right_towers):
            right_towers[first_empty_slot_left_towers] = 1

        if(first_empty_slot_left_towers<first_empty_slot_right_towers):
            left_towers[first_empty_slot_left_towers] = 1

        one_a = np.concatenate([left_towers,right_towers])
        print(f"towers :{towers}")
        
    def removespaces(string):
        return string.replace(" ", "")

    number = removespaces(number)
    print(number)
    now = datetime.now()
    insert = f"insert into entrytable(car_number,parking_area,parking_slot,entry_time,mobile_number) values (%s,%s,%s,%s,%s)"
    val = (number , choice , slot+1 , now, phone_number)
    mycursor.execute(insert , val)
    for x in mycursor:
        print(x)
    mydb.commit()
    print("ENTRY GRANTED!!")

    if choice == "1A":
        insert = f"insert into one_a(car_number,slot,entry_time,mobile_number) values (%s,%s,%s,%s)"
        val = (number , slot+1 , now, phone_number)
        mycursor.execute(insert , val)
        for x in mycursor:
         print(x)
        mydb.commit()
    
    if choice == "2A":
        insert = f"insert into two_a(car_number,slot,entry_time,mobile_number) values (%s,%s,%s,%s)"
        val = (number , slot+1 , now, phone_number)
        mycursor.execute(insert , val)
        for x in mycursor:
         print(x)
        mydb.commit()

    if choice == "3A":
        insert = f"insert into three_a(car_number,slot,entry_time,mobile_number) values (%s,%s,%s,%s)"
        val = (number , slot+1 , now, phone_number)
        mycursor.execute(insert , val)
        for x in mycursor:
         print(x)
        mydb.commit()

    if choice == "TOWERS":
        insert = f"insert into towers(car_number,slot,entry_time,mobile_number) values (%s,%s,%s,%s)"
        val = (number , slot+1 , now, phone_number)
        mycursor.execute(insert , val)
        for x in mycursor:
         print(x)
        mydb.commit()



    # with open("list.csv","r+") as f:
    #     mydatalist=f.readlines()
    #     numberlist = []
    #     for line in mydatalist:
    #         entry = line.split(',')
    #         numberlist.append(entry[0])
    #     if number not in numberlist:
    #         now = datetime.now()
    #         entrytime = now.strftime('%H:%M:%S')
    #         f.writelines(f"\n{parkedcars},{number},{choice},{entrytime},{slot+1},{phone_number}")
            # message = client.messages \
            #         .create(
            #             body=f"your car {number} has been parked in {choice} in the slot {slot} at {entrytime}",
            #             from_='+16232577297',
            #             to=f'+91{phone_number}'
            #         )
            # print(message.status)
    
def removespaces(string):
    return string.replace(" ", "")

def exitcar(img):
    number=numberextraction(img)
    number = removespaces(number)
    mycursor.reset()
    mycursor.execute(f"select * from entrytable where car_number ='{number}'")
    for x in mycursor:
        print(x)
        if x[1]=="1A":
            index = x[2]
            one_a[index-1]=0
            print(one_a)
            insert = (f"update entrytable set exit_time=now() where parking_slot = {index}")
            mycursor.execute(insert)
            mydb.commit()
            time_spent = x[5]-x[3]
            time_spent = time_spent.total_seconds()/60
            print(time_spent)
            total_hours = int(time_spent/60)
            total_bill = 0
            if time_spent<60:
                total_bill = 50
            if time_spent>60:
                total_bill = 50 + 20*(total_hours)
            print(f'total bill : {total_bill}')
            mycursor.reset()
            mycursor.execute(f"delete from one_a where slot = {index}")
            mydb.commit()
            print("deleted")

        if x[1]=="2A":
            index = x[2]
            one_a[index-1]=0
            print(one_a)
            insert = (f"update entrytable set exit_time=now() where parking_slot = {index}")
            mycursor.execute(insert)
            mydb.commit()
            time_spent = x[5]-x[3]
            time_spent = time_spent.total_seconds()/60
            print(time_spent)
            total_hours = int(time_spent/60)
            total_bill = 0
            if time_spent<60:
                total_bill = 50
            if time_spent>60:
                total_bill = 50 + 20*(total_hours)
            print(f'total bill : {total_bill}')
            mycursor.reset()
            mycursor.execute(f"delete from two_a where slot = {index}")
            mydb.commit()
            print("deleted")

        if x[1]=="3A":
            index = x[2]
            one_a[index-1]=0
            print(one_a)
            insert = (f"update entrytable set exit_time=now() where parking_slot = {index}")
            mycursor.execute(insert)
            mydb.commit()
            time_spent = x[5]-x[3]
            time_spent = time_spent.total_seconds()/60
            print(time_spent)
            total_hours = int(time_spent/60)
            total_bill = 0
            if time_spent<60:
                total_bill = 50
            if time_spent>60:
                total_bill = 50 + 20*(total_hours)
            print(f'total bill : {total_bill}')
            mycursor.reset()
            mycursor.execute(f"delete from three_a where slot = {index}")
            mydb.commit()
            print("deleted")

        if x[1]=="TOWERS":
            index = x[2]
            one_a[index-1]=0
            print(one_a)
            now = datetime.now()
            insert = (f"update entrytable set exit_time='{now}' where parking_slot = {index}")
            mycursor.execute(insert)
            mydb.commit()
            time_spent = x[5]-x[3]
            time_spent = time_spent.total_seconds()/60
            print(time_spent)
            total_hours = int(time_spent/60)
            total_bill = 0
            if time_spent<60:
                total_bill = 50
            if time_spent>60:
                total_bill = 50 + 20*(total_hours)
            print(f'total bill : {total_bill}')
            mycursor.reset()
            mycursor.execute(f"delete from towers where slot = {index}")
            mydb.commit()
            print("deleted")

#     with open("list.csv","w") as fw:
#         writer = csv.writer(fw)
#         writer.writerows(lines)
#         print("\nexit complete\n")
#         exittime = datetime.now()
        # message = client.messages \
        #             .create(
        #                 body=f"your car {number} has left from {choice} , slot {slot} at {exittime}",
        #                 from_='+16232577297',
        #                 to=f'+91{phone_number}'
        #             )
        # print(message.status)

#TESTCASE 1
        #   1,2
        #   2
        #   2,3,4,5
        #   3,4,5
        #   4,5
        #   5

          
# entry(1)
# entry(2)
# entry(3)

entry(4)