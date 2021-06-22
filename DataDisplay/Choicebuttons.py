from tkinter import ttk
import tkinter as tk
from tkinter import *

# ChoiceButton is derived from RadioButton
class ChoiceButton(tk.Radiobutton):
    def __init__(self, rt, btext, index, gvar):
        super().__init__(rt, text=btext,
                         padx=20,
                         variable=gvar, value=index)

        self.index = index
        self.root=rt
       # self.color = color
        self.var = gvar
        self.text = btext
        super().configure(command=self.comd)  # set to 0 to get buttons

    def getText(self):
         return self.var

    # clicks are sent here
    def comd(self):
        pass
        #    print(self.index, self.color, self.var.get())
      #  self.root.configure(background=self.color)
