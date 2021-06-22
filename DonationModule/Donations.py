""" This module allows you to enter donations manually, or read them from a csv file
The donor table is a subset of all patrons who have at sometime donated.
If you want to record a donation and the name does not appear in the list
add that patron to the donor list first
"""

import tkinter as tk
from datetime import date, datetime
from tkinter import *
import tkinter.ttk
from tkinter.ttk import *
from tkinter import filedialog, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile

from DataDisplay.Checkbox import Checkbox
from DataDisplay.Choicebuttons import ChoiceButton
from DataDisplay.Dbuttons import DButton
from Database.DBUtils import Database, Intcol, Table, Charcol, PrimaryCol, Query
from PeopleEditor.People import CsvExport

# Mediates between various widgets
class TMediator():
    def __init__(self, db):
        self.db = db
        self.adding = False  #not adding in new donors from file

    def setEntry(self, srchEntry):
        self.srchEntry = srchEntry

    def setInkind(self, ink):
        self.inkind = ink  # from CheckBox

   # def setPatList(self, plist):
   #     self.patlist = plist
    def getFullQUery(self):
        qry = """select donorkey, frname, lname from patrons, donors
                      where patrons.personkey=donors.personkey
                          order by  lname"""
        return qry

    # searches for the partial name string and displays only those donors
    def keyClick(self, evt):
        s = self.srchEntry
        text = s.get()
        print("Text=" + text)
        if len(text) > 0:
            qry = """select donorkey, frname, lname from patrons, donors 
                  where patrons.personkey=donors.personkey                          
            and lname like """ + "\'" + text + "%\'" + " order by lname"""
            print(qry)
        else:
            qry = """select donorkey, frname, lname from patrons, donors
              where patrons.personkey=donors.personkey
                  order by  lname"""
            print(qry)
        #query = Query(self.db.cursor, qry)
       # results = query.execute()
       # rows = results.getRows()
        self.fillList(qry)

    def setChoiceArg(self, gv):
        self.groupv = gv

    def setNamelist(self, bbox):
        self.nameList = bbox

    def setTop(self, top):
        self.top = top  # top level of Board window

    def getDb(self):
        return self.db

    def setColumnheads(self, heads):
        self.heads = heads
    def getColumnheads(self):
        return self.heads

# adds a donation manually from date and amount fields using key from donors column
    def addDonation(self):
        index = self.nameList.curselection()
        try:
            i = int(index[0])

            patkey = self.keys[i]
            print(patkey)

            don = self.donation.get()   #from entry field
            dt = self.date.get()
            ink = self.inkind.getVar()
            qry = "Insert into donations (donorkey, amount, date, inkind) " \
                  "values("+str(patkey)+", "+ "\'"+don+ "\'," + "\'"+dt+"\'," +"\'"+str(ink)+"\')"
            query = Query(self.db.cursor, qry)
            query.execute()
            self.db.commit()
        except Exception as error:
            messagebox.showerror("No donor selected", error)
       # self.srchEntry.delete(0,END)
        # names= str(rows[0])
        # names += str(officekey)
        # self.boardBox.insert(END,names )
        self.fillList(self.getFullQUery())

    def fillList(self, qry):
        self.nameList.delete(0, END)
        ##where patrons.personkey=donors.personkey
       #order by  lname"""
        query = Query(self.db.cursor, qry)
        results = query.execute()
        rows = results.getRows()
        self.keys = []
        for r in rows:
            name = r[1] + " " + r[2]
            self.keys.append(r[0])
            self.nameList.insert(END, name)

    # name list clicked
    # display donations if not in add mode
    def nameClick(self, evt):
        if not self.adding:
            index = self.nameList.curselection()
            i = int(index[0])
            key = self.keys[i]
            qry="""select amount, date from donations, 
                donors where donors.donorkey=donations.donorkey 
                and donors.donorkey="""+str(key) +" order by date desc"
            query=Query(self.db.cursor, qry)
            results = query.execute()
            rows = results.rows
            self.donorlist.delete(0, END)
            for r in rows:
                don = str(r[0])+ " " +str(r[1])
                self.donorlist.insert(END, don)


    def setDonation(self, don):
        self.donation = don
    def getAdding(self):
        return self.adding
    def setDate(self, dt):
        self.date=dt
    def setDonorlist(self, dlist):
        self.donorlist = dlist
    def fillDonors(self, donors):
        self.donors = donors
        self.adding = True
        for d in self.donors:
            self.donorlist.insert(END, d.getName()+" "+d.getDonation())

    # donor clicked in list from csv file-
    # fill date and amount and put name in search box
    def donClick(self, evt):
        index = self.donorlist.curselection()
        i = int(index[0])
        donor = self.donors[i]
        self.srchEntry.delete(0,END)
        self.srchEntry.insert(0,donor.getLname())
        self.date.delete(0, END)
        self.date.insert(0, donor.getDate())
        self.donation.delete(0,END)
        self.donation.insert(0, donor.nickname)

    def deleteDonor(self):
        if self.adding:
            index = self.donorlist.curselection()
            i = int(index[0])
            self.donorlist.delete(i)

    def tableDisplay(self):
        tb = TableDisplay(self)


# exports current table
class ExportButton(DButton):
    def __init__(self, master, med, results, **kwargs):
        self.med = med
        self.results = results
        super().__init__(master, text="Export", **kwargs)

    def comd(self):
        # export csv file of this query
        CsvExport.export(self.results, "Donations.csv")

# records donation in in database
class AddDonationButton(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="Add donation", **kwargs)

    def comd(self):
        self.med.addNickname()


# read in csv file of donors
class ReadButton(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="Read CSV", **kwargs)
    def comd(self):
        rd = ReadDonors()
        donors = rd.read()
        self.med.fillDonors(donors)  #fills the list box


# Display complete donor table
class TableButton(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="Show table", **kwargs)

    def comd(self):
        self.med.tableDisplay()

# displays the board members in a Treeview
class TableDisplay():
    def __init__(self, med):
        self.med = med
        self.results=None
        self.frame = Toplevel(master=None)
#        self.med.setTreetop(self.frame)
        self.frame.geometry("900x400")
        self.frame.title("Donations")
        self.mainTree = Treeview(self.frame)
        self.mainTree = Treeview(self.frame, height=14)
        # self.mainTree.grid(row=0, column=0)

        self.mainTree["columns"] = (
         "frname", "lname", "donation", "date", "address", "town", "state", "zip", "email", "phone", "phone2", "nickname")
        self.med.setColumnheads(self.mainTree['columns'])

        self.mainTree.column("#0", width=20, minwidth=20, stretch=NO)  # first name
        self.mainTree.column("frname", width=80, stretch=NO)
        self.mainTree.column("lname", width=80, stretch=NO)
        self.mainTree.column("donation", width=60, stretch=NO)
        self.mainTree.column("date", width=80, stretch=NO)

        self.mainTree.column("address", width=100, stretch=NO)

        self.mainTree.column("town", width=100, stretch=NO)
        self.mainTree.column("state", width=30, stretch=NO)
        self.mainTree.column("zip", width=40, stretch=NO)
        self.mainTree.column("email", width=100, stretch=NO)
        self.mainTree.column("phone", width=100, stretch=NO)
        self.mainTree.column("phone2", width=100, stretch=NO)
        self.mainTree.column("nickname", width=100, stretch=NO)

        self.mainTree.heading('#0', text="key")
        self.mainTree.heading("frname", text="Frname")
        self.mainTree.heading("lname", text="Lname")
        self.mainTree.heading("donation", text="Donation")
        self.mainTree.heading("date", text="Date")

        self.mainTree.heading("address", text="Address")
        self.mainTree.heading("town", text="Town")
        self.mainTree.heading("state", text="State")
        self.mainTree.heading("zip", text="Zip")
        self.mainTree.heading("email", text="Email")
        self.mainTree.heading("phone", text="Mobile")
        self.mainTree.heading("phone2", text="Home")
        self.mainTree.heading("nickname", text="Nickname")
    #    med.setTree(self.mainTree)
        self.mainTree.grid(row=0, column=0, columnspan=4)
        lb1 = Label(self.frame, text="Enter \'from\' date, yyyy-mm-dd", foreground='blue')
        lb1.grid(row=4, column=1)
        self.sumButton = Button(self.frame, text = 'Sum', command=lambda:self.sumqry(self.dateEntry.get()))
        self.sumButton.grid(row=5, column=0)
        self.dateEntry = Entry(self.frame)
        self.dateEntry.grid(row=5, column=1)
        self.fullButton =  Button(self.frame, text='Full', command=lambda: self.straitquery(self.dateEntry.get()))
        self.fullButton.grid(row=5, column=2)
        self.exportButton = Button(self.frame, text="Export",
                                   command=lambda: CsvExport.export(self.results, "Donations.csv",
                                                                    self.med.getColumnheads()))
        self.exportButton.grid(row=5, column=3)

        #exportButton = ExportButton(self.frame, self.med, results)
        #exportButton.grid(row=5, column=0)

        self.straitquery(self.dateEntry.get())

    # fills the treelist
    def fillTable(self, qry):
            tree = self.mainTree
            tree.delete(*tree.get_children())
            query = Query(self.med.db.cursor, qry)
            self.results = query.execute()
            rows = self.results.getRows()

            index = 0
            for r in rows:
                riter = iter(r)
                tree.insert("", index, text=next(riter), values=(
                    next(riter), next(riter), next(riter), next(riter), next(riter),
                    next(riter), next(riter), next(riter), next(riter), next(riter), next(riter)))
                index = index + 1

    #computes sum of each donors donations
    def sumqry(self, pdate):
        if len(pdate)<=0:
            var0="select patrons.personkey, frname, lname, sum(Amount), (donations.Date), address, town,"
            var =  " state, zipcode, email, phone, phone2, nickname  from patrons, donations,"
            var1= "donors where donors.personkey=patrons.personkey and donors.donorkey=donations.Donorkey "
            var2= "group by patrons.personkey order by sum(donations.Amount) desc"
            qry = var0+var+var1+var2
        else:
            # var = " state, zipcode, email, phone, phone2  from patrons, donations,"
            # var1 = "donors where donors.personkey=patrons.personkey and donors.donorkey=donations.Donorkey "
            # var2 = "group by patrons.personkey  and donations.Date > \'"+pdate+"\' order by sum(donations.Amount) desc"
            #qry = var0 + var + var1 + var2
            qry="""select patrons.personkey, frname, lname, sum(Amount), donations.Date, 
            address, town, state, zipcode, email, phone, phone2, nickname  from patrons, 
            donations,donors where donors.personkey=patrons.personkey 
            and donors.donorkey=donations.Donorkey group by patrons.personkey,donations.date,donations.amount  
            and donations.Date > \'""" +pdate +"\' order by sum(donations.Amount) desc"""
        self.fillTable(qry)

    #displays all the conors in date order
    def straitquery(self, pdate):
        if len(pdate)<=0:
            fullqry = """select patrons.personkey, frname, lname, amount, donations.Date, address, town, 
                state, zipcode, email, phone, phone2, nickname from patrons, 
                donations, donors where donors.personkey=patrons.personkey 
                and donors.donorkey=donations.Donorkey order by donations.Date desc"""
        else:
            fullqry = """select patrons.personkey, frname, lname, amount, donations.Date, address, town, 
                            state, zipcode, email, phone, phone2,nickname from patrons, 
                            donations, donors where donors.personkey=patrons.personkey 
                            and donors.donorkey=donations.Donorkey and donations.Date > \'"""+pdate+"\' order by donations.Date desc"""
        self.fillTable(fullqry)

# Donor class holds one imported donor
# and formats the date for MySQL
class Donor():
    def __init__(self, line):
        tokens = line.split(",")
        self.frname = tokens[0]
        self.lname = tokens[1]
        self.donation = tokens[2]
        dstring = tokens[3].strip()
        print (dstring)
        self.date = datetime.strptime(dstring, "%m/%d/%Y")

    def getName(self):
        return self.frname+" "+self.lname
    def getLname(self):
        return self.lname

    def getDonation(self):
        return self.donation

    def getDate(self):
        return f'{self.date:%Y-%m-%d}'

# Read donors from csv file
class ReadDonors():
    def read(self):

        filename = filedialog.askopenfilename(
            initialdir="/", title="Select file",
            filetypes = (("Comm sep", "*.csv"), ("All Files", "*.*")))
        # create array of donors
        self.donors=[]
        with open(filename,"r") as f:
            for don in f:
                self.donors.append(Donor(don))
        return self.donors


# Displays and edits donoration and date
class DonationEditor():
    def __init__(self, db):
        self.db = db
        self.med = TMediator(db)
       # qry = "use trouperspatrons"
        #query = Query(self.db.cursor, qry)
        #results = query.execute()

    def showDonors(self):
        self.frame = Toplevel(master=None)
        self.med.setTop(self.frame)
        self.frame.geometry("600x400")
        self.frame.title("Donations")

        box1=LabelFrame(self.frame, text="Donation")
        box1.grid(row=0, column=1, rowspan=2)
        lb1=Label(box1,text="Donation amount", foreground='blue')
        lb1.grid(row=0, column=1, sticky=N)
        self.donation = Entry(box1, width=20)
        self.donation.grid(row=1, column=1, sticky=N)
        self.inkindvar = IntVar()
        self.inkindvar.set(0)

        self.inKind = Checkbox(box1, "In kind", self.inkindvar)
        self.inKind.grid(row=2, column=1, sticky=N)
        self.med.setInkind(self.inKind)
        box2= LabelFrame(self.frame, text="Donation date" )
        lb2 = Label(box2, text=" yyyy-mm-dd", foreground='blue')
        lb2.grid(row=0,column=1,sticky=N)
        self.date = Entry(box2)
        today = date.today()
        stoday = f'{today:%Y-%m-%d}'
        self.date.insert(0, stoday)
        self.date.grid(row=1, column=1, sticky=N)
        box2.grid(row=2, column=1, sticky=N)

        self.med.setDonation(self.donation)
        self.med.setDate(self.date)

        mlb = AddDonationButton(self.frame, self.med)
        mlb.grid(row=5, column=1, padx=5, pady=10)

        nameEntry = Entry(self.frame)
        self.med.setEntry(nameEntry)
        nameEntry.grid(row=0, column=0, sticky=N)
        nameEntry.bind("<KeyRelease>", self.med.keyClick)

        self.nameList = Listbox(self.frame, height=15, exportselection=False)
        self.nameList.grid(row=1, column=0, rowspan=3, sticky=N)
        self.med.setNamelist(self.nameList)
        self.nameList.bind('<<ListboxSelect>>', self.med.nameClick)
        self.med.fillList(self.med.getFullQUery())

        # create right list box and read button
        self.donList = Listbox(self.frame, height=15, width=25, exportselection=False)
        self.donList.grid(column=2, row=0, pady=10, rowspan=3)
        self.donList.bind('<<ListboxSelect>>', self.med.donClick)
        self.med.setDonorlist(self.donList)
        self.readButton = ReadButton(self. frame,self.med)
        self.readButton.grid(row=3, column=2)

        self.tbutton = TableButton(self.frame, self.med)
        self.tbutton.grid(row=4, column=0)



