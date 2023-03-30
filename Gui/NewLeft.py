
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from globalVar import CFG_FILE
from config import ConfigControl, ConfigView

class Line(tk.Frame):
	row = 0

	def __init__(self, master):
		super().__init__(master)
		self.col = 0
		Line.row += 1
		self.MakeLine()

	def MakeLine(self):
		pass

class SettingLine(Line):

	def __init__(self, master, contentType, contentText , contentdefault, defaultEnableCheck=None):
		self.contentType = contentType
		self.contentText = contentText
		self.contentdefault = contentdefault
		self.defaultEnableCheck = defaultEnableCheck

		super().__init__(master)
		self.grid(column=0, row=self.row, sticky="w")

	def MakeLine(self):
		self.EnableCheckBox(self.defaultEnableCheck)
		self.Separator()
		getattr(self, self.contentType)(text=self.contentText, default=self.contentdefault)

	def ToggleState(self):
		self.Enable = not self.Enable
		self.UpdateContentState()

	def EnableCheckBox(self, default):
		self.Enable = tk.BooleanVar(value=default)
		args = {
			"text" : None,
			"variable" : self.Enable,
			"command" : self.ToggleState,
			"padx" : 2,
			"pady" : 2,
		}
		self.Enablecheckbox = tk.Checkbutton(self, **args)
		grid = {
			"column" : self.col,
			"row" : 0,
			"sticky" : "W",
			"padx" : 0,
			"pady" : 0,
		}
		self.col += 1
		self.Enablecheckbox.grid(**grid)
		self.master.grid_columnconfigure(0, minsize=20, weight=0)

	def Separator(self):
		self.separator = ttk.Separator(self, orient="vertical")
		grid = {
			"column" : self.col,
			"row" : 0,
			"sticky" : "NS",
			"padx" : 2,
			"pady" : 2,
		}
		self.col +=1
		self.separator.grid(**grid)
		self.master.grid_columnconfigure(1, minsize=20, weight=0)

	def UpdateContentState(self):
		if self.Enable:
			self.content["state"] = "normal"
		else:
			self.content["state"] = "disabled"

	def CheckBox(self, text, default):
		self.retvar = tk.BooleanVar(value=default)
		args = {
			"text" : text,
			"variable" : self.retvar,
			"comand" : None, # todo
			"padx" : 0,
			"pady" : 0,
		}
		self.content = tk.Checkbutton(self, **args)
		self.UpdateContentState()
		grid = {
			"column" : self.col,
			"row" : 0,
			"padx" : 2,
			"pady" : 2,
		}
		self.col += 1
		self.content.grid(**grid)

	def Entry(self, text, default):
		label = ttk.Label(self, text=text)
		labelGrid = {
			"column" : self.col,
			"row" : 0,
			"padx" : 0,
			"pady" : 0,
		}
		self.col += 1
		label.grid(**labelGrid)
		self.retvar = tk.StringVar(value=default)
		self.content = ttk.Entry(self, textvariable=self.retvar)
		self.UpdateContentState()
		entryGrid = {
			"column" : self.col,
			"row" : 0,
			"padx" : 2,
			"pady" : 2,
		}
		self.col += 1
		self.content.grid(**entryGrid)

	def GetContent(self):
		return self.Enable, self.retvar.get()
		

class SaveSetting(Line):

	def __init__(self, master, config, settingList):
		self.config = config
		self.settingList = settingList
		super().__init__(master)
		self.grid(column=0, row=self.row)
		

	def MakeLine(self):
		self.col = 1
		self.SaveButton()

	def Updateconfig(self):
		for key, obj in self.settingList.items():
			enable, value = obj.GetContent()
			if enable :
				self.config.__dict__[key] = value
			print(f"key: {key}, new value: {value}")

	def AskUser(self):
		args = {
			"title" : "Confirmation",
			"message" : "T sur gros",
		}
		return messagebox.askyesno(**args)

	def Save(self):
		if self.AskUser():
			ConfigView.PrintAll(self.config)
			self.Updateconfig()
			ConfigView.PrintAll(self.config)
			self.config.SaveToFile(CFG_FILE)
			#self.Config.SaveToFile(CFG_FILE)

	def SaveButton(self):
		text = "Save General"
		args = {
			"text" : text,
			"command" : self.Save
		}
		saveButton = tk.Button(self, **args)
		grid = {
			"column" : self.col,
			"row" : self.row,
			"padx" : 2,
			"pady" : 2,
		}
		saveButton.grid(**grid)


class LeftSettingView(tk.Frame):
	"""
	Methods
	------

	MakeFrame :
	
	TitelFrame : 
		creat Title of the Frame
	"""

	def __init__(self, master):
		super().__init__(master, highlightbackground="black", highlightthickness=1)
		self.Config = ConfigControl()
		self.Config.SetFromFile(CFG_FILE)
		self.grid(column=0, row=0, padx=2, pady=2, sticky="W")
		self.MakeFrame()

	def MakeFrame(self):
		self.TitleLine()
		self.settingList = {
			"defaultDstDir" : SettingLine(self, "Entry", "Dst Dir", self.Config.defaultDstDir, True),
			"defaultZipDst" : SettingLine(self, "Entry", "Dst Zip", self.Config.defaultZipDst, True),
			"delZip" : SettingLine(self, "CheckBox", "Remove Zip", self.Config.delZip, True),
			"delReadme" : SettingLine(self, "CheckBox", "Remove Readme", self.Config.delReadme, True),
			"delLicense" : SettingLine(self, "CheckBox", "Remove License", self.Config.delLicense, True),
		}
		self.SaveLine()

	def TitleLine(self):
		self.title = Line(self)
		self.title.label = ttk.Label(self, text="Setting")
		self.title.label.grid(column=0, row=0, padx=5, pady=5, sticky="N")

	def SaveLine(self):
		self.saveLine = SaveSetting(self, self.Config, self.settingList)