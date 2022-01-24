# -*- coding: utf-8 -*-
"""
Created on Mon May  3 19:17:53 2021

@author: Anway
"""
from tkinter import *
#from tkinter.ttk import *
from tkinter import Text
import tkinter.filedialog as file
import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk
import numpy 
import tkinter.messagebox
import collections

data_length = 0
max_data = 0
img1 = numpy.ndarray
img2 = numpy.ndarray
max_freq_intensity = 0

def Display_Data_Size():
    global data_length
    data = text_entry.get("1.0", "end-1c") 
    data_length = len(data) * 8           #+1 for the delimeter
    if(data_length>max_data):
        data_label['fg'] = '#FF0000'
    else:
        data_label['fg'] = 'white'
    data_label['text'] = "Data Size: " + str(data_length)
    root.after(1, Display_Data_Size)
    #print(data_length)

def Display_Shared_Key():
    global max_freq_intensity
    key = key_entry.get()
    public_key_label['text'] = "Shared Key: " + str(max_freq_intensity)+"#"+key
    root.after(1, Display_Shared_Key)
    
def Upload_IMG():
    global max_data
    global img1
    #global img, image, FilePath
    FilePath = file.askopenfilename()
    
    img = Image.open(FilePath)
    img1 = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    resized_img = img.resize(Dim(img, height=300))
    canvas.image = ImageTk.PhotoImage(resized_img)
    canvas.create_image(200,150, image=canvas.image, anchor='center')
    
    max_data = img.size[0]*img.size[1]*3//8
    print(img.size)
    max_data_label['text'] = "Max Data: " + str(max_data)
    return 0

    
def Dim(image, width = None, height = None):
    dim = None
    w, h = image.size
    
    if width is None and height is None:
        return image
    
    elif height is None:
        r = width/float(w) #ratio of new width to old width.
        dim = (width, int(h*r))
        
    elif width is None:
        r = height/float(h)
        dim = (int(w * r), height)
        
    return dim

def Encode():
    global max_freq_intensity
    if(data_length==0):
        tkinter.messagebox.showinfo("Empty Data", "PLease enter text")
        return
    
    if(not delimeter_entry.get()):
        tkinter.messagebox.showinfo("No Key", "PLease enter a key")
        return
    
    data = (text_entry.get("1.0", "end-1c")) + delimeter_entry.get()
    data_binary = "".join([format(ord(i), "08b") for i in data])
    print(data_binary)

    data_encoded_count = 0
    empty_list = []
    for values in range(0,img1.shape[0]):
        for pixel in range(0,img1.shape[1]):
            empty_list.append(img1[values][pixel][0])  
    
    counter = collections.Counter(empty_list)
    counter = dict(counter)
    max_frequency = max(counter.values())
    print("Max Frequency",max_frequency)
    max_freq_intensity = list(counter.keys())[list(counter.values()).index(max_frequency)]
    print("Max Intensity",max_freq_intensity)

    key = key_entry.get()
    key = str(max_freq_intensity) + "#" + key
    print("Use key ", key)

    #print(img1[0])
    for values in range(0,img1.shape[0]):
        for pixel in range(0,img1.shape[1]):
            #pixel_binary = [i for i in pixel]
            #r,g,b = pixel_binary
            r = img1[values][pixel][0]
            if r > max_freq_intensity:
                #print(r)
                img1[values][pixel][0] = r+1
    #print(img1[0])

    for values in range(0,img1.shape[0]):
        for pixel in range(0,img1.shape[0]):
            r = img1[values][pixel][0]
            if r == max_freq_intensity:
                #print(pixel.where)
                if int(data_binary[data_encoded_count]) == 0:
                    data_encoded_count += 1
                    #print("0", data_encoded_count,values,pixel)
                elif int(data_binary[data_encoded_count]) == 1:
                    img1[values][pixel][0] = r + 1
                    data_encoded_count += 1
                    #print("1", data_encoded_count, values,pixel)
                if data_encoded_count>=(len(data_binary)):
                    print("data_encoded_count_limit_reached",data_encoded_count)
                    break
        if data_encoded_count>=(len(data_binary)):
            print("data_encoded_count_limit_reached",data_encoded_count)
            break

    save_img_window = Tk()
    save_img_window.title("Save Image")
    save_img_window.configure(background='#34A853')
        
    stego_img = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    stego_img_pil = Image.fromarray(stego_img)
    stego_img_pil_resized = stego_img_pil.resize(Dim(stego_img_pil, height=300))
    stego_img_pil_resized = ImageTk.PhotoImage(stego_img_pil_resized, master = save_img_window)
    
    img_label = Label(save_img_window, image=stego_img_pil_resized)
    img_label.image = stego_img_pil_resized
    img_label.pack()
    
    save_button = Button(save_img_window, text = 'Save', bg = 'white',
                         command=lambda: Save_Stego_Img(stego_img_pil))
    save_button.pack()
    
    def Save_Stego_Img(img_save):
        img_save = img_save.save("stego_object.png")
        save_img_window.destroy()
        
    save_img_window.mainloop()
    return
    
def Decode_Window():
    decode_window = Tk()
    decode_window.title("Steganography")
    decode_window.geometry("1000x600")
    decode_window.configure(background='#474747')
    decode_window.resizable(width = False, height=False)
    #decode_window.iconbitmap('icon.ico')
    global img2
    
    def Upload_Decode_IMG():
        global img2
        FilePath2 = file.askopenfilename()
        img2_canvas = Image.open(FilePath2)
        img2 = cv2.cvtColor(numpy.array(img2_canvas), cv2.COLOR_RGB2BGR)
        resized_img2 = img2_canvas.resize(Dim(img2_canvas, height=300))
        canvas1.image = ImageTk.PhotoImage(resized_img2, master = decode_window)
        canvas1.create_image(200,150, image=canvas1.image, anchor='center')
        return
    
    def Decode_Data():
        global img2
        
        entered_del = delimeter_entry1.get()
        print(entered_del)
        entered_key = key_entry1.get()

        key_intensity = int(entered_key.split('#')[0])
        entered_key = entered_key.split('#')[1]
        print("key_intensity", key_intensity)

        if(type(img2) == type):
            tkinter.messagebox.showinfo("No Image",
                                       "Please Upload an Image")
            return
        
        if(len(entered_del)==0):
            tkinter.messagebox.showinfo("No Delimeter",
                                       "Please Enter Delimeter")
            return
        
        if(len(entered_key)==0):
            tkinter.messagebox.showinfo("No Key",
                                       "Please Enter Key")
            return
        
        original_del = delimeter_entry.get()
        
        if(original_del != entered_del):
            tkinter.messagebox.showinfo("Wrong Delimeter",
                                        "Delimeter does not match")
            return
        
        original_key = key_entry.get()
        
        if(original_key != entered_key):
            tkinter.messagebox.showinfo("Wrong Key",
                                        "Key does not match")
            return
        


        data_decoded_count = 0
        binary_decoded_string = ""
        decoded_string = ""
        flag = 0
        char_set = 0
        for values in range(0,img2.shape[0]):
            for pixel in range(0,img2.shape[1]):
                #pixel_binary = [i for i in pixel]
                #r, g, b = pixel_binary
                r = img2[values][pixel][0]
                if r == key_intensity:
                    binary_decoded_string += '0'
                    data_decoded_count += 1
                    char_set = 1
                if r == key_intensity + 1:
                    binary_decoded_string += '1'
                    data_decoded_count += 1
                    char_set = 1
                if data_decoded_count%8 == 0 and char_set == 1:
                    print(data_decoded_count)
                    if binary_decoded_string != "":
                        char_byte = binary_decoded_string[data_decoded_count-8:data_decoded_count]
                        character = chr(int(char_byte, 2))
                        char_ascii = int(char_byte, 2)
                        char_set = 0
                        if char_ascii<32 or char_ascii>127 or character==entered_del :
                            flag = 1
                            char_set = 0
                            break
                        else:
                            decoded_string += character
                            print(character)
                            
            if flag == 1:
                break


        print(binary_decoded_string)
        print(decoded_string)
        
        
        print(decoded_string)
        decoded_text_entry.delete('1.0', END)
        decoded_text_entry.insert('1.0', decoded_string)
        
        return
    
    title = Label(decode_window,font=("Alegreya Sans Bold", 25),
                  text="Image Steganography Tool\nDecode Window",
                  bg='#474747', fg='#FFFFFF')
    title.pack()
    
    image_label = Label(decode_window, text="Stego Object: ", bg='#474747',
                        fg='#FFFFFF', font=("Alegreya Sans Bold", 15))
    image_label.pack()
    image_label.place(anchor = "w", relx = 0.05, y = 120)
    
    canvas1 = Canvas(decode_window, bg = 'white', height = 300, width = 400)
    canvas1.pack()
    canvas1.place(anchor='center', relx = 0.25, y = 300)
    
    upload_button = Button(decode_window, text="Upload Image",
                           font=("Alegreya Sans Bold", 10),
                           fg = '#474747', bg = 'white',
                           command = Upload_Decode_IMG)
    upload_button.pack()
    upload_button.place(anchor = "center",
                        relx = 0.25, y = 500,
                        height = 30, width = 90)
    
    delimeter_label1 = Label(decode_window, text="Enter Delimiter (Key): ",
                             bg='#474747', fg='#FFFFFF',
                             font=("Alegreya Sans Bold", 15))
    delimeter_label1.pack()
    delimeter_label1.place(anchor = "w", relx = 0.60, y = 140)
    
    delimeter_entry1 = Entry(decode_window)
    delimeter_entry1.pack()
    delimeter_entry1.place(anchor = "w", relx = 0.60, y = 170)
    
    key_label1 = Label(decode_window, text="Enter Key: ", bg='#474747',
                   fg='#FFFFFF', font=("Alegreya Sans Bold", 15))
    key_label1.pack()
    key_label1.place(anchor = "w", relx = 0.85, y = 140)
    
    key_entry1 = Entry(decode_window)
    key_entry1.pack()
    key_entry1.place(anchor = "w", relx = 0.85, y = 170)
    
    decode_button = Button(decode_window, text="Decode Data",
                       font=("Alegreya Sans Bold", 10),
                       fg = '#474747', bg = 'white',
                       command = Decode_Data)
    decode_button.pack()
    decode_button.place(anchor = "w", relx = 0.60,
                        y = 220, height = 20, width = 110)
    
    decoded_text_label = Label(decode_window, text="Decoded Text: ",
                               bg='#474747', fg='#FFFFFF',
                               font=("Alegreya Sans Bold", 15))
    decoded_text_label.pack()
    decoded_text_label.place(anchor = "w", relx = 0.60, y = 260)
    
    decoded_text_entry = Text(decode_window, width = 40, height = 7, font=("Alegreya Sans", 10))
    decoded_text_entry.pack()
    decoded_text_entry.place(anchor = "w", relx = 0.60, y = 340)
    
    decode_window.mainloop()

def clear_text():
    text_entry.delete('1.0', END)
    
root = Tk()
root.title("Steganography")
root.geometry("1000x600")
root.configure(background='#34A853')
#root.iconbitmap('icon.ico')
#window_logo = PhotoImage(file = '32x32.png')
#print(window_logo)
#root.iconphoto(False, window_logo)
#root.tk.call('wm', 'iconphoto', root._w, window_logo)
#root.attributes('-fullscreen', True)
#root.bind("<Escape>", lambda event: main_window.attributes
                 #("-fullscreen", False))
root.resizable(width = False, height=False)

title = Label(root, text="Image Steganography Tool", bg='#34A853',
              fg='#FFFFFF', font=("Alegreya Sans Bold", 25))
title.pack()

image_label = Label(root, text="Stego Image: ", bg='#34A853',
                   fg='#FFFFFF', font=("Alegreya Sans Bold", 15))
image_label.pack()
image_label.place(anchor = "w", relx = 0.05, y = 120)

canvas = Canvas(root, bg = 'white', height = 300, width = 400)
canvas.pack()
canvas.place(anchor='center', relx = 0.25, y = 300)

upload_button = Button(root, text="Upload Image",
                       font=("Alegreya Sans Bold", 10),
                       fg = '#34A853', bg = 'white',
                       command = Upload_IMG)
upload_button.pack()
upload_button.place(anchor = "center", relx = 0.25, y = 500,
                    height = 30, width = 90)

enter_text_label = Label(root, text="Enter Text: ", bg='#34A853',
                         fg='#FFFFFF', font=("Alegreya Sans Bold", 15))
enter_text_label.pack()
enter_text_label.place(anchor = "w", relx = 0.60, y = 120)

text_entry = Text(root, width = 40, height = 7, font=("Alegreya Sans", 10))
text_entry.pack()
text_entry.place(anchor = "w", relx = 0.60, y = 200)

delimeter_label = Label(root, text="Enter Delimiter: ", bg='#34A853',
                   fg='#FFFFFF', font=("Alegreya Sans Bold", 15))
delimeter_label.pack()
delimeter_label.place(anchor = "w", relx = 0.60, y = 370)

delimeter_entry = Entry(root)
delimeter_entry.pack()
delimeter_entry.place(anchor = "w", relx = 0.60, y = 400)

key_label = Label(root, text="Enter Key: ", bg='#34A853',
                   fg='#FFFFFF', font=("Alegreya Sans Bold", 15))
key_label.pack()
key_label.place(anchor = "w", relx = 0.80, y = 370)

key_entry = Entry(root)
key_entry.pack()
key_entry.place(anchor = "w", relx = 0.80, y = 400)

public_key_label = Label(root, text="Shared Key: ", bg='#34A853',
                   fg='#FFFFFF', font=("Alegreya Sans Bold", 13))
public_key_label.pack()
public_key_label.place(anchor = "w", relx = 0.80, y = 450)

data_label = Label(root, text = "Data Size: " + str(data_length), 
                   font=("Alegreya Sans Bold", 10),
                   bg='#34A853', fg='#FFFFFF')
data_label.pack()
data_label.place(anchor = "w", relx = 0.8, y = 280)

max_data_label = Label(root, text = "Max Data: " + str(max_data),
                       font=("Alegreya Sans Bold", 10),
                       bg='#34A853', fg='#FFFFFF')

max_data_label.pack()
max_data_label.place(anchor = "w", relx = 0.8, y = 300)


encode_button = Button(root, text="Encode Data",
                       font=("Alegreya Sans Bold", 10),
                       fg = '#34A853', bg = 'white',
                       command = Encode)
encode_button.pack()
encode_button.place(anchor = "w", relx = 0.60, y = 450,
                    height = 20, width = 90)

decode_button = Button(root, text="Decode Window",
                       font=("Alegreya Sans Bold", 10),
                       fg = '#34A853', bg = 'white',
                       command = Decode_Window)
decode_button.pack()
decode_button.place(anchor = "w", relx = 0.70,
                    y = 500, height = 20, width = 110) 

clear_button = Button(root, text="Clear Text",
                      font=("Alegreya Sans Bold", 10),
                      fg = '#34A853', bg = 'white',
                      command = clear_text)
clear_button.pack()
clear_button.place(anchor = "w", relx = 0.60, y = 280,
                   height = 20, width = 90) 

Display_Data_Size()
Display_Shared_Key()
root.mainloop()

