import configparser

from pathlib import Path

class ConfigModel:
	"""
		Model of config
	"""

	def __init__(self):
		#path
		self.defaultDstDir = None
		self.defaultZipDst = None
		#delete var
		self.delReadme = None
		self.delLicense = None
		self.delZip = None

class ConfigControl(ConfigModel):
	"""
		Controleur of Config Model
	"""

	# For get in file
	SectionName = "Default Value"
	InitialName = "InitalDir"
	DestName = "DestDir"
	ZipName = "ZipDest"
	#delete thing
	NameDeleteReadme = "DeleteReadme"
	NameDeleteLicense = "DeleteLicense"
	NameDeleteZip = "DeleteZip"

	def __init__(self):
		super().__init__()

	def MakePath(self, path):
		if not isinstance(path, Path):
			return Path.home() / Path(path)
		return path

	def SetFromFile(self, cfg_file):
		config = configparser.ConfigParser()
		configPath = self.MakePath(cfg_file)
		if not configPath.exists():
			print(f"error: {cfg_file} Not found")
			return
		config.read(configPath)
		default = config[self.SectionName]
		#Path
		self.DefaultDstDir = default.get(self.DestName)
		self.DefaultZipDst = default.get(self.ZipName)
		#Del Flag
		self.delReadme = default.getboolean(self.NameDeleteReadme)
		self.delLicense = default.getboolean(self.NameDeleteLicense)
		self.delZip = default.getboolean(self.NameDeleteZip)

	def SetFromArg(self, arg):
		#Path
		self.DefaultDstDir = arg.dstDir
		self.DefaultZipDst = arg.ZipDst
		#Del Flag
		self.delReadme = arg.delReadme
		self.delLicense = arg.delLicense
		self.delZip = arg.delZip

	def SaveToFile(self, path):
		configPath = self.MakePath(path)
		config = configparser.ConfigParser()
		config.add_section(self.SectionName)
		#Path
		config.set(self.SectionName, self.DestName, str(self.defaultDstDir))
		config.set(self.SectionName, self.ZipName, str(self.defaultZipDst))
		#Del flag
		config.set(self.SectionName, self.NameDeleteReadme, str(self.delReadme))
		config.set(self.SectionName, self.NameDeleteLicense, str(self.delLicense))
		config.set(self.SectionName, self.NameDeleteZip, str(self.delZip))
		
		with open(configPath.resolve(), "w") as fd:
			config.write(fd)
		configPath.chmod(0o755)

class ConfigView:
	
	@staticmethod
	def PrintAll(config):
		print(f"Dst dir: {config.defaultDstDir}")
		print(f"Zip dir: {config.defaultZipDst}")
		print(f"del Readme: {config.delReadme}")
		print(f"del License: {config.delLicense}")
		print(f"del Zip: {config.delZip}")
