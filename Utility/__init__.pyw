from os import *
from pathlib import Path
from contextlib import redirect_stdout
from tkinter import Tk, PhotoImage, filedialog as fd, messagebox as MsgBox, TclError
del open

#-=-=-=-#

Main_File = path.abspath("../YTMVG.py")
Main_File_Directory = path.dirname(Main_File)
Main_File_Name = ".".join(path.basename(Main_File).split(".")[:-1])

# Won't even let me have the abspath of icon, ffs
Icon = path.join(Main_File_Directory, "Documents/Pictures/Icons/Icon.png")
Icon_HQ = path.join(Main_File_Directory, "Documents/Pictures/Icons/Icon_HQ.ico")

#-=-=-=-#

root = Tk()
root.withdraw()
try:
	if path.exists(Icon_HQ):
		root.iconbitmap(Icon_HQ)
except:
	if path.exists(Icon):
		root.call("wm", "iconphoto", root._w, PhotoImage(file = Icon))

#-=-=-=-#

def Folder_Size():
	"""Calculates folder size recursively"""
	Files = [str(File.resolve()) for File in Path(".").rglob("*")]
	Size = sum([os.path.getsize(File) for File in Files])
	return Size

def File_Size(Bytes: float) -> str:
	"""Returns human-readable file size"""
	for Unit in ["B", "KB", "MB", "GB", "TB"]:
		if Bytes < 1024:
			break
		Bytes /= 1024
	return "{0} {1}".format(round(Bytes, 2), Unit)