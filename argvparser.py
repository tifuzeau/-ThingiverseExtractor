import argparse

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
