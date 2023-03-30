
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

class LeftConfig(tk.Frame):
	"""
	"""

	def __init__(self, master):
		super().__init__(master, highlightbackground="black", highlightthickness=1)
		self.grid(column=0, row=1, padx=2, pady=2, sticky="W")
		self.MakeFrame()

	def MakeFrame(self):
		self.TitleFrame()
		self.ReadmeBox()
		self.LicenseBox()
		self.ZipBox()
		self.SaveButton()
	
	def TitleFrame(self):
		self.label = ttk.Label(self, text="Setting")
		self.label.grid(column=0, row=0, padx=5, pady=5, sticky="N")

	def ReadmeBox(self):
		text_readme = "Remove README.txt"
		self.checkbox_readme_var = tk.BooleanVar(value=False)
		self.checkbox_readme = tk.Checkbutton(self, text=text_readme, \
			variable=self.checkbox_readme_var, padx=2, pady=2)
		self.checkbox_readme.grid(column=0, padx=5, pady=5)

	def LicenseBox(self):
		text_license = "Remove LICENSE.txt"
		self.checkbox_License_var = tk.BooleanVar(value=False)
		self.checkbox_License = tk.Checkbutton(self, text=text_license, \
			variable=self.checkbox_License_var, padx=2, pady=2)
		self.checkbox_License.grid(column=0, padx=5, pady=5)
		
	def ZipBox(self):
		text_Zip = "Remove Zip.zip"
		self.checkbox_Zip_var = tk.BooleanVar(value=False)
		self.checkbox_Zip = tk.Checkbutton(self, text=text_Zip, \
			variable=self.checkbox_Zip_var, padx=2, pady=2)
		self.checkbox_Zip.grid(column=0, padx=5, pady=5)

	def SaveButton(self):
		self.button_save = ttk.Button(self, text="Save", command=self.SaveConfig)
		self.button_save.grid(column=0, padx=5, pady=5)

	def SaveConfig(self):
		print("Todo")
