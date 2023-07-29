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
import customtkinter
import tkinter as tk
from tkinter import *
from PIL import Image , ImageTk

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
two_a = [0]*8
three_a = [0]*6
towers = [0]*6

mycursor.execute("select * from one_a;")
count = mycursor.rowcount

for x in mycursor: 
    count = count+1
mycursor.reset()

app = customtkinter.CTk()
app.title("entry page")
app.geometry("700x500")
app.config(bg="#000000")

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
            three_a_array.append(int(three_a_list_string[i]))

            
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

import os

dir_path = r'./photos'
count = 0
for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1



def numberextraction():
    dir_path = r'./photos'
    count = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            count += 1
    count = count-1
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
        
            img_name = f"photos/image{count+1}.jpg".format(count)
            cv2.imwrite(img_name, frame)
            print(f"{img_name} written!")
            count = count+1
    cam.release()

    cv2.destroyAllWindows()
    img = cv2.imread(f'photos/image{4}.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))

    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection
    plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))

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
    plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))

    (x,y) = np.where(mask==255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))

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


def entry():
    global parkedcars
    global fullslots
    global one_a,two_a,three_a,towers
    import random
    number=numberextraction()
    app.winfo_children()[0].destroy()
    for item in app.winfo_children():
             item.destroy() 
    canvas = Canvas(app, width=700, height=400,borderwidth=5 , highlightthickness=0 , bg="#202020")
    canvas.place(x=0, y=100)
    hello_label = customtkinter.CTkLabel(app , text=f" WELCOME {number}" , text_font = ('Arial', 24)).place(x = 200 , y = 60)
    user_name = customtkinter.CTkLabel(app, text = "PLEASE ENTER YOUR MOBILE NO." ,bg_color="#202020", text_font = ('Arial', 16)).place(x = 200,y = 150)
        
    v = StringVar() 
    phone_number_area = customtkinter.CTkEntry(app, textvariable=v , width=250,
                                height=30,
                                border_width=2,
                                corner_radius=10)

    phone_number_area.place(x=200,y=200)
    optionmenu_var = StringVar()     
    
    phone_number = "8383096694"
    parking_area_label = customtkinter.CTkLabel(app, text = "CHOOSE YOUR PARKING AREA" ,bg_color="#202020", text_font = ('ARIAL', 16)).place(x = 200,y = 280)
    combobox = customtkinter.CTkComboBox(master=app,width=250,height=30,
                                     values=["1A", "2A" , "3A" , "TOWERS"],
                                     variable=optionmenu_var)
    combobox.place(x=200 , y = 330)
    submitbutton = customtkinter.CTkButton(app ,text="PROCEEED",text_font="Arial" , width=250 , bg_color= "#3B3B3B" , fg_color="#E44E0C",height=40)
    submitbutton.place(x=200,y=390)

    choice = input("enter choice :")
    if(choice=="1A"):
        right_one_a = []
        left_one_a = []

        for i in range(int(len(one_a)/2)):
                    left_one_a.append(int(one_a[i]))
        first_empty_slot_left = left_one_a.index(0)
                

        for i in range(int(len(one_a)/2), len(one_a)):
                    right_one_a.append(int(one_a[i]))

        first_empty_slot_right = right_one_a.index(0)
        
        if(first_empty_slot_left > first_empty_slot_right):
                    right_one_a[first_empty_slot_right] = 1
                    slot = first_empty_slot_right+len(left_one_a)

        if(first_empty_slot_left <= first_empty_slot_right):
                    left_one_a[first_empty_slot_left] = 1
                    slot = first_empty_slot_left

        one_a = np.concatenate([left_one_a, right_one_a])
        app.winfo_children()[0].destroy()
        for item in app.winfo_children():
            item.destroy() 
        number_label = customtkinter.CTkLabel(app , text=f"CAR NUMBER : {number}" , text_font = ('arial', 20)).place(x = 400 , y = 100)
        slot_label = customtkinter.CTkLabel(app , text=f"SLOT ALLOTED : {slot+1}" , text_font = ('arial', 20)).place(x = 400 , y = 130)
        area_label = customtkinter.CTkLabel(app , text=f"PARKING AREA : 1A" , text_font = ('aRIAL', 20)).place(x = 80 , y = 100)
        number_label = customtkinter.CTkLabel(app , text=f"ENTRY FROM HERE" , text_font = ('arial', 15)).place(x = 13 , y = 250)
        canvas = Canvas(app, width=400, height=200,borderwidth=5 , highlightthickness=0 , bg="#000000")
        canvas.place(x=180, y=200)
        x = 10
        y = 10
        i=0
        for i in range(len(left_one_a)):
            if i == slot and slot<len(one_a)/2:
                color = "green"
            else:
                color = "black"
            canvas.create_rectangle(x,y,x+70,y+70,outline = "orange", fill = color,width = 2)
            x = x+100
        x = 10
        y = 90
        for i in range(int(len(right_one_a))):
            if i == slot-len(left_one_a) and slot>=len(one_a)/2:
                color = "green"
            else:
                color = "black"
            canvas.create_rectangle(x,y,x+70,y+70,outline = "orange", fill = color ,width = 2)
            x = x+100
        
    if(choice=="2A"):
        right_two_a = []
        left_two_a = []


        for i in range(int(len(two_a)/2)):
            left_two_a.append(int(two_a[i]))

        
        first_empty_slot_left_two_a = left_two_a.index(0)
    

        for i in range(int(len(two_a)/2),len(two_a)):
            right_two_a.append(int(two_a[i]))

        first_empty_slot_right_two_a = right_two_a.index(0)
    

        if(first_empty_slot_left>first_empty_slot_right):
            right_two_a[first_empty_slot_right_two_a] = 1

        if(first_empty_slot_left<=first_empty_slot_right):
            left_two_a[first_empty_slot_left_two_a] = 1

        two_a = np.concatenate([left_two_a,right_two_a])
       
       

    if(choice=="3A"):
        right_three_a = []
        left_three_a = []


        for i in range(int(len(three_a)/2)):
            left_one_a.append(int(three_a[i]))

       
        first_empty_slot_left_three_a = left_three_a.index(0)
       

        for i in range(int(len(three_a)/2),len(three_a)):
            right_three_a.append(int(three_a[i]))

        first_empty_slot_right_three_a = right_three_a.index(0)
       
        if(first_empty_slot_left_three_a>=first_empty_slot_right_three_a):
            right_three_a[first_empty_slot_left_three_a] = 1

        if(first_empty_slot_left_three_a<first_empty_slot_right_three_a):
            left_three_a[first_empty_slot_left_three_a] = 1

        three_a = np.concatenate([left_three_a,right_three_a])


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
      

        if(first_empty_slot_left_towers>=first_empty_slot_right_towers):
            right_towers[first_empty_slot_left_towers] = 1

        if(first_empty_slot_left_towers<first_empty_slot_right_towers):
            left_towers[first_empty_slot_left_towers] = 1

        one_a = np.concatenate([left_towers,right_towers])
    
        
    def removespaces(string):
        return string.replace(" ", "")

    number = removespaces(number)
    now = datetime.now()
    insert = f"insert into entrytable(car_number,parking_area,parking_slot,entry_time,mobile_number) values (%s,%s,%s,%s,%s)"
    val = (number , choice , slot+1 , now, phone_number)
    mycursor.execute(insert , val)
    mydb.commit()
    number_label = customtkinter.CTkLabel(app , text=f"ENTRY GRANTED" , text_font = ('arial', 20)).place(x = 200 , y = 400)
    print("ENTRY GRANTED!!")

    message = client.messages \
                    .create(
                        body=f"your car {number} has been parked in {choice} in the slot {slot+1} at {now}",
                        from_='+16232577297',
                        to=f'+91{8383096694}'
                    )
    print(message.status)


    if choice == "1A":
        insert = f"insert into one_a(car_number,slot,entry_time,mobile_number) values (%s,%s,%s,%s)"
        val = (number , slot+1 , now, phone_number)
        mycursor.execute(insert , val)
        mydb.commit()
    
    if choice == "2A":
        insert = f"insert into two_a(car_number,slot,entry_time,mobile_number) values (%s,%s,%s,%s)"
        val = (number , slot+1 , now, phone_number)
        mycursor.execute(insert , val)
        mydb.commit()

    if choice == "3A":
        insert = f"insert into three_a(car_number,slot,entry_time,mobile_number) values (%s,%s,%s,%s)"
        val = (number , slot+1 , now, phone_number)
        mycursor.execute(insert , val)
        mydb.commit()

    if choice == "TOWERS":
        insert = f"insert into towers(car_number,slot,entry_time,mobile_number) values (%s,%s,%s,%s)"
        val = (number , slot+1 , now, phone_number)
        mycursor.execute(insert , val)
        mydb.commit()


def removespaces(string):
    return string.replace(" ", "")

def exitcar():
    img = 4
    number=numberextraction()
    number = removespaces(number)
    mycursor.reset()
    mycursor.execute(f"select * from entrytable where car_number ='{number}'")
    myresult = mycursor.fetchall()
    app.winfo_children()[0].destroy()
    for item in app.winfo_children():
             item.destroy() 
    for x in myresult:
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
            
    #         img = (Image.open("./img/logo.png"))
    # # Resize the Image using resize method
    #         resized_image = img.resize((400, 100))
    #         new_image = ImageTk.PhotoImage(resized_image)
    # # Add image to the Canvas Items
            # canvas.create_image(0, 0,anchor = "nw", image=new_image)
            canvas = Canvas(app, width=700, height=400, borderwidth=5 , highlightthickness=0 , bg="#202020")
            canvas.place(x=0, y=100)
            number_label = customtkinter.CTkLabel(app , text=f"THANKYOU FOR YOUR VISIT" , text_font = ('arial', 35)).place(x = 100 , y = 50)
            number_label = customtkinter.CTkLabel(app , text=f"CAR NUMBER : {number}" ,  bg_color="#202020" ,text_font = ('arial', 25)).place(x = 70 , y = 180)
            number_label = customtkinter.CTkLabel(app , text=f"TIME SPENT : {time_spent}" , bg_color="#202020", text_font = ('arial', 25)).place(x = 70 , y = 230)
            number_label = customtkinter.CTkLabel(app , text=f"TOTAL BILL : {total_bill}" , bg_color="#202020", text_font = ('arial', 25)).place(x = 70 , y = 280)


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

            message = client.messages \
                    .create(
                        body=f"your car {number} was removed from {choice} , slot {index + 1}. total time spent = {time_spent} , total bill = {total_bill}",
                        from_='+16232577297',
                        to=f'+91{8383096694}'
                    )
            print(message.status)


def homescreen():
    entrybutton = customtkinter.CTkButton(
        app, text="ENTRY", text_font="Arial",command=entry, width=300 , height = 50,  bg_color= "#3B3B3B" , fg_color="#E44E0C")
    entrybutton.place(x=200, y=270)
    exitbutton = customtkinter.CTkButton(
        app, text="EXIT", text_font="Arial",command=exitcar ,width=300,height = 50, bg_color = "#3b3b3b", fg_color="#E44E0C")
    exitbutton.place(x=200, y=330)
        
canvas = Canvas(app, width=400, height=100, borderwidth=5 , bg="#000000", highlightthickness=0)
canvas.place(x=120, y=100)
img = (Image.open("./img/logo.png"))
resized_image = img.resize((400, 100))
new_image = ImageTk.PhotoImage(resized_image)
canvas.create_image(0, 0,anchor = "nw", image=new_image)
homescreen()

app.mainloop()
