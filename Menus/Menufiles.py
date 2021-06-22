import tkinter as tk
from tkinter import filedialog
from tkinter import *

# creates the menu bar
class Menubar(Menu):
    def __init__(self, root):
        super().__init__(root)
        root.config(menu=self)

   # def get(self):
    #    return self.menubar

# abstract base class for menu items
class Menucommand():
    def __init__(self, root, label):
        self.root = root
        self.label=label
    def getLabel(self):
        return self.label
    def comd(self): pass


# menu item that calls the file open dialog


# exits from the program
class Quitcommand(Menucommand):
    def __init__(self, root,  label):
        super().__init__(root,  label)
    def comd(self):
        sys.exit()

#this class represents the top menu item in each column
class TopMenu():
    def __init__(self, root, label, menubar):
        self.mb = menubar
        self.root = root
        self.fmenu = Menu(self.mb, tearoff=0)
        self.mb.add_cascade(label=label, menu=self.fmenu)

    def addMenuitem(self, mcomd):
        self.fmenu.add_command(label = mcomd.getLabel(),
                    command = mcomd.comd)

    def addSeparator(self):
        self.fmenu.add_separator()
