import argparse

def argvparses():
	"""
		Fonction to conf argparse and set somme default var
	"""
	parser = argparse.ArgumentParser()

	# Path thing
	parser.add_argument("--src", type=str, dest="srcList",nargs="+", help="Path of many zip file source", required=True)
	parser.add_argument("--dst", type=str, dest="dstDir", help="Destination path of extraction", default="./", required=False)
	parser.add_argument("--zipdstDir", type=str, dest="zipDstDir", help="path to archive folder", default="./", required=False)

	# Other thing
	parser.add_argument("--DeleteReadme", action="store_true", dest="delReadme", help="todo", default=False)
	parser.add_argument("--DeleteLicense", action="store_true", dest="delLicense", help="todo", default=False)
	parser.add_argument("--DeleteZip", action="store_true", dest="delZip", help="todo", default=False)
	parser.add_argument("--interactive", "-i", action="store_true", dest="interactive", help="set interactivemode", default=False, required=False)
	
	argv = parser.parse_args()
	return argv
