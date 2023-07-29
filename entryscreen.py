import customtkinter
import csv
from tkinter import *
from PIL import Image, ImageTk
app = customtkinter.CTk()
app.title("entry page")
app.geometry("700x500")
app.config(bg="#000000")
number = "HR51BN7411"
# hello_label = customtkinter.CTkLabel(app, text=f" WELCOME {number}", text_font=(
#     'Helvetica bold', 20)).place(x=220, y=100)
# user_name = customtkinter.CTkLabel(app, text="PLEASE ENTER YOUR MOBILE NO.", text_font=(
#     'Helvetica bold', 16)).place(x=200, y=150)

# v = StringVar()
# phone_number_area = customtkinter.CTkEntry(app, textvariable=v, width=250,
#                                              height=25,
#                                              border_width=2,
#                                              corner_radius=10)

# phone_number_area.place(x=200, y=200)

# def clear():
#         app.winfo_children()[0].destroy()
#         for item in app.winfo_children():
#             item.destroy()
# optionmenu_var = StringVar()
# import pandas as pd
# csvopen1 = pd.read_csv('list.csv')

# def button(number):
#         content = v.get()
#         choice_content = optionmenu_var.get()
#         with open("list.csv", "a") as f:
#             f.writelines(f"{content},{choice_content}\n")

# submitbutton = customtkinter.CTkButton(app, command= lambda: button(phone_number_area.get()), text="PROCEEED", text_font="Arial", width=250, fg_color="#b55286", height=10)
# submitbutton.place(x=200, y=350)
# parking_area_label = customtkinter.CTkLabel(app, text="CHOOSE YOUR PARKING AREA", text_font=('Helvetica bold', 16)).place(x= 210, y = 250)
# combobox = customtkinter.CTkComboBox(master=app, width=250, height=25,
#                                          values=["1A", "2A", "3A", "TOWERS"],
#                                          variable=optionmenu_var)
# combobox.place(x=210, y=270)
# phone_number = ''
# import time
# app.mainloop()
# csvopen2 = pd.read_csv('list.csv')
# while(len(csvopen1)==len(csvopen2)):
#     print("into wait")
#     time.sleep(1)
# with open('list.csv', mode='r+') as file:
#         csvFile = csv.reader(file)
#         for lines in csvFile:
#             phone_number = lines
#     # hello_label = customtkinter.CTkLabel(app , text=f" WELCOME {number}" , text_font = ('Helvetica bold', 20)).place(x = 220 , y = 100)
#     # user_name = customtkinter.CTkLabel(app, text = "PLEASE ENTER THE SLOT YOU WANT TO GO TO" , text_font = ('Helvetica bold', 16)).place(x = 200,y = 150)

#     # v = StringVar()
#     # choice_area = customtkinter.CTkEntry(app, textvariable=v , width=250,
#     #                             height=25,
#     #                             border_width=2,
#     #                             corner_radius=10)

#     # choice_area.place(x=200,y=200)
#     # def get_choice():
#     #         content = v.get()
#     #         return content

# print(f"phone number : {phone_number}")

canvas = Canvas(app, width=400, height=100, borderwidth=5 , bg="#000000", highlightthickness=0)
canvas.place(x=120, y=100)
img = (Image.open("./img/logo.png"))
# Resize the Image using resize method
resized_image = img.resize((400, 100))
new_image = ImageTk.PhotoImage(resized_image)
# Add image to the Canvas Items
canvas.create_image(0, 0,anchor = "nw", image=new_image)
entrybutton = customtkinter.CTkButton(
    app, text="ENTRY", text_font="Arial", width=300 , height = 50,  bg_color= "#3B3B3B" , fg_color="#E44E0C")
entrybutton.place(x=200, y=270)
exitbutton = customtkinter.CTkButton(
    app, text="EXIT", text_font="Arial", width=300,height = 50, bg_color = "#3b3b3b", fg_color="#E44E0C")
exitbutton.place(x=200, y=330)

app.mainloop()