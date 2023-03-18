#!python3

import os
import sys
import zipfile
import shutil

from pathlib import Path

class ThingExtractor:

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
