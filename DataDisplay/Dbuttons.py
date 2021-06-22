from tkinter import *
from tkinter.ttk import *

from tkinter import *
from tkinter.ttk import *

# Command interface
class Command():
    def comd(self):pass

#derived button class with an abstract comd method
class DButton(Button, Command):
    def __init__(self, master,  **kwargs):
        super().__init__(master, command=self.comd, **kwargs)

    def disable(self):
        try:
            self.state(['disabled'])
        except AttributeError:
            self.configure(state="disable")

    def enable(self):
        self.state(['!disabled'])
