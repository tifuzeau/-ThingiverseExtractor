import argparse

from globalVar import *

def argvparses():
	"""
		Fonction to conf argparse and set somme default var
	"""
	parser = argparse.ArgumentParser()

	# Path thing
	parser.add_argument("--src", type=str, dest="srcList",nargs="+", help="Path of many zip file source", required=True)
	parser.add_argument("--dst", type=str, dest="dstDir", help="Destination path of extraction", default="./", required=False)
	parser.add_argument("--zipdstDir", type=str, dest="zipDst", help="path to Zip folder", default="./", required=False)

	# Other thing
	parser.add_argument("--DeleteReadme", action="store_true", dest="delReadme", help=f"set to remove {README_NAME}", default=False)
	parser.add_argument("--DeleteLicense", action="store_true", dest="delLicense", help=f"set to remove {LICENSE_NAME}", default=False)
	parser.add_argument("--DeleteZip", action="store_true", dest="delZip", help="set to delete .zip", default=False)
	parser.add_argument("--interactive", "-i", action="store_true", dest="interactive", help="set interactivemode", default=False, required=False)
	
	argv = parser.parse_args()
	return argv
