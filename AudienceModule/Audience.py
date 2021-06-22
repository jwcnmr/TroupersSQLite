import tkinter as tk
from tkinter import *
import tkinter.ttk
from tkinter.ttk import *
from tkinter import filedialog, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile

from DataDisplay.Choicebuttons import ChoiceButton
from DataDisplay.Dbuttons import DButton
from Database.DBUtils import Database, Intcol, Table, Charcol, PrimaryCol, Query
from PeopleEditor.People import CsvExport
from AudienceModule.TableDisp import ATableDisplay


class OpenCSV(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="Open CSV", **kwargs)

    def comd(self):
        self.med.openFile()

class NextButton(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="Next", **kwargs)

    def comd(self):
        self.med.readNext()


class Assign(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="<--Assign", **kwargs)

    def comd(self):
        self.med.addAudience()

class CMediator():
    def __init__(self, db):
        self.db = db
        # use this database
        #qry = "use trouperspatrons"
        #query = Query(self.db.cursor, qry)
        #results = query.execute()
        self.voiceList = ["Soprano", "Alto", "Tenor", "Bass"]

    def openFile(self):
        fname = filedialog.askopenfilename(
        title="Select file")
        self.csvfile = open(fname, "r")
        self.cnames=[]
        self.cnames = self.csvfile.readlines()
        self.findex = 0
        self.readNext()

    def readNext(self):
        cols = self.cnames[self.findex]
        acols = cols.split(",")
        self.findex += 1
        self.srchEntry.delete(0, END)
        self.srchEntry.insert(0, acols[0])
        #order in csv must be last, first
        self.nameLabel.config(text=acols[1]+" "+acols[0])

    def setLabel(self, lbl):
        self.nameLabel = lbl

    def getDB(self):
        return self.db

    def setPatlist(self, plist):
        self.patList = plist

    def setEntry(self, srch):
        self.srchEntry = srch

    def setAudlist(self, alist):
        self.aList = alist

    def getCastlist(self):
        return self.aList

    def setRoletype(self, rtype):
        self.roleType = rtype

    def setTreetop(self, frame):
        self.treetop = frame

    def getTreetop(self):
        return self.treetop

    def showClick(self, evt):
        cindex = self.showlist.curselection()
        print(cindex[0])
        index = cindex[0]
        self.showkey = self.showkeys[index]
        self.fillAud(self.showkey)

    def getShowKey(self):
        return self.showkey

    def getTree(self):
        return self.tree

    def keyClick(self, evt):
        s = self.srchEntry
        text = s.get()
        #  print("Text=" + text)
        if len(text) > 0:
            qry = """select personkey, frname, lname, address, town, state, zipcode, 
            email, phone from patrons where lname like """ + "\'" + text + "%\'" + " order by lname"
            print(qry)
        else:
            qry = """select personkey, frname, lname, address, town, state, zipcode, 
                        email, phone from patrons order by lname"""
            print(qry)
        query = Query(self.db.cursor, qry)
        results = query.execute()
        rows = results.getRows()
        self.patList.delete(0, END)
        self.keys = []
        for r in rows:
            name = r[1] + " " + r[2]
            self.keys.append(r[0])
            self.patList.insert(END, name)

    def setShowlist(self, showlist):
        self.showlist = showlist

    def setRolename(self, rname):
        self.roleName = rname

    def getShowkey(self):
        return self.showkey

    def voiceClicked(self, index):
        self.roleName.delete(0, END)
        self.roleName.insert(0, self.voiceList[index])

    def editPerson(self, idict):
        self.patkey = int(idict.get('text'))
       # pe = PersonEdit(self.db, self, self.patkey)

    def setColnames(self, cnames):
        self.colnames = cnames
    def getColnames(self):
        return self.colnames

    def setTree(self, tree):
        self.tree = tree

    def fillList(self):
        self.showlist.delete(0, END)
        qry = "select showkey, showname, showdate from shows order by showdate desc"
        query = Query(self.db.cursor, qry)
        results = query.execute()
        rows = results.rows
        self.showkeys = []
        for r in rows:
            self.showkeys.append(r[0])
            self.showlist.insert(END, r[1] + " " + str(r[2]))

    def addAudience(self):
        #rolename = self.roleName.get()
        cindex = self.showlist.curselection()
        index = cindex[0]
        showkey = self.showkeys[index]
        cindex = self.patList.curselection()
        patkey = self.keys[cindex[0]]
        #roletype = self.roleType.get()
        qry = "Insert into audience (showkey, personkey) values(%s, %s)"
        val = (showkey, patkey)
        #print(qry)
        #print(val)
        self.db.cursor.execute(qry, val)
        self.db.commit()
        self.fillAud(showkey)
      #  self.roleName.delete(0,END)

    def fillAud(self, index):
        # qry= """select personkey, frname, lname, rolename from patrons, cast
        # where shows.personkey=patrons.personkey order by patrons.sex desc,
        # cast.roletype where shows.showkey=\'"""+str(index)+"\'"
        qry = """select audkey, frname, lname from patrons, audience 
            where audience.personkey=patrons.personkey and audience.showkey=""" + str(
            index) + " order by lname"
        print(qry)
        query = Query(self.db.cursor, qry)
        results = query.execute()
        rows = results.getRows()
        self.audKeys =[]
        self.aList.delete(0, END)
        for r in rows:
            riter = iter(r)
            key = next(riter)
            self.audKeys.append(int(key))
            self.aList.insert(END, next(riter)+" "+ next(riter))
            # next(riter), next(riter), next(riter), next(riter), next(riter)))
            index = index + 1

class TableButton(DButton):
        def __init__(self, master, med, **kwargs):
            self.med = med
            super().__init__(master, text="Show table", **kwargs)

        def comd(self):
            tbd = ATableDisplay(self.med)

class EditButton(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="Edit", **kwargs)

    def comd(self):
        tree = self.med.getCastlist()
        curitem = tree.focus()
        print("edit person")
        self.med.editPerson(tree.item(curitem))

    def deleterow(self):
        ans = messagebox.askyesno("Delete?", "Do you want to delete " + self.name)
        if ans == YES:
            qry = "delete from audience where audkey=" + str(self.audkey)
            query = Query(self.db.cursor, qry)
            query.execute()
        self.exitC()

    def exitC(self):
        self.frame.destroy()


class AudMembers():
    def __init__(self, db):
        self.db = db

    def builder(self):
        self.frame = Toplevel(master=None)
        self.frame.geometry("670x500")
        self.med = CMediator(self.db)

        self.audList = Listbox(self.frame, height=20, width=30, exportselection=False)

        self.audList.grid(row=0, column=0, rowspan=3, sticky=N)
        self.med.setAudlist(self.audList)

        rframe = Frame(self.frame)
        self.srchEntry = Entry(rframe, width=30)
        self.srchEntry.grid(row=0, column=0, sticky=N)
        self.srchEntry.bind("<KeyRelease>", self.med.keyClick)
        self.med.setEntry(self.srchEntry)
        self.nameLabel = Label(rframe, text="")
        self.patlist = Listbox(rframe, height=20, width=30, exportselection=False)
        self.patlist.grid(row=1, column=0, rowspan=4, sticky=N)
        self.med.setPatlist(self.patlist)
        rframe.grid(row=0, column=2)
        self.nameLabel.grid(row=2, column=2)
        self.med.setLabel(self.nameLabel)
        audfile = OpenCSV(rframe, self.med)
        audfile.grid(row=4, column=2)
        nxButton = NextButton(rframe,self.med)
        nxButton.grid(row = 5, column=2)

        cFrame = Frame(self.frame)
        self.showList = Listbox(cFrame, width=30, height=8, exportselection=False)
        self.showList.grid(row=0, column=0, rowspan=2, sticky=N)
        self.med.setShowlist(self.showList)
        self.showList.bind('<<ListboxSelect>>', self.med.showClick)
        cFrame.grid(row=0, column=1, sticky=N, pady=5)

       # lb1 = Label(cFrame, text="Character", foreground='blue')
       # lb1.grid(row=2, column=0, sticky=N)
       # self.roleName = Entry(cFrame, width=20)
       # self.roleName.grid(row=3, column=0, sticky=N)
       # self.med.setRolename(self.roleName)

        asButton = Assign(self.frame, self.med)
        asButton.grid(row=3, column=1)
        self.med.fillList()  # fill show list box

        tb = TableButton(self.frame, self.med)
        tb.grid(row=4, column=0)









