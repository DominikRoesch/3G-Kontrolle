#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program can be used to check 3G-status and presence.
For further details, see the readme on Github.

@author: Dominik

Coded on a Raspberry Pi 4 with Spyder

"""

import csv
import tkinter as tk
import os
from tkinter import ttk
from ttkwidgets.autocomplete import AutocompleteCombobox
import shutil
from datetime import date


########################## FUNCTIONS #########################################

def append_data(file_path, Nachname, Vorname, ueber18, dreiG_vorhanden):
    # fill data into the Teilnehmerliste
    fieldnames = ['Nachname','Vorname','ueber18', '3G_vorhanden']
    with open(file_path, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        writer.writerow({
            'Nachname': Nachname,
            'Vorname': Vorname,
            'ueber18': ueber18,
            '3G_vorhanden': dreiG_vorhanden
            })
        
        
def provide_familynames(file_path):     # look for the different family_id's
    familynames = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for line in csv_reader:
            familynames.append(line['family_id'])
    familynames = list(set(familynames))
    return familynames

def provide_firstnames(file_path,familyID):     # look for the different FirstNames in familyID
    firstnames = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for line in csv_reader:
            if line['family_id'] == familyID:
                firstnames.append(line['vorname'])
    firstnames = list(set(firstnames))      # variable will be saved globally
    return firstnames

def writein_firstnames():
    firstnames = provide_firstnames(file_path,combovalue2G.get())
    #combo2G_vorname = AutocompleteCombobox(righttopframe, textvariable=combovalue2G_vorname,completevalues = firstnames)
    #combo2G_vorname.grid(row=1, column=3, padx=5, pady=20)
    combo2G_vorname['completevalues'] = firstnames


def teilnehmerliste_initialize():   # create the Teilnehmerliste
    fieldnames = ['Nachname','Vorname','ueber18', '3G_vorhanden']
    filename = '%s-Teilnehmerliste.csv' % today     # save in a file named with todays date
    with open(filename, 'w') as new_file:
        writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        writer.writeheader()
        
        
def fetch_data():           # get the single names of family members
    reference = combovalue.get()
    clear_data()
    k = 0       # initialize row counter
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for line in csv_reader:
            if line['family_id'] == reference:  # look for the correct family ID
                nn[k].set(line['nachname'])
                vn[k].set(line['vorname'])
                aw_check[k].set(1)              # family member is present by default
                
                if line['nachweis_bis_jahr'] != '':
                    checkdate = date(int(line['nachweis_bis_jahr']),int(line['nachweis_bis_monat']),int(line['nachweis_bis_tag']))
                    if today <= checkdate:
                        dreiG[k].configure(state='disabled')    # no need to check 3G if 2G is already fulfilled
                
                if line['ueber18'] == 'nein':
                    dreiG[k].configure(state='disabled')    # no need to check 3G if person is below 18 years old
                    ueber18_merker[k] = 'nein'
                else:
                    ueber18_merker[k] = 'ja'    
                
                # print(dreiG[k].cget('state')=='disabled')    
                k += 1
                
                
def clear_data():           # clear the displayed names/ticks/temporary storage
    for i in range(lines):
        nn[i].set('')
        vn[i].set('')
        aw_check[i].set(0)
        dreiG_check[i].set(0)
        dreiG[i].configure(state='normal')
        ueber18_merker[i] = ''
    
    
def document_presence():    # decide which entries to write into the Teilnehmerliste
    for i in range(lines):
        if nn[i].get() == '':
            break           # skip if there is nothing written in the row
        else:
            ueber18 = ''                # initialize variable
            dreiG_vorhanden = 'nein'    # initialize variable
            if aw_check[i].get() == 1:
                if ueber18_merker[i] == 'nein':
                    ueber18 = 'nein'
                    dreiG_vorhanden = '-'
                elif dreiG[i].cget('state') == 'disabled':
                    ueber18 = 'ja'
                    dreiG_vorhanden = 'ja'
                elif dreiG_check[i].get() == 1:
                    ueber18 = 'ja'
                    dreiG_vorhanden = 'ja'
                
                filename = '%s-Teilnehmerliste.csv' % today
                append_data(filename, nn[i].get(), vn[i].get(), ueber18, dreiG_vorhanden)
    clear_data()    # delete data after for loop
                

def set_2G():
    temp_file = 'new_database.csv'   # create temporary file that is copied to original one later on  

    with open(file_path,'r',encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = ['id','family_id','nachname','vorname','ueber18','nachweis_bis_jahr','nachweis_bis_monat','nachweis_bis_tag','3G_vorhanden']
        
        with open(temp_file, 'w') as new_file:
            
            writer = csv.DictWriter(new_file, fieldnames=fieldnames)
            writer.writeheader()
            
            for line in reader:
                if line['family_id'] == combovalue2G.get() and line['vorname'] == combovalue2G_vorname.get():
                    line['nachweis_bis_tag'] = cb_day.get()
                    line['nachweis_bis_monat'] = cb_month.get()
                    line['nachweis_bis_jahr'] = cb_year.get()
                writer.writerow(line)

            new_file.close()
    shutil.move(temp_file, file_path) # copy the new data into the database
    # set empty values "Reset"
    combovalue2G.set('')
    combovalue2G_vorname.set('')

def disableGuest3G():
    if guestu18_int.get() == 1:
        Guest3G_cb.configure(state='disabled')
    else:
        Guest3G_cb.configure(state='active')

def save_Guestentry():
    # first check if data was inserted properly
    if guestnn_string.get() != '' and guestvn_string.get() != '':
        if guestu18_int.get() == 1:
            ueber18 = 'nein'
            dreiG_vorhanden = '-'
        elif guest3G_int.get() == 1:
            ueber18 = 'ja'
            dreiG_vorhanden = 'ja'
        else:
            return
        filename = '%s-Teilnehmerliste.csv' % today
        append_data(filename, guestnn_string.get(), guestvn_string.get(), ueber18, dreiG_vorhanden)
        guestnn_string.set('')
        guestvn_string.set('')
        guestu18_int.set(0)
        guest3G_int.set(0)
        Guest3G_cb.configure(state='active')
        
    
    
########## Pre-Settings -- Load information and provide necessary data #######

today = date.today()
file_path = 'teilnehmerliste_demo.csv'

familynames = provide_familynames(file_path)
lines = 7   # specify how many maximum persons to fill in at ones
days = list(range(1,32))
months = list(range(1,13))
years = list(range(today.year,today.year+2))

#### check, whether todays Teilnehmerliste exists, if not -- create ##########
if not os.path.isfile('%s-Teilnehmerliste.csv' % today):
    teilnehmerliste_initialize()

########## General GUI layout ################################################

root = tk.Tk()

photo_image = tk.PhotoImage(master = root, file='./images/background_pic.png')

root.geometry('1280x720')
#root.wm_attributes('-transparentcolor', 'white') # seems to only work with windows

background_label = ttk.Label(root, image = photo_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

leftframe = tk.Frame(root)
leftframe.pack(side='left')

rightframe = tk.Frame(root)
rightframe.pack(side='right')

lefttopframe = tk.Frame(leftframe)
lefttopframe.pack(side='top')

leftbottomframe = tk.Frame(leftframe)
leftbottomframe.pack(side='bottom')

righttopframe = tk.Frame(rightframe)
righttopframe.pack(side='top')

rightbottomframe = tk.Frame(rightframe)
rightbottomframe.pack(side='bottom')

########## Left side of the GUI #############################################


label2 = tk.Label(lefttopframe, text='Eingabe der Anwesenheit und 3G-Kontrolle', font=('Arial',16))
label2.grid(row=0, columnspan = 4, padx=5, pady=5)

label1 = tk.Label(lefttopframe, text='Eingabe Namen:')
label1.grid(row=1, column=0, padx=5, pady=20)

combovalue = tk.StringVar()
combo = AutocompleteCombobox(lefttopframe, textvariable=combovalue, completevalues=familynames)
combo.grid(row=1, column=1, padx=5, pady=20)

button_fetch = tk.Button(lefttopframe, text='Daten anzeigen', command=fetch_data)
button_fetch.grid(row=1, column=2, padx=5, pady=20)

button_saveentry = tk.Button(lefttopframe, text='Eingabe speichern', command=document_presence)
button_saveentry.grid(row=1, column=3, padx=20, pady=20)

########## names field with checkbuttons ####################################


nachnamenentry = []
vornamenentry = []
anwesenheit = []
dreiG = []

nn = []
vn = []
aw_check = []
dreiG_check = []
ueber18_merker = []
for i in range(lines):
    nn.append(tk.StringVar())
    vn.append(tk.StringVar())
    aw_check.append(tk.IntVar())
    dreiG_check.append(tk.IntVar())
    ueber18_merker.append('')


for i in range(4):
    for j in range(lines):
        nameframe = tk.Frame(master=leftbottomframe, relief=tk.RAISED, borderwidth=1)
        nameframe.grid(row=j, column=i, padx=5, pady=5)
        
        if i == 0:
            nachnamenentry.append(tk.Entry(nameframe, width=20, textvariable=nn[j]))
            nachnamenentry[j].pack(padx=5, pady=5)
            
        if i == 1:
            vornamenentry.append(tk.Entry(nameframe, width=20, textvariable=vn[j]))
            vornamenentry[j].pack(padx=5, pady=5)
        
        if i == 2:
            anwesenheit.append(tk.Checkbutton(nameframe, text = 'anwesend', variable = aw_check[j]))
            anwesenheit[j].pack(padx=5, pady=5)
            
        if i == 3:
            dreiG.append(tk.Checkbutton(nameframe, text = '3G kontrolliert', variable = dreiG_check[j]))
            dreiG[j].pack(padx=5, pady=5)

########## Right Top side of the GUI ##########################################
label_2GHead= tk.Label(righttopframe, text='2G-Status in Datenbank einpflegen', font=('Arial',16))
label_2GHead.grid(row=0, columnspan = 4, padx=5, pady=5)

label_IDFam = tk.Label(righttopframe, text='ID Familie:')
label_IDFam.grid(row=1, column=0, padx=5, pady=20)

combovalue2G = tk.StringVar()

combo2G = AutocompleteCombobox(righttopframe, textvariable=combovalue2G, completevalues=familynames)
combo2G.grid(row=1, column=1, padx=5, pady=20)

label_Firstname = tk.Label(righttopframe, text='Vorname:')
label_Firstname.grid(row=1, column=2, padx=5, pady=20)

combovalue2G_vorname = tk.StringVar()
combo2G_vorname = AutocompleteCombobox(righttopframe, textvariable=combovalue2G_vorname,postcommand = writein_firstnames,completevalues = [])
combo2G_vorname.grid(row=1, column=3, padx=5, pady=20)

label_New2G = tk.Label(righttopframe, text='Neuer 2G-Nachweis bis:')
label_New2G.grid(row=2, column=0, padx=5, pady=20)

cb_day = tk.IntVar(value=today.day)
cb_month = tk.IntVar(value=today.month)
cb_year = tk.IntVar(value=today.year) 

combo_day = ttk.Combobox(righttopframe, width = 5, textvariable=cb_day, values = days)
combo_day.grid(row=2, column=1, padx=5, pady=20)

combo_month = ttk.Combobox(righttopframe, width = 5, textvariable=cb_month, values = months)
combo_month.grid(row=2, column=2, padx=5, pady=20)

combo_year = ttk.Combobox(righttopframe, width = 5, textvariable=cb_year, values = years)
combo_year.grid(row=2, column=3, padx=5, pady=20)

buttonSave2G = tk.Button(righttopframe, text='2G-Status speichern',command=set_2G)
buttonSave2G.grid(row=3, columnspan = 4, padx=5, pady=5)

fillspace = tk.Label(righttopframe)
fillspace.grid(row=4, columnspan = 4, padx=5, pady=13)

########## Right Bottom side of the GUI #######################################
label_guest= tk.Label(rightbottomframe, text='Anwesenheit Gast dokumentieren', font=('Arial',16))
label_guest.grid(row=0, columnspan = 4, padx=5, pady=20)

labelGuestVN = tk.Label(rightbottomframe, text='Vorname')
labelGuestVN.grid(row=1, column=0, padx=5, pady=0)

labelGuestNN = tk.Label(rightbottomframe, text='Nachname')
labelGuestNN.grid(row=1, column=1, padx=5, pady=0)

guestvn_string = tk.StringVar()
guestnn_string = tk.StringVar()
guestu18_int = tk.IntVar()
guest3G_int = tk.IntVar()
guestu18_int.set(0)
guest3G_int.set(0)

GuestVN = tk.Frame(master=rightbottomframe, relief=tk.RAISED, borderwidth=1)
GuestVN.grid(row=2, column=0, padx=5, pady=5)
GuestVN_E = tk.Entry(GuestVN, width=20, textvariable=guestvn_string)
GuestVN_E.pack(padx=5, pady=5)

GuestNN = tk.Frame(master=rightbottomframe, relief=tk.RAISED, borderwidth=1)
GuestNN.grid(row=2, column=1, padx=5, pady=5)
GuestNN_E = tk.Entry(GuestNN, width=20, textvariable=guestnn_string)
GuestNN_E.pack(padx=5, pady=5)

Guestu18 = tk.Frame(master=rightbottomframe, relief=tk.RAISED, borderwidth=1)
Guestu18.grid(row=2, column=2, padx=5, pady=5)
Guestu18_cb = tk.Checkbutton(Guestu18, text = 'unter 18', variable = guestu18_int, command=disableGuest3G)
Guestu18_cb.pack(padx=5, pady=5)

Guest3G = tk.Frame(master=rightbottomframe, relief=tk.RAISED, borderwidth=1)
Guest3G.grid(row=2, column=3, padx=5, pady=5)
Guest3G_cb = tk.Checkbutton(Guest3G, text = '3G kontrolliert', variable = guest3G_int)
Guest3G_cb.pack(padx=5, pady=5)

buttonSaveGuest = tk.Button(rightbottomframe, text='Eingabe Gast speichern',command=save_Guestentry)
buttonSaveGuest.grid(row=3, columnspan = 4, padx=5, pady=5)


root.title('Anwesenheitsdokumentation')
root.mainloop()