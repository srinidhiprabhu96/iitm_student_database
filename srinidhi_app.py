import sys
from Tkinter import *
import Tkinter as tk
import urllib
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import os
def get_details(roll_no):
	gui = Toplevel()
	gui.geometry('850x500+400+200')
	from_file = get_from_file(roll_no)
	label = Label(gui,text = 'Details of '+roll_no,fg='black',font=('Times New Roman',20)).pack()
	url = 'u'
	if not from_file:
		try:
			url = urllib.urlopen("https://ccw.iitm.ac.in/IITMHostels/sinfo/"+roll_no)
			if not os.path.exists('photos'):
				os.makedirs('photos')
			f = open('photos/'+roll_no+'.jpg','wb')
			f.write(requests.get("http://photos.iitm.ac.in/byroll.php?roll="+roll_no).content)
			f.close()
			soup = BeautifulSoup(url,"lxml")
			table = soup.find("table")
			if table:
				list_of_rows = table.find_all('tr')
				list_of_data = {}
				list_of_data['Name'] = list_of_rows[0].find_all('td')[0].get_text()
				for i in range(1,len(list_of_rows)):
					list1 = list_of_rows[i].find_all('td')
					list_of_data[str(list1[0].get_text())] = str(list1[1].get_text())
				if list_of_data['Gender']=='M':
					list_of_data['Gender'] = 'Male'
				else:
					list_of_data['Gender'] = 'Female'
				label20 = Label(gui,text = 'Got from website',fg='black',font=('Arial',12)).place(x=200,y=450)
			else:
				label21 = Label(gui,text = 'Invalid roll number!',fg='black',font=('Times New Roman',20)).pack()
				url = ''
		except Exception as e:
			url=''
			label21 = Label(gui,text = 'Check your internet connection!',fg='black',font=('Times New Roman',20)).pack()
	else:
		list_of_data = eval(from_file)
		label20 = Label(gui,text = 'Got from local file',fg='black',font=('Arial',12)).place(x=200,y=450)
	if url:
		label1 = Label(gui,text = 'Name:',fg='black',font=('Arial',12)).place(x=50,y=100)
		label2 = Label(gui,text = list_of_data['Name'],fg='black',font=('Arial',12)).place(x=200,y=100)
		label3 = Label(gui,text = 'Gender:',fg='black',font=('Arial',12)).place(x=50,y=150)
		label4 = Label(gui,text = list_of_data['Gender'],fg='black',font=('Arial',12)).place(x=200,y=150)
		label5 = Label(gui,text = 'Program Name:',fg='black',font=('Arial',12)).place(x=50,y=200)
		label6 = Label(gui,text = list_of_data['Program Name'],fg='black',font=('Arial',12)).place(x=200,y=200)
		label7 = Label(gui,text = 'Department:',fg='black',font=('Arial',12)).place(x=50,y=250)
		label8 = Label(gui,text = list_of_data['Department'],fg='black',font=('Arial',12)).place(x=200,y=250)
		label9 = Label(gui,text = 'Date of Joining:',fg='black',font=('Arial',12)).place(x=50,y=300)
		label10 = Label(gui,text = list_of_data['Date of Joining'],fg='black',font=('Arial',12)).place(x=200,y=300)
		label11 = Label(gui,text = 'Faculty Advisor:',fg='black',font=('Arial',12)).place(x=50,y=350)
		label12 = Label(gui,text = list_of_data['Faculty Advisor'].title(),fg='black',font=('Arial',12)).place(x=200,y=350)
		label13 = Label(gui,text = 'Current Semester:',fg='black',font=('Arial',12)).place(x=50,y=400)
		label14 = Label(gui,text = list_of_data['Current semester'],fg='black',font=('Arial',12)).place(x=200,y=400)
		try:
			image = Image.open('photos/'+roll_no+'.jpg')
			photo = ImageTk.PhotoImage(image)
			label15 = Label(master=gui,image=photo) 
			label15.image = photo
			label15.place(x=500,y=100)
		except:
			label15 = Label(gui,text="Image not found",fg='black',font=('Arial',20)).place(x=500,y=100)
		save_btn = Button(gui,text = 'Save',bg='white',command = lambda:save_details(roll_no,list_of_data)).pack()
	
	
def get_from_file(roll_no):
	try:
		f = open('details.txt','r')
	except:
		return False
	lines = f.readlines()
	for i in range(0,len(lines),2):
		if roll_no in lines[i]:
			return lines[i+1]
	return False

def save_details(roll_no,list_of_data):
	try:
		if roll_no in open('details.txt').read():
			gui1 = Toplevel()
			gui1.geometry('300x50+400+200')
			label = Label(gui1,text = 'Already Saved',fg = 'black',font=('Arial',20)).pack()
		else:
			f = open('details.txt','a')
			f.write(roll_no+'\n')
			f.write(str(list_of_data)+'\n')
			f.close()
			gui1 = Toplevel()
			gui1.geometry('300x50+400+200')
			label = Label(gui1,text = 'Saved successfully!',fg = 'black',font=('Arial',20)).pack()
	except:
		f = open('details.txt','w')
		f.write(roll_no+'\n')
		f.write(str(list_of_data)+'\n')
		f.close()
		gui1 = Toplevel()
		gui1.geometry('300x50+400+200')
		label = Label(gui1,text = 'Saved successfully!',fg = 'black',font=('Arial',20)).pack()
	
gui = Tk()
roll_no = StringVar()
gui.geometry('400x150+400+200')
gui.title('Student Details')
label = Label(gui,text = 'Student details',fg='black',font=('Times New Roman',20)).pack()
label2 = Label(gui,text = 'Enter roll number in the text box and submit',fg='black',font=('Times New Roman',12)).pack()
entry_box = Entry(gui,textvariable = roll_no).place(x=50,y=70)
submit_roll_no = Button(gui,text = 'Submit',bg='white',command = lambda:get_details(roll_no.get().upper())).place(x=250,y=70)
gui.mainloop()
