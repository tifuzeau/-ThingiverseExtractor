try:
	from tkinter import filedialog
	from tkinter import messagebox
	from tkinter import Tk
except ImportError:
	filedialog = None
	messagebox = None
	Tk = None

def initTk():
	root = Tk()
	root.withdraw()
	return root

def eprintGui(msg):
	title = "Error"
	messagebox.showerror(title=title, message=msg)

def GetZipList(initalDir):
    title = "Zip Selection"
    msg = "Select zip file to extract. Use ctrl for multiple selection"
    messagebox.showinfo(title=title, message=msg)
    initialdir = initalDir
    filetype = (("zip file", "*.zip"),)
    zipList = filedialog.askopenfilenames(initialdir=initialdir, title=title, filetypes=filetype, multiple=True)
    return zipList
