import os
import sys

try:
	import tkinter as tk
	from tkinter import ttk
	from tkinter import filedialog
	from tkinter import messagebox
except ImportError:
	Tk = None


from NorthWestFrame import NortWestFrame
from WestFrame import WestFrame
from EastFrame import EastFrame

from globalVar import *


def chdir():
	path = Path(sys.argv[0])
	os.chdir(path.parent)

def mainGui():
	chdir()
	config = Config(CFG_FILE)
	if config.confError:
		return
	gui = ThingGui(config)
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

	def __init__(self, config):
		if tk is None:
			self.Error = True
			return
		self.Error = False
		self.root = tk.Tk()
		self.root.title(GUI_TITLE)
		self.config = config
		
		# Control
		self.controlThing = ControlGui(self.root)

		#Gui Frame
		self.NortWestFrame = NortWestFrame(self.root)
		self.WestFrame = WestFrame(self.root)
		self.EastFrame = EastFrame(self.root)


	@staticmethod
	def EnabalGui():
		if tk is None:
			return False
		return True


class ControlGui:

	def __init__(self):
		pass


	def RunExtraction(self):
		extractionList = []
		for zipFile in zipList:
			if Path(zipFile).exists():
				extractionList.append(ThingExtractor(src=zipFile, dstDir=config.dstDir, dstName=None, archivedstDir=config.archiveDst, delete=config.deleteArchive, interactive=config.interactive))
			else:
				eprintGui(f"Error: {zipFile} not found. skip")
		if config.interactive:
			InteraciveGui(extractionList)
		for thing in extractionList:
			thing.Run()