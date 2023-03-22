import configparser

from pathlib import Path

class Config:
	""" 
		Get or Make Config 

	Atributes
	---------

	*Name : str
		key and section name 
	initalDir : Path
		Path to the initial directori for zip searching
	destDir : Path
		Path of extractacting zip file
	archiveDest : Path
		Path where move zip file after extraction
	deleteArchive : Bool
		true for removing archine instaed of moving to archiveDest
	interactive : Bool
		true for asking name folder where sotr extraction


	"""
	SectionName = "Default Value"
	InitialName = "InitalDir"
	DestName = "DestDir"
	ArchiveName = "ArchiveDest"
	#delete thing
	NameDeleteReadme = "DeleteReadme"
	NameDeleteLicense = "DeleteLicense"
	NameDeleteArchive = "DeleteArchive"


	def __init__(self, cfg_Path):
		config = configparser.ConfigParser()
		configPath = Path(cfg_Path)
		self.confError = False
		if not configPath.exists():
			self.InitConfigFile(configPath)
			return
		config.read(cfg_Path)
		default = config[self.SectionName]
		#path
		self.initalDir = default.get(self.InitialName)
		self.dstDir = default.get(self.DestName)
		self.archiveDst = default.get(self.ArchiveName)
		#delete var
		self.deleteReadme = default.getboolean(self.NameDeleteReadme)
		self.deleteLicense = default.getboolean(self.NameDeleteLicense)
		self.deleteArchive = default.getboolean(self.NameDeleteArchive)

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

	def _initDeleteArchive(self):
		title = "Delete Archive"
		msg = "Do you whant to delete Zip file after extraction"
		ret = messagebox.askyesno(title=title, message=msg, default="no")
		return ret

	def _initArchiveDest(self):
		title = "Archive Dest"
		dest_Archive = filedialog.askdirectory(title=title)
		return Path(dest_Archive)


	def _SaveConfig(self, configPath):
		config = configparser.ConfigParser()
		config.add_section(self.SectionName)
		#path
		config.set(self.SectionName, self.InitialName, str(self.initalDir))
		config.set(self.SectionName, self.DestName, str(self.destDir))
		config.set(self.SectionName, self.ArchiveName, str(self.archiveDest))
		#delete 
		config.set(self.SectionName, self.NameDeleteReadme, str(self.deleteReadme))
		config.set(self.SectionName, self.NameDeleteLicense, str(self.deleteLicense))
		config.set(self.SectionName, self.NameDeleteArchive, str(self.deleteArchive))
		
		with open(configPath.resolve(), "w") as fd:
			config.write(fd)
		configPath.chmod(0o755)

	def InitConfigFile(self, configPath):
		if not self._initPopUp():
			self.confError = True
			return
		self.initalDir = self._initSourceDir()
		self.destDir = self._initDestDir()
		self.deleteArchive = self._initDeleteArchive()
		self.archiveDest = self._initArchiveDest()
		self.interactive = self._initInteractive()
		self._SaveConfig(configPath)
