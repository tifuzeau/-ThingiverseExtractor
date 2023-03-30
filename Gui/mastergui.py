import os
import sys


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path

from Gui.NewLeft import LeftSettingView

from globalVar import *


def chdir():
	path = Path(sys.argv[0])
	os.chdir(path.parent)

def mainGui():
	chdir()
	gui = GuiThing()
	gui.root.mainloop()


class ThingView(tk.Frame):
	"""
		class to see thing
	"""

	def __init__(self, master, thing):
		super().__init__(master)
		self.thing = thing
		self.label = ttk.Label(master, text=self.thing.src)
		self.entry = ttk.Entry(master)


class GuiThing:
	"""
	"""

	def __init__(self):
		self.root = tk.Tk()
		self.root.title(GUI_TITLE)

		#Gui Frame
		self.LeftSetting = LeftSettingView(self.root)