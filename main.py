#!python3

import os
import sys

from pathlib import Path

# local file
from globalVar import *

from argvparser import argvparses
from thingExtractor import ThingControl, ThingFile


def chdir():
	path = Path(sys.argv[0])
	os.chdir(path.parent)

def InteraciveConsole(argsList):
	print(f"Interacive mode Starting.")
	print(f"on empty inpute name convserver on ctrl + D skip")
	control = ThingControl()
	for args in argsList:
		thing = ThingFile(**args)
		try:
			dst = input(f"extraction, {thing.zipSrc} -> {thing.dst}: ")
			if dst != "":
				thing.dst = dst
			ret = input(f"Remove ZipSource (y/N): ")
			thing.delZip = ret in YES_TEXT
			move_zip = input(f"Move ZipSource (y/N): ")
			if move_zip in YES_TEXT:
				new_zipDst = input(f"Move {thing.zipSrc} to : ")
				thing.zipDst = new_zipDst
			else:
				thing.zipDst = None
			ret = input(f"Remove {README_NAME} (y/N): ")
			thing.delReadme = ret in YES_TEXT
			ret = input(f"Remove {LICENSE_NAME} (y/N): ")
			thing.delLicense = ret in YES_TEXT
		except EOFError:
			continue 
		control.OneExtraction(thing)

def mainConsole():
	argv = argvparses()
	zipList = argv.srcList
	argsList = []
	for zipFile in zipList:
		if Path(zipFile).exists():
			args = {
				'zipSrc': zipFile,
    			'dstDir': argv.dstDir,
    			'dstName': None,
    			'zipDstDir': argv.zipDstDir,
    			'zipDstName': None,
    			'delReadme': argv.delReadme,
    			'delLicense': argv.delLicense,
    			'delZip': argv.delZip,
			}
		else:
			eprint(f"Error: {zipFile} not found. skip")
		argsList.append(args)
	if not argv.interactive:
		control = ThingControl(argsList)
		control.RunExtraction()
	else:
		InteraciveConsole(argsList)


if __name__ == "__main__":
	mainConsole()

#if __name__ == "__main__":
#	if ThingGui.EnabalGui():
#		# Mode Gui
#		chdir()
#		mainGui()
#		
#	else:
#		# Mode Console
#		mainConsole()