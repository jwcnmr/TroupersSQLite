import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox

from AudienceModule.Audience import AudMembers
from DataDisplay.Dbuttons import DButton
from Database.DBUtils import Table, Charcol, PrimaryCol, Query, SqltDatabase
from DonationModule.Donations import DonationEditor
from DonationModule.Donors import DonorEditor
from Lifermodule.Lifers import LiferEditor
from Menus import Menubar, TopMenu, Menucommand
from Menus.Menufiles import Quitcommand
from DonationModule.Nicknames import NicknameEditor
from PeopleEditor.People import BoardEditor
from Casts.Shows import ShowWindow
from Tables.TableEdit import PatronEdit
from Casts.Castselection import Casting
import sys
from os import path
# from PeopleEditor import BoardEditor


class Patron:
    def __init__(self, line):
        toks = line.split(",")
        it = iter(toks)
        self.oldid =  \
            next(it)
        self.frname = next(it)
        self.frname = self.frname.replace(";", ",")
        self.lname = next(it)
        self.lname = self.lname.replace(";", ",")
        self.address = next(it)
        self.address = self.address.replace(";", ",")
        self.town = next(it)
        self.state = next(it)
        self.zip = next(it)
        if len(self.zip) == 4:
            self.zip = "0"+self.zip
        self.phone = next(it)
        self.email = next(it)

    def getLoadString(self, i):
        vals = (self.frname, self.lname, self.address, self.town, self.state, self.zip, self.phone, self.email.strip())
        #print(vals)
        return vals


class Mediator:
    def __init__(self):
        self.treeflag=False
        self.datafile=""
    def getQuery(self):
        return """SELECT personkey, frname, lname, address, town, state, zipcode, 
        email, phone, phone2 FROM trouperspatrons.patrons order by lname"""
    def setPats(self, patrons):
        self.pats = patrons
    def getPats(self):
        return self.pats
    def setPrimaryString(self, prims):
        self.pstring = prims
    def getPrimaryString(self):
        return self.pstring
    def setMainTree(self, tree):
        self.mainTree = tree
        self.treeflag = True
    def getTree(self):
        return self.mainTree
    def setSearchfield(self,srch):
        self.srchEntry = srch
    #deletes entry field and clears the tree
    def clearClicked(self):
        self.srchEntry.delete(0, END)
        self.mainTree.delete(*self.mainTree.get_children())
    def setDb(self,db):
        self.db = db
    def getDB(self):
        return self.db
    def setKeys(self,keys):
        self.keys = keys
    def keyClick(self, evt):
        s=self.srchEntry
        text = s.get()
       #print("Text=" + text)
        if len(text) >0:
            qry = """select personkey, frname, lname, address, town, state, zipcode, 
            email, phone,phone2 from patrons where lname like """+ "\'" + text + "%\'" +" order by lname"
            #print(qry)
            if self.treeflag:
                tree = self.mainTree
                tree.delete(*self.mainTree.get_children())
                tl = TreeLoader(tree, self )
                tl.load(qry)

    def treeDouble(self, evt):
        selection = self.mainTree.selection()
        curitem = self.mainTree.focus()
        tbEdit = PatronEdit( self.db)
        tbEdit.editPerson(self.mainTree.item(curitem))

    def addClicked(self):
        tbEdit = PatronEdit(self.db)
        tbEdit.addPerson()

    def delClicked(self):
        curitem = self.mainTree.focus()
        id = self.mainTree.item(curitem)
        self.patkey = int(id.get('text'))
        answer=messagebox.askyesno("Delete warning","Do you really want to delete person "+str(self.patkey))
        if answer==YES:
            querytxt = "delete from patrons where personkey =" + str(self.patkey)
            #(querytxt)
            query = Query(self.db.cursor, querytxt)

            query.execute()
            self.db.commit()

    def setPatTable(self, pat):
        self.patTable = pat
    def setDelButton(self, delbutton):
        self.delButton = delbutton
    def treeClick(self,evt):
        self.delButton.enable()
    def showBoard(self):
        bded=BoardEditor(self.db)
        bded.showBoard()
    def showLifers(self):
        lifed = LiferEditor(self.db)
        lifed.showLifers()
    def showDonors(self):
        donored = DonorEditor(self.db)
        donored.showDonors()
    def showDonations(self):
        donated = DonationEditor(self.db)
        donated.showDonors()
    def editNicknames(self):
        nicked = NicknameEditor(self.db)
        nicked.showDonors()

    def showList(self):
        showed= ShowWindow(self.db)
        showed.showShows()
    def showCast(self):
        casting= Casting(self.db)
        casting.builder()

    def showAudience(self):
        audience = AudMembers(self.db)
        audience.builder()


class MakeDatabase():
    def __init__(self, med):
        self.med = med

    def create(self):
        #db = Database("localhost", "newuser", "new_user")
        db = SqltDatabase('Trouperspatrons.db')
        db.create("TroupersPatrons")
        self.patTable = Table(db, "patrons", self.med)
        self.patTable.addColumn(PrimaryCol("personkey", True, self.med))  # primary key
        self.patTable.addColumn(Charcol("frname", 45))
        self.patTable.addColumn(Charcol("lname", 45))
        self.patTable.addColumn(Charcol("address", 45))
        self.patTable.addColumn(Charcol("town", 45))
        self.patTable.addColumn(Charcol("state", 6))
        self.patTable.addColumn(Charcol("zipcode", 10))
        self.patTable.addColumn(Charcol("phone", 15))
        self.patTable.addColumn(Charcol("email", 45))
        self.patTable.create()
        self.med.setPatTable(self.patTable)

    def loadTable(self):
        pats = self.med.getPats()
        p1="["
        p1 = ""
        for i in range(1,len(pats)):
            p1 = ""
        #i=1
            p1 += str(pats[i-1].getLoadString(i))
        #    if i<10:
        #        p1+=", "
            #p1 = "[" + str(p1)
            p1=p1+","
        #remove last comma
            k=len(p1)
            p2 = p1[0:k-1]
        #p2 += "]"
            #print(p2)
            self.patTable.addRow(p2)
            self.med.setPatTable(self.patTable)

class Readcommand(Menucommand):
    def __init__(self, root, label, med):
        super().__init__(root, label)
        self.med = med

    def comd(self):
       fname= filedialog.askopenfilename( title="Select file")
       fl = open(fname, "r")
       header = fl.readline()
       self.pats = []
       for sname in fl:
            pat = Patron(sname)
            self.pats.append(pat)
       #print(len(self.pats))
       self.med.setPats( self.pats)
       mkdb = MakeDatabase(self.med)
       mkdb.create()
       mkdb.loadTable()

class TreeLoader():
    def __init__(self, tree, med):
        self.tree = tree
        self.med = med
    def load(self,querytxt):
        #print(querytxt)
        db = self.med.getDB()
        query = Query(db.cursor, querytxt)
        results = query.execute()
        rows = results.getRows()
        dictRows = results.getDictRows()
        #print (rows)

        #self.keyslist = []
        """ index = 0
        for r in rows:
            riter = iter(r)
            self.tree.insert("", index, text=next(riter), values=(next(riter),
            next(riter), next(riter), next(riter), next(riter),
            next(riter), next(riter), next(riter), next(riter)))
            index = index + 1"""

        index = 0
        for r in dictRows:
            self.tree.insert("", index,
            text= r.get('personkey'),
            values=(r.get('frname'),
                    r.get('lname'),
                    r.get('address'),
                    r.get('town'),
                    r.get('state'),
                    r.get('zipcode'),
                    r.get('phone'),
                    r.get('email')))
            index += 1


class OpenCommand(Menucommand):
    def __init__(self, root, label, med):
        super().__init__(root, label)
        self.med = med
    def comd(self):

        if not path.exists(self.med.datafile):
            self.med.datafile = filedialog.askopenfilename(defaultextension= '*.db')
        db = SqltDatabase(self.med.datafile)
        tb = db.getTables()
        #(tb)
        #db = Database("localhost", "newuser", "new_user")
        self.med.setDb(db)
        keylist = []    #list of person keys
        querytxt = "SELECT personkey, frname, lname, address, town, state, zipcode, email, phone, phone2 FROM patrons order by lname"
        query = Query(db.cursor, querytxt)
        results = query.execute()
        rows = results.getRows()
        tree= self.med.getTree()
        index = 0
        for r in rows:
            riter=iter(r)
            #keylist.append(next(riter)) #save key list
            try:
                tree.insert("", index, text=next(riter),values=(next(riter),next(riter),
                        next(riter),next(riter),next(riter),next(riter),next(riter),
                        next(riter), next(riter)))
            except:
                print('insert error', sys.exc_info()[0], index)
            index = index+1
        self.med.setKeys(keylist)

class Boardmembers(Menucommand):
    def __init__(self, root, label, med):
        super().__init__(root, label)
        self.med = med
    def comd(self):
        self.med.showBoard()

class Lifemembers(Menucommand):
    def __init__(self, root, label, med):
        super().__init__(root, label)
        self.med = med
    def comd(self):
        self.med.showLifers()

class ShowEntry(Menucommand):
    def __init__(self, root, label, med):
        super().__init__(root, label)
        self.med = med
    def comd(self):
        self.med.showList()

class ShowCast(Menucommand):
    def __init__(self, root, label, med):
        super().__init__(root, label)
        self.med = med
    def comd(self):
        self.med.showCast()

class ShowAudience(Menucommand):
    def __init__(self, root, label, med):
        super().__init__(root, label)
        self.med = med
    def comd(self):
        self.med.showAudience()

class ShowDonors(Menucommand):
    def __init__(self, root, label, med):
        super().__init__(root, label)
        self.med = med
    def comd(self):
        self.med.showDonors()

class ShowDonations(Menucommand):
    def __init__(self, root, label, med):
        super().__init__(root, label)
        self.med = med
    def comd(self):
        self.med.showDonations()

class NickEdit(Menucommand):
    def __init__(self, root, label, med):
        super().__init__(root, label)
        self.med = med
    def comd(self):
        self.med.editNicknames()



class ClearButton(DButton):
    def __init__(self, root, med, **kwargs):
        super().__init__(root, text="Clr", width=5)
        self.med = med

    def comd(self):
        self.med.clearClicked()

class AddButton(DButton):
    def __init__(self, root, med, **kwargs):
        super().__init__(root, text="Add", width=10)
        self.med = med

    def comd(self):
        self.med.addClicked()

class DeleteButton(DButton):
    def __init__(self, root, med, **kwargs):
        super().__init__(root, text="Delete", width=10)
        self.med = med

    def comd(self):
        self.med.delClicked()


class Builder():
    def build(self, datafile):
        self.datafile = datafile
        root = tk.Tk()
        root.geometry("750x600")
        root.title("Troupers database")
        frame = Frame(root)
        menubar = Menubar(root)
        med = Mediator()
        med.datafile = self.datafile


        # create the File menu and its children
        filemenu = TopMenu(root, "File", menubar)
        filemenu.addMenuitem(Menucommand(root, "New"))
        filemenu.addMenuitem(OpenCommand(root, "Open", med))
        filemenu.addMenuitem(Readcommand(root, "Read", med))
        filemenu.addSeparator()
        filemenu.addMenuitem(Quitcommand(root, "Exit"))

        tableMenu = TopMenu(root, "Tables", menubar)
        tableMenu.addMenuitem(Boardmembers(root, "Board", med))
        tableMenu.addMenuitem(Lifemembers(root, "Lifers", med))
        tableMenu.addMenuitem(ShowAudience(root, "Audience", med))

        showMenu = TopMenu(root, "Shows", menubar)
        showMenu.addMenuitem(ShowCast(root, "Cast", med))
        showMenu.addMenuitem(ShowEntry(root, "Show list", med))

        donorMenu =  TopMenu(root, "Donations", menubar)
        donorMenu.addMenuitem(ShowDonors(root, "Donors", med))
        donorMenu.addMenuitem(ShowDonations(root, 'Donations', med))
        donorMenu.addMenuitem( NickEdit(root, 'Nicknames', med))


        # search controls
        srchEntry = Entry(root)
        med.setSearchfield(srchEntry)
        srchEntry.grid(row=0, column=2)
        srchEntry.bind("<KeyRelease>", med.keyClick)


        clrButton=ClearButton(root, med)
        clrButton.grid(row=0, column=3)


        # set up main Treeview
        self.mainTree = Treeview(root, height=20)
        self.mainTree["columns"] = ("frname","lname", "address", "town", "state", "zip","email", "phone", "phone2")
        self.mainTree.column("#0", width=20, minwidth=20, stretch=NO) #first name
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
        med.setMainTree(self.mainTree)
        self.mainTree.grid(row=1, column=0, columnspan=4)
        self.mainTree.bind("<Double-1>", med.treeDouble)
        self.mainTree.bind("<Button-1>", med.treeClick)

    #Add buttons at bottom
        addButton = AddButton(root, med)
        addButton.grid(row=2, column=1, padx=5,pady=10, sticky=E)
        delButton = DeleteButton(root, med)
        delButton.grid(row=2, column =2, padx=5,pady=10, sticky=W)
        med.setDelButton(delButton)
        delButton.disable()  #disabed unless person selected


# ----------------------------
def main():
    if len(sys.argv)>1:
        datafile = sys.argv[1]
        print (sys.argv[1])
    else:
        datafile =""
    Builder().build(datafile)
    mainloop()

###  Here we go  ####
if __name__ == "__main__":
    main()