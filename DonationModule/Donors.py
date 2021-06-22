import tkinter as tk
from tkinter import *
import tkinter.ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename, asksaveasfile

from DataDisplay.Choicebuttons import ChoiceButton
from DataDisplay.Dbuttons import DButton
from Database.DBUtils import Database, Intcol, Table, Charcol, PrimaryCol, Query
from PeopleEditor.People import CsvExport


class TMediator():
    def __init__(self, db):
        self.db = db

    def setEntry(self, srchEntry):
        self.srchEntry = srchEntry

    def setPatList(self, plist):
        self.patlist = plist

    def keyClick(self, evt):
        s = self.srchEntry
        text = s.get()
        print("Text=" + text)
        if len(text) > 0:
            qry = """select personkey, frname, lname, address, town, state, zipcode, 
            email, phone from trouperspatrons.patrons where lname like """ + "\'" + text + "%\'" + " order by lname"
            print(qry)
        else:
            qry = """select personkey, frname, lname, address, town, state, zipcode, 
                        email, phone from trouperspatrons.patrons order by lname"""
            print(qry)
        query = Query(self.db.cursor, qry)
        results = query.execute()
        rows = results.getRows()
        self.patlist.delete(0, END)
        self.keys = []
        for r in rows:
            name = r[1] + " " + r[2]
            self.keys.append(r[0])
            self.patlist.insert(END, name)

    def setChoiceArg(self, gv):
        self.groupv = gv

    def setBoardBox(self, bbox):
        self.boardBox = bbox

    def setTop(self, top):
        self.top = top  # top level of Board window

    def getDb(self):
        return self.db

    def moveLeft(self):
        index = self.patlist.curselection()
        i = int(index[0])
        patkey = self.keys[i]
       # officekey = self.groupv.get()
        print(patkey)

        qry = "select frname, lname  from patrons where patrons.personkey=" + str(
            patkey)
        print(qry)
        query = Query(self.db.cursor, qry)
        results = query.execute()
        rows = results.getRows()
        names = ""
        for r in rows:
            names += str(r) + " "
        qry = "Insert into donors (personkey) values("+str(patkey)+")"
        query = Query(self.db.cursor, qry)
        query.execute()
        self.db.commit()
        self.srchEntry.delete(0,END)
        # names= str(rows[0])
        # names += str(officekey)
        # self.boardBox.insert(END,names )
        self.fillList()

    def fillList(self):
        self.boardBox.delete(0, END)
        qry = """select frname, lname from patrons, donors 
       where patrons.personkey=donors.personkey 
       order by  lname"""
        query = Query(self.db.cursor, qry)
        results = query.execute()
        rows = results.getRows()
        for row in rows:
            name = ""
            for r in row:
                name += str(r) + " "
            self.boardBox.insert(END, name)

    def setTree(self, tree):
        self.tree = tree

    def getTree(self):
        return self.tree

    def showTable(self):
        tb = TableDisplay(self)

    def setTreetop(self, treetop):
        self.treetop = treetop

    def setheader(self,hd):
        self.headers =hd
    def getHeader(self):
        return self.headers


# displays the board members in a Treeview
class TableDisplay():
    def __init__(self, med):
        self.med = med
        self.frame = Toplevel(master=None)
        self.med.setTreetop(self.frame)
        self.frame.geometry("825x400")
        self.frame.title("Donors")
        self.mainTree = Treeview(self.frame)
        self.mainTree = Treeview(self.frame, height=14)
        # self.mainTree.grid(row=0, column=0)

        self.mainTree["columns"] = (
        "frname", "lname", "address", "town", "state", "zip", "email", "phone", "phone2")
        med.setheader(self.mainTree["columns"])
        self.mainTree.column("#0", width=20, minwidth=20, stretch=NO)  # first name
        self.mainTree.column("frname", width=80, stretch=NO)
        self.mainTree.column("lname", width=80, stretch=NO)
        self.mainTree.column("address", width=100, stretch=NO)

        self.mainTree.column("town", width=100, stretch=NO)
        self.mainTree.column("state", width=30, stretch=NO)
        self.mainTree.column("zip", width=40, stretch=NO)
        self.mainTree.column("email", width=100, stretch=NO)
        self.mainTree.column("phone", width=100, stretch=NO)
        self.mainTree.column("phone2", width=100, stretch=NO)

        self.mainTree.heading('#0', text="key")
        self.mainTree.heading("frname", text="Frname")
        self.mainTree.heading("lname", text="Lname")

        self.mainTree.heading("address", text="Address")
        self.mainTree.heading("town", text="Town")
        self.mainTree.heading("state", text="State")
        self.mainTree.heading("zip", text="Zip")
        self.mainTree.heading("email", text="Email")
        self.mainTree.heading("phone", text="Mobile")
        self.mainTree.heading("phone2", text="Home")
        med.setTree(self.mainTree)
        self.mainTree.grid(row=0, column=0, columnspan=4)

        qry = """select patrons.personkey, frname, lname, address, town, state, zipcode, email, phone, phone2 from patrons, donors 
              where patrons.personkey=donors.personkey 
              order by lname"""

        query = Query(self.med.db.cursor, qry)
        results = query.execute()
        rows = results.getRows()
        query = Query(med.db.cursor, qry)
        results = query.execute()
        rows = results.getRows()
        tree = self.med.getTree()
        index = 0
        for r in rows:
            riter = iter(r)

            tree.insert("", index, text=next(riter), values=(
                next(riter), next(riter), next(riter), next(riter), next(riter),
                next(riter), next(riter), next(riter), next(riter)))
            index = index + 1
        exportButton = ExportButton(self.frame, self.med, results)
        exportButton.grid(row=5, column=0)


# exports curremt table
class ExportButton(DButton):
    def __init__(self, master, med, results, **kwargs):
        self.med = med
        self.results = results
        super().__init__(master, text="Export", **kwargs)

    def comd(self):
        # export csv file of this query
        CsvExport.export(self.results, med.getHeader(), "Donors.csv")


class MoveLeftButton(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="<--Add", **kwargs)

    def comd(self):
        self.med.moveLeft()

# Display complete donor table
class TableButton(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="Show table", **kwargs)

    def comd(self):
        self.med.showTable()


class ExitButton(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="Exit", **kwargs)

    def comd(self):
        self.med.top.destroy()


# Displays and edits board members
class DonorEditor():
    def __init__(self, db):
        self.db = db
        self.med = TMediator(db)
        #qry = "use trouperspatrons"
        #query = Query(self.db.cursor, qry)
        #results = query.execute()

    def showDonors(self):
        self.frame = Toplevel(master=None)
        self.med.setTop(self.frame)
        self.frame.geometry("600x400")
        self.frame.title("Donors")

        self.boardLbox = Listbox(self.frame, width=25, height=15)
        self.boardLbox.grid(row=0, column=0, rowspan=4, sticky=N)
        self.med.setBoardBox(self.boardLbox)
       # lframe = LabelFrame(self.frame, text="Life members")
       # lframe.grid(row=0, column=1, rowspan=3)

        tblButton = TableButton(self.frame, self.med)
        tblButton.grid(row=5, column=0)
        exitButton = ExitButton(self.frame, self.med)
        exitButton.grid(row=5, column=1)

        mlb = MoveLeftButton(self.frame, self.med)
        mlb.grid(row=4, column=1)

        nameEntry = Entry(self.frame)
        self.med.setEntry(nameEntry)
        nameEntry.grid(row=0, column=2, sticky=N)
        nameEntry.bind("<KeyRelease>", self.med.keyClick)

        nameList = Listbox(self.frame)
        nameList.grid(row=1, column=2, rowspan=3, sticky=N)
        self.med.setPatList(nameList)
        self.med.fillList()

