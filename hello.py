import customtkinter
from tkinter import *
from PIL import Image , ImageTk
app = customtkinter.CTk()
app.title("entry page")
app.geometry("700x500")
app.config(bg="#000000")

img = 4
number = "HR51BN7411"
# app.winfo_children()[0].destroy()
# for item in app.winfo_children():
#     item.destroy()
canvas = Canvas(app, width=100, height=50, borderwidth=5,
                bg="#000000", highlightthickness=0)
canvas.place(x=20, y=20)
img = (Image.open("./img/logo.png"))
# Resize the Image using resize method
resized_image = img.resize((100, 50), Image.ANTIALIAS)
new_image = ImageTk.PhotoImage(resized_image)
# Add image to the Canvas Items
canvas.create_image(10, 20, anchor=NW, image=new_image)

hello_label = customtkinter.CTkLabel(app, text=f" WELCOME {number}", text_font=(
    'Helvetica bold', 20)).place(x=220, y=100)
user_name = customtkinter.CTkLabel(app, text="PLEASE ENTER YOUR MOBILE NO.", text_font=(
    'Helvetica bold', 16)).place(x=200, y=150)

v = StringVar()
phone_number_area = customtkinter.CTkEntry(app, width=250,
                                             height=25,
                                             textvariable=v,
                                             border_width=2,
                                             corner_radius=10)

phone_number_area.place(x=200, y=200)

def clear():
        app.winfo_children()[0].destroy()
        for item in app.winfo_children():
            item.destroy()
from functools import partial 

phone_number = ""

def button(number):
    content = v.get()
    with open("list.csv" , "w") as f:
        f.write(content)
    
submitbutton = customtkinter.CTkButton(app, command= lambda : button(phone_number_area.get()), text="PROCEEED", text_font="Arial", width=250, fg_color="#b55286", height=10)
submitbutton.place(x=200, y=350)
import csv
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

print(f"phome : {phone_number}" )
app.mainloop()
