from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

from DataDisplay.Choicebuttons import ChoiceButton
from DataDisplay.Dbuttons import DButton
from Database.DBUtils import Query
from Tables.TbDisplay import TableDisplay


class Assign(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="<--Assign", **kwargs)

    def comd(self):
        self.med.addCast()


class VoiceChoice(ChoiceButton):
    def __init__(self, root, name, index, gvar, med):
        super().__init__(root, name, index, gvar)
        self.med = med
        self.index = index

    def comd(self):
        self.med.voiceClicked(self.index)


class CMediator():
    def __init__(self, db):
        self.db = db
        # use this database
        #qry = "use trouperspatrons"
        #query = Query(self.db.cursor, qry)
       # results = query.execute()
        self.voiceList = ["Soprano", "Alto", "Tenor", "Bass"]

    def getDB(self):
        return self.db

    def setPatlist(self, plist):
        self.patList = plist

    def setEntry(self, srch):
        self.srchEntry = srch

    def setCastlist(self, ctree):
        self.ctree = ctree

    def getCastlist(self):
        return self.ctree

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
        self.fillCast(self.showkey)

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
        pe = PersonEdit(self.db, self, self.patkey)

    def setColnames(self, cnames):
        self.colnames = cnames
    def getColnames(self):
        return self.colnames

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

    def addCast(self):
        rolename = self.roleName.get()
        cindex = self.showlist.curselection()
        index = cindex[0]
        showkey = self.showkeys[index]
        cindex = self.patList.curselection()
        patkey = self.keys[cindex[0]]
        roletype = self.roleType.get()
        qry = "Insert into cast (showkey, personkey, roletype, rolename) values(%s,%s, %s, %s)"
        val = (showkey, patkey, roletype, rolename)
        #print(qry)
        #print(val)
        self.db.cursor.execute(qry, val)
        self.db.commit()
        self.fillCast(showkey)
        self.roleName.delete(0,END)

    def fillCast(self, index):
        # qry= """select personkey, frname, lname, rolename from patrons, cast
        # where shows.personkey=patrons.personkey order by patrons.sex desc,
        # cast.roletype where shows.showkey=\'"""+str(index)+"\'"
        qry = """select castkey, frname, lname, rolename from patrons as p, cast as c
        where c.personkey=p.personkey and c.showkey=""" + str(
            index) + " order by c.roletype,  p.sex desc"
        print(qry)
        query = Query(self.db.cursor, qry)
        results = query.execute()
        rows = results.getRows()
        index = 0
        self.ctree.delete(*self.ctree.get_children())
        for r in rows:
            riter = iter(r)
            self.ctree.insert("", index, text=next(riter), values=(
                next(riter), next(riter), next(riter)))
            # next(riter), next(riter), next(riter), next(riter), next(riter)))
            index = index + 1

class TableButton(DButton):
        def __init__(self, master, med, **kwargs):
            self.med = med
            super().__init__(master, text="Show table", **kwargs)

        def comd(self):
            tbd = TableDisplay(self.med)

class EditButton(DButton):
    def __init__(self, master, med, **kwargs):
        self.med = med
        super().__init__(master, text="Edit", **kwargs)

    def comd(self):
        tree = self.med.getCastlist()
        curitem = tree.focus()
        print("edit person")
        self.med.editPerson(tree.item(curitem))


class PersonEdit():

    def __init__(self, db, med, key):
        self.frame = Toplevel(master=None)
        self.frame.geometry("300x100")
        self.db = db
        self.med=med
        self.key = key
        qry = "select castkey, frname, lname,rolename from patrons, cast " \
              "where cast.personkey = patrons.personkey and castkey = " + str(key)
        query = Query(self.db.cursor, qry)
        results = query.execute()
        rows = results.getRows()
        r = rows[0]
        riter = iter(r)
        self.castkey = int(next(riter))
        self.name = next(riter) + " " + next(riter)
        role = next(riter)
        lb1 = Label(self.frame, text=self.name)
        lb1.grid(row=0, column=1, sticky=EW)
        self.roleentry = Entry(self.frame)
        self.roleentry.insert(0, role)
        self.roleentry.grid(row=1, column=1, sticky=EW)
        sv = Button(self.frame, text="Save", command=self.saveRow)
        sv.grid(row=2, column=0, pady=5)
        exitBtn = Button(self.frame, text="Close", command=self.exitC)
        exitBtn.grid(row=2, column=1, padx=5,pady=5)
        delBtn = Button(self.frame, text="Delete", command=self.deleterow)
        delBtn.grid(row=2, column=2, padx=5,pady=5)

    def saveRow(self):
        name = self.roleentry.get()
        qry = "update cast set rolename=\'" + name + "\' where castkey=" + str(self.castkey)
        query = Query(self.db.cursor, qry)
        query.execute()
        self.db.commit()
        #self.med.fillCast(self.showkey)
        self.exitC()

    def deleterow(self):
        ans = messagebox.askyesno("Delete?", "Do you want to delete " + self.name)
        if ans == YES:
            qry = "delete from cast where castkey=" + str(self.castkey)
            query = Query(self.db.cursor, qry)
            query.execute()
        self.exitC()

    def exitC(self):
        self.frame.destroy()


class Casting():
    def __init__(self, db):
        self.db = db

    def builder(self):
        self.frame = Toplevel(master=None)
        self.frame.geometry("670x500")
        self.med = CMediator(self.db)

        self.castList = Treeview(self.frame, height=14)
        self.castList["columns"] = ("frname", "lname", "rolename")
        self.castList.column("#0", width=20, minwidth=20, stretch=NO)  # key
        self.castList.column("frname", width=80, stretch=NO)
        self.castList.column("lname", width=80, stretch=NO)
        # self.castList.column("roletype", width=5, stretch=NO)
        self.castList.column("rolename", width=100, stretch=NO)
        self.castList.heading('#0', text="key")
        self.castList.heading("frname", text="Frname")
        self.castList.heading("lname", text="Lname")
        # self.castList.heading("roletype", text="type")
        self.castList.heading("rolename", text="Role")
        self.castList.grid(row=0, column=0, rowspan=3, sticky=N)
        self.med.setCastlist(self.castList)

        editButton = EditButton(self.frame, self.med)
        editButton.grid(row=3, column=0)

        rframe = Frame(self.frame)
        self.srchEntry = Entry(rframe, width=30)
        self.srchEntry.grid(row=0, column=0, sticky=N)
        self.srchEntry.bind("<KeyRelease>", self.med.keyClick)
        self.med.setEntry(self.srchEntry)

        self.patlist = Listbox(rframe, height=20, width=30, exportselection=False)
        self.patlist.grid(row=1, column=0, rowspan=4, sticky=N)
        self.med.setPatlist(self.patlist)
        rframe.grid(row=0, column=2)

        cFrame = Frame(self.frame)
        self.showList = Listbox(cFrame, width=30, height=8, exportselection=False)
        self.showList.grid(row=0, column=0, rowspan=2, sticky=N)
        self.med.setShowlist(self.showList)
        self.showList.bind('<<ListboxSelect>>', self.med.showClick)

        lb1 = Label(cFrame, text="Character", foreground='blue')
        lb1.grid(row=2, column=0, sticky=N)
        self.roleName = Entry(cFrame, width=20)
        self.roleName.grid(row=3, column=0, sticky=N)
        self.med.setRolename(self.roleName)

        lbframe = LabelFrame(cFrame, text="Role type")
        lbframe.grid(row=4, column=0, sticky=N)
        self.roleType = IntVar()
        self.roleType.set(0)
        ck1 = ChoiceButton(lbframe, 'Lead', 0, self.roleType)
        ck2 = ChoiceButton(lbframe, 'Minor lead', 1, self.roleType)
        ck3 = ChoiceButton(lbframe, 'Chorus', 2, self.roleType)
        ck4 = ChoiceButton(lbframe, 'Tech', 3, self.roleType)
        ck5 = ChoiceButton(lbframe, 'Accomp', 4, self.roleType)
        ck6 = ChoiceButton(lbframe, 'Director', 5, self.roleType)
        ck1.grid(row=0, column=0, sticky=W)
        ck2.grid(row=1, column=0, sticky=W)
        ck3.grid(row=2, column=0, sticky=W)
        ck4.grid(row=3, column=0, sticky=W)
        ck5.grid(row=4, column=0, sticky=W)
        ck6.grid(row=5, column=0, sticky=W)
        cFrame.grid(row=0, column=1, sticky=N, pady=5)
        self.med.setRoletype(self.roleType)

        # Voice parts SATB are numbere 0-3 and match array in the Mediator
        # Clicking on these puts that voice part name in the role entry field
        # No database lookup is used
        vFrame = Labelframe(self.frame, text="Voice part")
        self.voice = IntVar()
        vk1 = VoiceChoice(vFrame, 'S', 0, self.voice, self.med)
        vk2 = VoiceChoice(vFrame, 'A', 1, self.voice, self.med)
        vk3 = VoiceChoice(vFrame, 'T', 2, self.voice, self.med)
        vk4 = VoiceChoice(vFrame, 'B', 3, self.voice, self.med)
        self.voice.set(4)
        vk1.grid(row=0, column=0)
        vk2.grid(row=0, column=1)
        vk3.grid(row=1, column=0)
        vk4.grid(row=1, column=1)
        vFrame.grid(row=2, column=1)

        asButton = Assign(self.frame, self.med)
        asButton.grid(row=3, column=1)
        self.med.fillList()  # fill show list box

        tb = TableButton(self.frame, self.med)
        tb.grid(row=4, column=0)

    def getRoletype(self):
        return self.roleType


