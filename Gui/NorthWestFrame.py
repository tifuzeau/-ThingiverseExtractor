class NortWestFrame(tk.Frame):

	def __init__(self, master):
		super().__init__(master, highlightbackground="black", highlightthickness=1)
		self.grid(sticky="NW")
		self.SelectButton()

	# Button
	def SelectButton(self):
		text = "Select Zip Files"
		self.select_button = tk.Button(self, text=text, command=self.GetZipList)
		self.select_button.grid(column=0, row=2, padx=2, pady=2)

	def RunButton(self):
		text = "Run Extraction"
		self.run_button = tk.Button(self.root, text=text, command=self.Todo)
		self.run_button.grid(column=0, row=0, padx=2, pady=2, sticky="NW")

		# Zip List
	def GetZipList(self):
		title = "Zip Selection"
		initialdir = "."
		filetype = (("zip file", "*.zip"),)
		zipList = filedialog.askopenfilenames(initialdir=initialdir, title=title, filetypes=filetype, multiple=True)
		if not zipList:
			return
		self.UpdateZipList(zipList)

	def Todo(self):
		print("todo not a self")