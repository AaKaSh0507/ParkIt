from datetime import datetime
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import os
from twilio.rest import Client
import csv
import pandas as pd

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

fullslots = 0
left=[0]*4

def numberextraction(img):
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


def entry(img):

    global parkedcars
    global fullslots
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
    choice = input(f"\n\nwhere do you want to park?\n1A\n2A\n3A\nTowers\nenter : ")
    if(choice=="1A"):
        if(left[0]%2==0 and carentry ==0):
                for i in range(0,int(len(one_a)/2)-1):
                    if(one_a[i]==0):
                        one_a[i]=1
                        left[0] = 1
                        fullslots = fullslots+1
                        carentry=1
                        slot = i
                        print(one_a)
                        break      
        if(left[0]%2!=0 and carentry==0):
                for i in range(int(len(one_a)/2),int(len(one_a)-1)):
                    if(one_a[i]==0):
                        one_a[i]=1
                        left[0] = 0
                        fullslots = fullslots+1
                        carentry=1
                        slot = i
                        print(one_a)
                        break
        carentry = 0



    if(choice=="2A"):
        if(left[1]%2==0 and carentry ==0):
                for i in range(0,int(len(two_a)/2)-1):
                    if(two_a[i]==0):
                        two_a[i]=1
                        left[1] = 1
                        fullslots = fullslots+1
                        carentry=1
                        slot = i
                        print(two_a)
                        break      
        if(left[1]%2!=0 and carentry==0):
                for i in range(int(len(two_a)/2),int(len(two_a)-1)):
                    if(two_a[i]==0):
                        two_a[i]=1
                        left[1] = 0
                        fullslots = fullslots+1
                        carentry=1
                        slot = i
                        print(two_a)
                        break
        carentry = 0


    if(choice=="3A"):
        if(left[2]%2==0 and carentry ==0):
                for i in range(0,int(len(three_a)/2)-1):
                    if(three_a[i]==0):
                        three_a[i]=1
                        left[2] = 1
                        fullslots = fullslots+1
                        carentry=1
                        slot = i
                        print(three_a)
                        break      
        if(left[2]%2!=0 and carentry==0):
                for i in range(int(len(three_a)/2),int(len(three_a)-1)):
                    if(three_a[i]==0):
                        three_a[i]=1
                        left[2] = 0
                        fullslots = fullslots+1
                        carentry=1
                        slot = i
                        print(three_a)
                        break
        carentry = 0



    if(choice=="TOWERS"):
        if(left[3]%2==0 and carentry ==0):
                for i in range(0,int(len(towers)/2)-1):
                    if(towers[i]==0):
                        towers[i]=1
                        left[3] = 1
                        fullslots = fullslots+1
                        carentry=1
                        slot = i
                        print(towers)
                        break      
        if(left[3]%2!=0 and carentry==0):
                for i in range(int(len(towers)/2),int(len(towers)-1)):
                    if(towers[i]==0):
                        towers[i]=1
                        left[3] = 0
                        fullslots = fullslots+1
                        carentry=1
                        slot = i
                        print(towers)
                        break
        carentry = 0



    with open("list.csv","r+") as f:
        mydatalist=f.readlines()
        numberlist = []
        for line in mydatalist:
            entry = line.split(',')
            numberlist.append(entry[0])
        if number not in numberlist:
            now = datetime.now()
            entrytime = now.strftime('%H:%M:%S')
            f.writelines(f"\n{parkedcars},{number},{choice},{entrytime},{slot+1},{phone_number}")
            message = client.messages \
                    .create(
                        body=f"your car {number} has been parked in {choice} in the slot {slot} at {entrytime}",
                        from_='+16232577297',
                        to=f'+91{phone_number}'
                    )
            print(message.status)

def exitcar(img):
    global parkedcars
    number=numberextraction(img)
    lines = list()

    print("exit car running")

    with open("list.csv","r") as f:
        reader = csv.reader(f)
        for row in reader:
           lines.append(row)
           for items in row:
             if items == number:
                if row[2]=="1A":
                    one_a[int(row[4])-1] = 0
                    print(one_a)
                elif row[2]=="2A":
                    two_a[int(row[4])-1] = 0
                    print(two_a)
                elif row[3]=="3A":
                    three_a[int(row[4])-1] = 0
                    print(three_a)
                elif row[2]=="TOWERS":
                     towers[int(row[4])-1] = 0
                     print(towers)
                
                lines.remove(row)
                for items in row:
                    row[0] = int(row[0])-1

    with open("list.csv","w") as fw:
        writer = csv.writer(fw)
        writer.writerows(lines)

entry(1)
entry(2)
exitcar(1)
entry(3)
exitcar(2)
entry(4)
entry(5)
exitcar(3)
exitcar(4)
exitcar(5)



