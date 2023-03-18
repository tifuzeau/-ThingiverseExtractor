#!python3

import os
import sys

from pathlib import Path

# local file
from globalVar import *

from argvparser import argvparses
from thingExtractor import ThingExtractor

from gui import *
from config import Config


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
			extractionList.append(ThingExtractor(src=zipFile, dstDir=config.dstDir, dstName=None, archivedstDir=config.archiveDst, delete=config.deleteArchive, interactive=config.interactive))
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
			extractionList.append(ThingExtractor(src=zipFile, dstDir=argv.dstDir, dstName=None, archivedstDir=argv.archiveDst, delete=argv.deleteArchive, interactive=argv.interactive))
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