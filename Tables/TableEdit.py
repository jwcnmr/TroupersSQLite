import tkinter as tk
from tkinter import *
import tkinter.ttk
from tkinter.ttk import *
from tkinter import filedialog

from DataDisplay.Choicebuttons import ChoiceButton
from DataDisplay.Dbuttons import DButton
from Database.DBUtils import Database, Intcol, Table, Charcol, PrimaryCol, Query

class AddButton(DButton):
    def __init__(self,master, pe,  **kwargs):
        super().__init__(master, text="Add", **kwargs)
        self.pedit = pe
    def comd(self):
        self.pedit.addData()
        self.pedit.getFrame().destroy()


class SaveButton(DButton):
    def __init__(self,master, pe,  **kwargs):
        super().__init__(master, text="Save", **kwargs)
        self.pedit = pe
    def comd(self):
        self.pedit.saveData()
        self.pedit.getFrame().destroy()



class ExitButton(DButton):
    def __init__(self,  top,  **kwargs):
        super().__init__(top, text="Cancel", **kwargs)
        self.top = top
    def comd(self):
        self.top.destroy()



class PatronEdit():
    def __init__(self,  db):
        self.db = db

    def editPerson(self, lineId):
        idict = lineId
        self.patkey = int(idict.get('text'))

        self.cursor = self.db.cursor

        query="""SELECT frname, lname, address, town, state, zipcode,  email, phone, phone2, sex, nickname FROM patrons where personkey="""+str(self.patkey)
        qry = Query(self.cursor, query)
        results = qry.execute()
        trow = results.getRows()  #tuple
        row=trow[0] #first is list
        #print (row)
        self.buildTable()
        self.frname.insert(0, row[0])
        self.lname.insert(0, row[1])
        self.address.insert(0, row[2])
        self.town.insert(0, row[3])
        self.state.insert(0, row[4])
        self.zip.insert(0, row[5])
        self.email.insert(0, row[6])
        self.phone.insert(0, row[7])
        ph = row[8]
        if ph == None:
            ph = ""
        self.phone2.insert(0, ph)
        self.groupSex.set(row[9])
        self.nickname.delete(0, END)
        self.nickname.insert(0, row[10])

        savebutton = SaveButton(self.frame, self)
        savebutton.grid(row=9, column=0, padx=5,pady=5)

        exitbutton = ExitButton(self.frame )
        exitbutton.grid(row=9, column=1, padx=5, pady=5)

    def addPerson(self):
        self.buildTable()
        addbutton = AddButton(self.frame, self)
        addbutton.grid(row=9, column=0, padx=5, pady=5)

        exitbutton = ExitButton(self.frame)
        exitbutton.grid(row=9, column=1, padx=5, pady=5)

    def buildTable(self):
        self.frame = Toplevel(master=None)
        lb1 = Label(self.frame, text="Frname", foreground='blue')
        lb1.grid(row=0,column=0,sticky=S)
        lb2 = Label(self.frame, text="Lname", foreground='blue')
        lb2.grid(row=0, column=1, sticky=S)
        lb3=Label(self.frame, text="Sex", foreground='blue')
        lb3.grid(row=0, column=2, sticky=S)

        self.frname = Entry(self.frame)
        self.lname = Entry(self.frame)
        self.frname.grid(row=1, column=0, padx=5, pady=5)
        self.lname.grid(row=1, column=1, padx=5, pady=5)
        self.groupSex = tk.IntVar()
        self.groupSex.set(1)  # default to Female sex
        ck1=ChoiceButton(self.frame, 'F', 1, self.groupSex)
        ck2=ChoiceButton(self.frame, 'M', 2, self.groupSex)
        ck1.grid(row=1, column=2)
        ck2.grid(row=1, column=3,sticky=W)

        lb3 = Label(self.frame, text="Address", foreground='blue')
        lb3.grid(row=2, column=0)
        lb4 = Label(self.frame, text="Town", foreground='blue')
        lb4.grid(row=2, column=1)
        lb5 = Label(self.frame, text="State", foreground='blue')
        lb5.grid(row=2, column=2)

        self.address = Entry(self.frame)
        self.address.grid(row=3, column=0, padx=5, pady=5)
        self.town = Entry(self.frame)
        self.town.grid(row=3, column=1, padx=5, pady=5)
        self.state = Entry(self.frame, width=5)
        self.state.grid(row=3, column=2, padx=5, pady=5)

        lb6 = Label(self.frame, text="Zip", foreground='blue')
        lb6.grid(row=4, column=0)
        lb7 = Label(self.frame, text="Email", foreground='blue')
        lb7.grid(row=4, column=1)

        self.zip = Entry(self.frame)
        self.zip.grid(row=5, column=0, padx=5, pady=5)
        self.email = Entry(self.frame, width=30)
        self.email.grid(row=5, column=1, columnspan=2)

        lb8 = Label(self.frame, text="Mobile Phone", foreground='blue')
        lb8.grid(row=6, column=0)
        lb9 = Label(self.frame, text="Home phone", foreground='blue')
        lb9.grid(row=6, column=1)

        self.phone = Entry(self.frame)
        self.phone.grid(row=7, column=0, padx=5, pady=5)
        self.phone2 = Entry(self.frame)
        self.phone2.grid(row=7, column=1, padx=5, pady=5)
        lb9= Label(self.frame, text="Salutation", foreground='blue')
        lb9.grid(row=8, column=0)
        self.nickname = Entry(self.frame)
        self.nickname.grid(row=8, column=1)

    def getDb(self):
        return self.db
    def getFrame(self):
        return self.frame

    def addData(self):
        query = "insert into patrons(frname, lname, sex, address,town, " \
                "state,zipcode, email, phone, phone2,nickname) values (\'" + self.frname.get() + "\'" + \
                ", \'" + self.lname.get() + "\'" + \
                ", \'" + str(self.groupSex.get()) + "\'" + \
                ", \'" + self.address.get() + "\'" + \
                ", \'" + self.town.get() + "\'" + \
                ", \'" + self.state.get() + "\'" + \
                ", \'" + self.zip.get() + "\'" + \
                ", \'" + self.email.get() + "\'" + \
                ", \'" + self.phone.get() + "\'" + \
                ", \'" + self.phone2.get() + "\'" +\
                ", \'" + self.nickname.get() + "\')"
        print(query)
        qry = Query(self.db.cursor, query)
        qry.execute()
        self.db.commit()
        self.frame.destroy()  # close window

    def saveData(self):
            query = "update patrons set frname=\'" + self.frname.get() + "\'"+\
                    ", lname=\'" + self.lname.get() +"\'" + \
                    ", sex= \'" + str(self.groupSex.get()) + "\'" + \
                    ", address=\'" + self.address.get() +"\'" + \
                    ", town=\'" + self.town.get() + "\'" + \
                    ", state=\'" + self.state.get() +"\'" +\
                    ", zipcode=\'" + self.zip.get() +"\'" +\
                    ", email=\'" + self.email.get() +"\'" +\
                    ", phone=\'" + self.phone.get() + "\' " \
                    ", phone2=\'" + self.phone2.get() + "\' " \
                    ", nickname=\'" + self.nickname.get() + "\' " \
                    "where personkey=" + str(self.patkey)
            print(query)
            qry = Query(self.cursor, query)
            qry.execute()
            self.db.commit()
            self.frame.destroy()  # close window

