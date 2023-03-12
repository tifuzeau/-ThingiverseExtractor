#!python3

import os
import sys
import zipfile
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

CFG_FILE = "conf.ini"

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
		if not os.path.exists(cfg_Path):
			self.InitConfigFile()
			return
		config.read(cfg_Path)
		default = config[self.SectionName]
		self.initalDir = default.get(self.InitialName)
		self.destDir = default.get(self.DestName)
		self.archiveDest = default.get(self.ArchiveName)
		self.deleteArchive = default.getboolean(self.DeleteName)
		self.interactive = default.getboolean(self.InteractiveName)

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

	def _SaveConfig(self):
		config = configparser.ConfigParser()
		config.add_section(self.SectionName)
		config.set(self.SectionName, self.InitialName, str(self.initalDir))
		config.set(self.SectionName, self.DestName, str(self.destDir))
		config.set(self.SectionName, self.ArchiveName, str(self.archiveDest))
		config.set(self.SectionName, self.DeleteName, str(self.deleteArchive))
		config.set(self.SectionName, self.InteractiveName, str(self.interactive))
		with open(CFG_FILE, "w") as fd:
			config.write(fd)

	def InitConfigFile(self):
		self.initalDir = self._initSourceDir()
		self.destDir = self._initDestDir()
		self.deleteArchive = self._initDeleteArchive()
		self.archiveDest = self._initArchiveDest()
		self.interactive = self._initInteractive()
		self._SaveConfig()


class FileToExtract:

	def __init__(self, src, dstDir, dstName=None, archivedstDir=None, delete=False, interactive=False):
		self.src = Path(src)
		self.dstDir = Path(dstDir)
		self.dstPath = None
		self.archiveDstDir = Path(archivedstDir)
		self.archiveDstPath = self.archiveDstDir / self.src.name
		self.delete = delete
		self.UpdateDstPath(dstName)

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
		with zipfile.ZipFile(src, 'r') as fd:
			fd.extractall(dst)
		print(f"Extraction: {src} to {dst}")
	
	def Run(self):
		if self.Checkdst(self.dstPath) == False:
			eprint(f"Error: {self.dstPath} already exists")
			return
		self.ExtractFile(self.src, self.dstPath)      
		if self.delete:
			self.src.unlink()
			print(f"Remove: {self.src.name}")
			return
		if self.Checkdst(self.archiveDstPath):
			self.src.replace(self.archiveDstPath)
			print(f"Move: {self.src} to {self.archiveDstPath}")


def argvparses():
	"""
		Fonction to conf argparse and set somme default var
	"""
	parser = argparse.ArgumentParser()

	# Path thing
	parser.add_argument("--src", type=str, dest="srcList",nargs="+", help="Path of many zip file source", required=True)
	parser.add_argument("--dst", type=str, dest="dstPath", help="Destination path of extraction", default="./", required=False)
	parser.add_argument("--archivedst", type=str, dest="archiveDst", help="path to archive folder", default="./", required=False)

	# Other thing
	parser.add_argument("--DeleteArchive", "-D", action="store_true", dest="deleteArchive", help="To delete Archive file after extration", default=False ,required=False)
	parser.add_argument("--interactive", "-i", action="store_true", dest="interactive", help="set interactivemode", default=False, required=False)
	
	argv = parser.parse_args()
	return argv

def GetZipList(initalDir):
	title = "Zip Selection"
	initialdir = initalDir
	filetype = (("zip file", "*.zip"),)
	zipList = filedialog.askopenfilenames(initialdir=initialdir, title=title, filetypes=filetype, multiple=True)
	return zipList

def mainGui():
	root = initTk()
	config = Config(CFG_FILE)
	zipList = GetZipList(config.initalDir)
	for zipFile in zipList:
		print(zipFile)
	

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
			extractionList.append(FileToExtract(src=zipFile, dstDir=argv.dstPath, dstName=None, archivedstDir=argv.archiveDst, delete=argv.deleteArchive, interactive=argv.interactive))
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