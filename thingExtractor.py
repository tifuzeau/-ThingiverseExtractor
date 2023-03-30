#!python3

import os
import sys
import zipfile
import shutil

from pathlib import Path

from config import ConfigModel, ConfigControl
from globalVar import *

class ThingFile(ConfigModel):
	"""
		Model
	"""
	def __init__(self, zipSrc, dstDir=None, dstName=None, zipDstDir=None, zipDstName=None,
			delReadme=None, delLicense=None, delZip=None):
		super().__init__()
		self.zipSrc = Path(zipSrc)

		# extraction dst
		if not dstDir:
			dstDir = "."
		self.dstDir = Path(dstDir)
		if not dstName:
			dstName = self.zipSrc.stem
		self.dstName = Path(dstName)
		# zip dst

		if not zipDstDir:
			self.zipDstDir = None
		else:
			self.zipDstDir = Path(zipDstDir)
		if not zipDstName:
			zipDstName = self.zipSrc.name
		self.zipDstName = Path(zipDstName)

	def __setattr__(self, name, value):
		#Dst
		if name == "dst":
			if not value:
				return
			dst = Path(value)
			self.dstDir = dst.parent.resolve()
			self.dstName = dst.name
			print(f"set dst: {value} -> parent {self.dstDir}, Name: {self.dstName}")
		#ZipDst
		if name == "zipDst":
			if not value:
				self.zipDstDir = None
				self.zipDstName = None
			else:
				zipDst = Path(value)
				self.zipDstDir = zipDst.parent.resolve()
				self.zipDstName = zipDst.name
		#End
		else:
			super().__setattr__(name, value)

	def __getattribute__(self, name):
		#Dst
		if name == "dst":
			return self.dstDir / self.dstName
		#ZipDst
		if name == "zipDst":
			if not self.zipDstDir:
				return None
			return self.zipDstDir / self.zipDstName
		#End
		else:
			return super().__getattribute__(name)

class ThingControl(ConfigControl):
	"""
		Control
	"""

	def __init__(self, zipList = None):
		super().__init__()
		self.ThingList = []
		if not zipList:
			return
		self.FeedList(zipList)

	def AppendArg(self, arg):
		self.ThingList.append(ThingFile(arg))

	def AppendThing(self, thing):
		self.ThingList.append(thing)

	def FeedList(self, argsList):
		for args in argsList:
			if Path(args['zipSrc']).exists():
				self.ThingList.append(ThingFile(**args))

	def _Checkdst(self, dst):
		if dst.parent.exists() == False:
			print(f"mkdir: {dst.parent}")
			dst.parent.mkdir()
		if dst.exists():
			return False
		return True

	def ZipExtractor(self, thing):
		if self._Checkdst(thing.dst) == False:
			print(f"Error: {thing.dst} already exists")
			return False
		with zipfile.ZipFile(thing.zipSrc, 'r') as fd:
			fd.extractall(thing.dst)
		print(f"Extraction: {thing.zipSrc} to {thing.dst}")
		return True

	def DeleteFile(self, path):
		path.unlink()
		print(f"Remove: {path.name}")

	def MoveZip(self, thing):
		if not thing.zipDst:
			return
		if not self._Checkdst(thing.zipDst):
			print(f"Error: {thing.zipDst} already exists")
		shutil.move(str(thing.zipSrc.resolve()), str(thing.zipDst.resolve()))
		print(f"Move: {thing.zipSrc} to {thing.zipDst}")

	def OneExtraction(self, thing):
		if not self.ZipExtractor(thing):
			return
		if thing.delReadme:
			self.DeleteFile(thing.dst / README_NAME)
		if thing.delLicense:
			self.DeleteFile(thing.dst / LICENSE_NAME)
		if thing.delZip:
			self.DeleteFile(thing.zipSrc)
		else:
			self.MoveZip(thing)

	def RunExtraction(self):
		for thing in self.ThingList:
			self.OneExtraction(thing)
