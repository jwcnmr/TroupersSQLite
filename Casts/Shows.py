import tkinter as tk
from tkinter import *
import tkinter.ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, asksaveasfile

from DataDisplay.Choicebuttons import ChoiceButton
from DataDisplay.Dbuttons import DButton
from Database.DBUtils import Database, Intcol, Table, Charcol, PrimaryCol, Query

class SMediator():
    def __init__(self, db):
        self.db = db
    def setList(self, slist):
        self.sList = slist
    def setFields(self, sname, sdate):
        self.sname = sname
        self.sdate=sdate
    def clearFields(self):
        self.sname.delete(0, END)
        self.sdate.delete(0, END)
    def getShowname(self):
        return self.sname.get()
    def getDate(self):
        return self.sdate.get()
    def fillList(self):
        self.sList.delete(0,END)
        qry = "select showkey, showname, showdate from shows order by showdate desc"
        query = Query(self.db.cursor, qry)
        results = query.execute()
        rows = results.rows
        self.showkeys=[]
        for r in rows:
            self.showkeys.append(r[0])
            self.sList.insert(END, r[1]+" "+str(r[2]))
        self.clearFields()


class AddButton(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="Add show", **kwargs)

    def comd(self):
        sname = self.med.getShowname()
        sdate = self.med.getDate()
        qry = "insert into shows (showname, showdate) values(%s,%s)"
        #print(qry, sname, sdate)
        val = (sname,sdate)
        self.med.db.cursor.execute(qry, val)
        self.med.db.commit()

        self.med.fillList()



class ShowWindow():
    def __init__(self, db):
        self.db = db
        self.med=SMediator(db)
        #qry = "use trouperspatrons"
        #query = Query(self.db.cursor, qry)
        #query.execute()
    def showShows(self):
        self.frame = Toplevel(master=None)
        self.frame.geometry("350x300")
        self.showList = Listbox(self.frame, width=30)
        self.showList.grid(row=0, column =0, rowspan=4)
        self.med.setList(self.showList)
        lb1 = Label(self.frame, text="Show name", foreground='blue')
        lb1.grid(row=5, column =1)
        self.showName = Entry(self.frame, width=20)
        self.showName.grid(row = 6, column=1)

        lb1 = Label(self.frame, text="Date (yyyy-mm-dd)", foreground='blue')
        lb1.grid(row=7, column=1)
        self.showDate = Entry(self.frame,width = 20 )
        self.showDate.grid(row=8, column=1)
        self.med.setFields(self.showName, self.showDate)
        addb = AddButton(self.frame, self.med)
        addb.grid(row=9, column=1)
        self.med.fillList()


