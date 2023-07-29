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

import os

dir_path = r'./photos'
count = 0
for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1
print('File count:', count-1)

app = customtkinter.CTk()
app.title("entry page")
app.geometry("700x500")
app.config(bg="#000000")

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

    # cv2.destroyAllWindows()
    # dir_path = r'./photos'
    # count = 0
    # for path in os.listdir(dir_path):
    #     if os.path.isfile(os.path.join(dir_path, path)):
    #         count += 1
    # count = count-1
    img = cv2.imread(f'photos/image{img}.jpg')
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


# parking_area_label = customtkinter.CTkLabel(app, text = "CHOOSE YOUR PARKING AREA" , text_font = ('Helvetica bold', 16)).place(x = 210,y = 250)
    # optionmenu_var = StringVar()
    # def get_choice():
    #     content = optionmenu_var.get()
    #     return content

    # combobox = customtkinter.CTkComboBox(master=app,width=250,height=25,
    #                                  values=["1A", "2A"],
    #                                  variable=optionmenu_var)
    # combobox.place(x=210 , y = 270)
    
    # def get_data():
       
    #     ch = get_choice()
    #     return ch


def entryscreen():
    global phone_number
    img = 4
    number=numberextraction(img)
    # app.winfo_children()[0].destroy()
    # for item in app.winfo_children():
    #     item.destroy() 
    # canvas = Canvas(app, width = 100, height = 50 , borderwidth=5 , bg="#000000" , highlightthickness=0)  
    # canvas.place(x=20,y=20) 
    # img= (Image.open("./img/logo.png"))
    #     #Resize the Image using resize method
    # resized_image= img.resize((100,50), Image.ANTIALIAS)
    # new_image= ImageTk.PhotoImage(resized_image)
    #     #Add image to the Canvas Items
    # canvas.create_image(10,20, anchor=NW, image=new_image)

    hello_label = customtkinter.CTkLabel(app , text=f" WELCOME {number}" , text_font = ('Helvetica bold', 20)).place(x = 220 , y = 100)
    user_name = customtkinter.CTkLabel(app, text = "PLEASE ENTER YOUR MOBILE NO." , text_font = ('Helvetica bold', 16)).place(x = 200,y = 150)
        
    v = StringVar() 
    phone_number_area = customtkinter.CTkEntry(app, textvariable=v , width=250,
                                height=25,
                                border_width=2,
                                corner_radius=10)

    phone_number_area.place(x=200,y=200)
    
    def clear():
        app.winfo_children()[0].destroy()
        for item in app.winfo_children():
             item.destroy() 
    optionmenu_var = StringVar()     
    
    def button(number):
            content = v.get()
            choice_content = optionmenu_var.get()
            with open("list.csv" , "w") as f:
                f.write(f"{content},{choice_content}")
    
        
    submitbutton = customtkinter.CTkButton(app, command = lambda : button(phone_number_area.get()),text="PROCEEED",text_font="Arial" , width=250 , fg_color="#b55286",height=10)
    submitbutton.place(x=200,y=350)
    parking_area_label = customtkinter.CTkLabel(app, text = "CHOOSE YOUR PARKING AREA" , text_font = ('Helvetica bold', 16)).place(x = 210,y = 250)
    combobox = customtkinter.CTkComboBox(master=app,width=250,height=25,
                                     values=["1A", "2A" , "3A" , "TOWERS"],
                                     variable=optionmenu_var)
    combobox.place(x=210 , y = 270)
    with open('list.csv', mode ='r') as file:   
       csvFile = csv.reader(file)
       for lines in csvFile:
            phone_number = lines[0]
    # hello_label = customtkinter.CTkLabel(app , text=f" WELCOME {number}" , text_font = ('Helvetica bold', 20)).place(x = 220 , y = 100)
    # user_name = customtkinter.CTkLabel(app, text = "PLEASE ENTER THE SLOT YOU WANT TO GO TO" , text_font = ('Helvetica bold', 16)).place(x = 200,y = 150)
        
    # v = StringVar() 
    # choice_area = customtkinter.CTkEntry(app, textvariable=v , width=250,
    #                             height=25,
    #                             border_width=2,
    #                             corner_radius=10)

    # choice_area.place(x=200,y=200)
    # def get_choice():
    #         content = v.get()
    #         return content
     
    print(f"phone number : {phone_number}")
    app.mainloop()
    return phone_number

def entry():

    global parkedcars
    global fullslots
    global one_a,two_a,three_a,towers
    
    img = 4
    number=numberextraction(img)
    choice = input("enter choice :")
    if(choice=="1A"):
            right_one_a = []
            left_one_a = []


            for i in range(int(len(one_a)/2)):
                left_one_a.append(int(one_a[i]))

            # print(left_one_a)
            first_empty_slot_left = left_one_a.index(0)
            # print(first_empty_slot_left)

            for i in range(int(len(one_a)/2),len(one_a)):
                right_one_a.append(int(one_a[i]))

            first_empty_slot_right = right_one_a.index(0)
            # print(right_one_a)
            # print(first_empty_slot_right)

            if(first_empty_slot_left>first_empty_slot_right):
                right_one_a[first_empty_slot_right] = 1
                slot = first_empty_slot_right+len(left_one_a)-1

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

            # message = client.messages \
            #         .create(
            #             body=f"your car {number} has been parked in {choice} in the slot {slot} at {entrytime}",
            #             from_='+16232577297',
            #             to=f'+91{phone_number}'
            #         )
            # print(message.status)
        
def removespaces(string):
    return string.replace(" ", "")

def homescreen():
    canvas = Canvas(app, width = 400, height = 100 , borderwidth=5 , bg="#000000" , highlightthickness=0)  
    canvas.pack() 
    img= (Image.open("./img/logo.png"))
        #Resize the Image using resize method
    resized_image= img.resize((400,100), Image.ANTIALIAS)
    new_image= ImageTk.PhotoImage(resized_image)
        #Add image to the Canvas Items
    canvas.create_image(10,20, anchor=NW, image=new_image)

    entrybutton = customtkinter.CTkButton(app,command = entry , text="ENTRY",text_font="Arial" , width=250 , fg_color="#b55286",height=10)
    entrybutton.place(x=200,y=200)
    exitbutton = customtkinter.CTkButton(app,text="EXIT",text_font="Arial" , width=250 , fg_color="#b55286",height=10)
    exitbutton.place(x=200,y=300)

entryscreen()
