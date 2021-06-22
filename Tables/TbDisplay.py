from tkinter import Toplevel, NO
from tkinter.ttk import Treeview

from DataDisplay.Dbuttons import DButton
from Database.DBUtils import Query
from PeopleEditor.People import CsvExport


class TableDisplay():
    def __init__(self, med):
        self.med = med
        self.frame = Toplevel(master=None)
        self.med.setTreetop(self.frame)
        self.frame.geometry("825x400")
        self.frame.title("Cast Members")
        self.mainTree = Treeview(self.frame)
        self.mainTree = Treeview(self.frame, height=14)
        # self.mainTree.grid(row=0, column=0)

        self.mainTree["columns"] = (
            "frname", "lname", "role", "address", "town", "state", "zip", "email", "phone", "phone2")
        self.med.setColnames(self.mainTree['columns'])
        self.mainTree.column("#0", width=20, minwidth=20, stretch=NO)  # first name
        self.mainTree.column("frname", width=80, stretch=NO)
        self.mainTree.column("lname", width=80, stretch=NO)
        self.mainTree.column("role", width=80, stretch=NO)
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
        self.mainTree.heading("role", text="Role")

        self.mainTree.heading("address", text="Address")
        self.mainTree.heading("town", text="Town")
        self.mainTree.heading("state", text="State")
        self.mainTree.heading("zip", text="Zip")
        self.mainTree.heading("email", text="Email")
        self.mainTree.heading("phone", text="Mobile")
        self.mainTree.heading("phone2", text="Home")
        #med.setTree(self.mainTree)
        self.mainTree.grid(row=0, column=0, columnspan=4)

        qry = """select patrons.personkey, frname, lname,rolename, address, town, state, zipcode, email, phone, phone2 from patrons, cast 
              where patrons.personkey=cast.personkey and cast.showkey="""+str(med.getShowkey())+" order by lname"

        query = Query(self.med.db.cursor, qry)
        results = query.execute()
        rows = results.getRows()
        query = Query(med.db.cursor, qry)
        results = query.execute()
        rows = results.getRows()
        # = self.med.getTree()
        tree = self.mainTree
        index = 0
        for r in rows:
            riter = iter(r)

            tree.insert("", index, text=next(riter), values=(
                next(riter), next(riter), next(riter), next(riter), next(riter),
                next(riter), next(riter), next(riter), next(riter),next(riter)))
            index = index + 1
        exportButton = cExportButton(self.frame, self.med, results)
        exportButton.grid(row=5, column=0)


# exports current table
class cExportButton(DButton):
    def __init__(self, master, med, results, **kwargs):
        self.med = med
        self.results = results
        super().__init__(master, text="Export", **kwargs)

    def comd(self):
        # export csv file of this query
        CsvExport.export(self.results, "Castmembers.csv", self.med.getColnames())

