"""Checkbox class derived from Checkbutton
includes get methods to get the name var state"""
from tkinter import Checkbutton, DISABLED


class Checkbox(Checkbutton):
    def __init__(self, root, btext, gvar):
        super().__init__(root, text=btext, variable=gvar)
        self.text=btext
        self.var = gvar

    def getText(self):
        return self.text
    def getVar(self):
        return self.var.get()   #get the value stored in this IntVar