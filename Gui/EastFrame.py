

class EastFrame(tk.Frame):
	"""
	"""

	def __init__(self, masterWindow):
		super().__init__(masterWindow, highlightbackground="black", highlightthickness=1)
		self.grid(column=1, row=1, padx=2, pady=0, sticky="E")
		self.ThingList = None
		self.MakeFrame()

	def MakeFrame(self):
		self.SelectButton()

	def SelectButton(self):
		text = "Select Zip Files"
		self.select_button = tk.Button(self, text=text, command=self.GetZipList)
		self.select_button.grid(column=0, row=2, padx=2, pady=2)

	def GetZipList(self):
		pass

	def AddZipButton(self):
		self.select_button.config(text="Add Zip Files")
		self.RunButton()

	def _initText(self):
		self.ziptext = tk.Text(self)
		self.ziptext.grid(column=0, row=1)

	def _cleanDoublon(self, zipList):
		return zipList

	def UpdateZipList(self, zipList):
		if not self.ThingList:
			self.ThingList = []
		else:
			self._clearDoublon(zipList)
		for zipfile in zipList:
			self.ThingList.append(ThingExtractor(src=zipfile, dstDir=self.config.dstDir, archivedstDir=self.config.archiveDst ))
			self.ziptext.insert(tk.END, Path(zipfile).name + "\n")

		self.UpdateButton()
