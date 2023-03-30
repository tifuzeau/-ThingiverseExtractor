	def _initPopUp(self):
		title = "Init Config"
		msg = "Follow initalitation of config file"
		ret = messagebox.askyesno(title=title, message=msg)
		return ret

	def _initSourceDir(self):
		title = "Initial Dir for selection"
		source_folder = filedialog.askdirectory(title=title)
		return Path(source_folder)

	def _initDestDir(self):
		title = "Dir for extraction"
		dest_folder = filedialog.askdirectory(title=title)
		return Path(dest_folder)

	def _initDeleteZip(self):
		title = "Delete Zip"
		msg = "Do you whant to delete Zip file after extraction"
		ret = messagebox.askyesno(title=title, message=msg, default="no")
		return ret

	def _initZipDest(self):
		title = "Zip Dest"
		dest_Zip = filedialog.askdirectory(title=title)
		return Path(dest_Zip)

			def InitConfigFile(self, configPath):
		if not self._initPopUp():
			self.confError = True
			return
		self.initalDir = self._initSourceDir()
		self.destDir = self._initDestDir()
		self.deleteZip = self._initDeleteZip()
		self.ZipDest = self._initZipDest()
		self.interactive = self._initInteractive()
		self._SaveConfig(configPath)
