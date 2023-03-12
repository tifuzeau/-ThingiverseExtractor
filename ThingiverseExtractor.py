#!python3

import os
import sys
import zipfile
import shutil
import argparse
import configparser

from pathlib import Path

try:
	from tkinter import filedialog
	from tkinter import messagebox
	from tkinter import Tk
except ImportError:
	filedialog = None
	messagebox = None
	Tk = None


CFG_FILE = "config.ini"

def eprintGui(msg):
	title = "Error"
	messagebox.showerror(title=title, message=msg)

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def initTk():
	root = Tk()
	root.withdraw()
	return root


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
	DeleteName = "DeleteArchive"
	InteractiveName = "Interactive"


	def __init__(self, cfg_Path):
		config = configparser.ConfigParser()
		configPath = Path(cfg_Path)
		self.confError = False
		if not configPath.exists():
			self.InitConfigFile(configPath)
			return
		config.read(cfg_Path)
		default = config[self.SectionName]
		self.initalDir = default.get(self.InitialName)
		self.dstDir = default.get(self.DestName)
		self.archiveDst = default.get(self.ArchiveName)
		self.deleteArchive = default.getboolean(self.DeleteName)
		self.interactive = default.getboolean(self.InteractiveName)

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
	
	def _initInteractive(self):
		title = "Interactive Statu"
		msg  = "Do you whant to always active interactive mode"
		ret = messagebox.askyesno(title=title, message=msg, default="no")
		return ret

	def _SaveConfig(self, configPath):
		config = configparser.ConfigParser()
		config.add_section(self.SectionName)
		config.set(self.SectionName, self.InitialName, str(self.initalDir))
		config.set(self.SectionName, self.DestName, str(self.destDir))
		config.set(self.SectionName, self.ArchiveName, str(self.archiveDest))
		config.set(self.SectionName, self.DeleteName, str(self.deleteArchive))
		config.set(self.SectionName, self.InteractiveName, str(self.interactive))
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


class FileToExtract:

	def __init__(self, src, dstDir, dstName=None, archivedstDir=None, delete=False, interactive=False, perror=None):
		self.src = Path(src)
		self.dstDir = Path(dstDir)
		self.dstPath = None
		self.archiveDstDir = Path(archivedstDir)
		self.archiveDstPath = self.archiveDstDir / self.src.name
		self.delete = delete
		self.UpdateDstPath(dstName)

	def perror(self, msg):
		print(msg, file=sys.stderr)

	def UpdateDstPath(self, dstName):
		if not dstName:
			dstName = self.src.stem
		self.dstPath = self.dstDir / dstName

	def Checkdst(self, dst):
		"""
		Returns
		-------
		bool:
			False if error 
		"""
		if dst.parent.exists() == False:
			print(f"mkdir: {dst.parent}")
			dst.parent.mkdir()
		if dst.exists():
			return False
		return True	

	def ExtractFile(self, src, dst):
		if self.Checkdst(self.dstPath) == False:
			self.perror(f"Error: {self.dstPath} already exists")
			return False
		with zipfile.ZipFile(src, 'r') as fd:
			fd.extractall(dst)
		print(f"Extraction: {src} to {dst}")
		return True

	def deleteArchive(self):
		self.src.unlink()
		print(f"Remove: {self.src.name}")


	def moveArchive(self):
		if not self.Checkdst(self.archiveDstPath):
			self.perror(f"Error: {self.archiveDstPath} already exists")
		shutil.move(str(self.src.resolve()), str(self.dstPath.resolve()))
		print(f"Move: {self.src} to {self.archiveDstPath}")
		
	
	def Run(self):
		if not self.ExtractFile(self.src, self.dstPath):
			return      
		if self.delete:
			self.deleteArchive()
		else:
			self.moveArchive()
			


def argvparses():
	"""
		Fonction to conf argparse and set somme default var
	"""
	parser = argparse.ArgumentParser()

	# Path thing
	parser.add_argument("--src", type=str, dest="srcList",nargs="+", help="Path of many zip file source", required=True)
	parser.add_argument("--dst", type=str, dest="dstDir", help="Destination path of extraction", default="./", required=False)
	parser.add_argument("--archivedst", type=str, dest="archiveDst", help="path to archive folder", default="./", required=False)

	# Other thing
	parser.add_argument("--DeleteArchive", "-D", action="store_true", dest="deleteArchive", help="To delete Archive file after extration", default=False ,required=False)
	parser.add_argument("--interactive", "-i", action="store_true", dest="interactive", help="set interactivemode", default=False, required=False)
	
	argv = parser.parse_args()
	return argv

def GetZipList(initalDir):
	title = "Zip Selection"
	msg = "Select zip file to extract. Use ctrl for multiple selection"
	messagebox.showinfo(title=title, message=msg)
	initialdir = initalDir
	filetype = (("zip file", "*.zip"),)
	zipList = filedialog.askopenfilenames(initialdir=initialdir, title=title, filetypes=filetype, multiple=True)
	return zipList

def InteraciveGui():
	pass

def chdir():
	path = Path(sys.argv[0])
	os.chdir(path.parent)

def mainGui():
	root = initTk()
	chdir()
	config = Config(CFG_FILE)
	if config.confError:
		return
	zipList = GetZipList(config.initalDir)
	if not zipList:
		return
	extractionList = []
	for zipFile in zipList:
		if Path(zipFile).exists():
			extractionList.append(FileToExtract(src=zipFile, dstDir=config.dstDir, dstName=None, archivedstDir=config.archiveDst, delete=config.deleteArchive, interactive=config.interactive))
		else:
			eprintGui(f"Error: {zipFile} not found. skip")
	if config.interactive:
		InteraciveGui(extractionList)
	for thing in extractionList:
		thing.Run()

def InteraciveConsole(zipList):
	print(f"Interacive mode Starting.")
	print(f"on empty inpute name convserver")
	for zipFile in zipList:
		new_dstName = input(f"{zipFile.src} -> {zipFile.dstPath}/")
		zipFile.UpdateDstPath(new_dstName)

def mainConsole():
	argv = argvparses()
	zipList = argv.srcList
	extractionList = []
	for zipFile in zipList:
		if Path(zipFile).exists():
			extractionList.append(FileToExtract(src=zipFile, dstDir=argv.dstDir, dstName=None, archivedstDir=argv.archiveDst, delete=argv.deleteArchive, interactive=argv.interactive))
		else:
			eprint(f"Error: {zipFile} not found. skip")
	if argv.interactive:
		InteraciveConsole(extractionList)
	for extra in extractionList:
		extra.Run()

if __name__ == "__main__":
	if Tk is None:
		# Mode Console
		mainConsole()
	else:
		# Mode Gui
		mainGui()