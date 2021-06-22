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



# exports curret table
class ExportButton(DButton):
    def __init__(self, master, med, results, **kwargs):
        self.med = med
        self.results = results
        super().__init__(master, text="Export", **kwargs)

    def comd(self):
        # export csv file of this query
        CsvExport.export(self.results, "Audience.csv", self.med.getColnames())

# displays the board members in a Treeview
class ATableDisplay():
        def __init__(self, med):
            self.med = med
            self.frame = Toplevel(master=None)
            self.med.setTreetop(self.frame)
            self.frame.geometry("825x400")
            self.frame.title("Audience")
            self.mainTree = Treeview(self.frame)
            self.mainTree = Treeview(self.frame, height=14)
            # self.mainTree.grid(row=0, column=0)

            self.mainTree["columns"] = (
                "frname", "lname", "address", "town", "state", "zip", "email", "phone", "phone2")
            med.setColnames(self.mainTree["columns"])
            self.mainTree.column("#0", width=20, minwidth=20, stretch=NO)  # first name
            self.mainTree.column("frname", width=80, stretch=NO)
            self.mainTree.column("lname", width=80, stretch=NO)
           # self.mainTree.column("office", width=80, stretch=NO)
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
           # self.mainTree.heading("office", text="Office")
            self.mainTree.heading("address", text="Address")
            self.mainTree.heading("town", text="Town")
            self.mainTree.heading("state", text="State")
            self.mainTree.heading("zip", text="Zip")
            self.mainTree.heading("email", text="Email")
            self.mainTree.heading("phone", text="Mobile")
            self.mainTree.heading("phone2", text="Home")
            med.setTree(self.mainTree)
            self.mainTree.grid(row=0, column=0, columnspan=4)

            qry = """select patrons.personkey, frname, lname, address, town, state, zipcode, email, phone, phone2 from patrons, audience
                  where patrons.personkey=audience.personkey and audience.showkey = """\
                  +str(med.getShowKey())  + " order by lname"

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
