"""YTMVG Iterative Video Batch Processor."""
import sys
from os import *
from PIL import Image
from pathlib import Path
from shutil import rmtree
from time import sleep, time
from mutagen import File as mFile
from distro import id as distro_name
from tkinter import Tk, PhotoImage, messagebox as MsgBox, filedialog as fd, TclError
chdir(path.abspath(path.dirname(__file__)))
del open

#-=-=-=-=-=-#

__name__		= open(__file__).readlines()[0].rstrip("\n").strip('"').strip(".")
__author__	= "kubinka0505"
__credits__	= __author__
__version__	= "1.1"
__date__		= "01.01.2023"

#-=-=-=-=-=-#

# Directory with files
#
# Must contain at least one:
# - Audio file in formats below
# - Picture to be used as video, as above
Folder = r""

# YTMVG Location
YTMVG = r"../YTMVG.py"

#-=-=-=-#

# Searched file formats
Formats = {
	"Audio": ("MP3", "FLAC", "OGG"),
	"Image": ("PNG", "JPG", "JPEG", "WebP", "BMP")
}

# Additional processing arguments
# !!! Use long names !!!
Arguments = "--color 1", "--no-bell"

# Print commmands instead of execute
Debug = False

# Open directory after processing
Open_Directory = True

# Python name on Unix operating systems
Python_Name = "python3"

#-=-=-=-=-=-#

Icon = path.abspath("../Documents/Pictures/Icons/Icon.png")

root = Tk()
root.withdraw()
try:
	root.call("wm", "iconphoto", root._w, PhotoImage(file = Icon))
except TclError:
	pass

#-=-=-=-=-=-#
# Functions

def Get_Path(FilePath: str) -> str:
	"""Absolute path getter with additional user and variables expansion."""
	return str(Path(path.abspath(path.expanduser(path.expandvars(FilePath)))).resolve())

def Error(Traceback: str, Class: Exception = Exception) -> Exception:
	__args = Class.__name__, Traceback
	print("{0}: {1}".format(*__args))
	if name == "nt":
		MsgBox.showerror(*__args)
	raise SystemExit

def __Title(Title: str):
	if name == "nt":
		system("title {0} ^| {1}".format(__name__, Title))

__Title("Waiting for directory...")

#-=-=-=-=-=-#
# Tkinter prompt

print("Waiting for directory...", end = "\r")
if not Folder:
	Folder = fd.askdirectory(
		title = "Select directory with audio files and cover art",
		initialdir = path.expanduser("~/Music")
	)
	if not Folder:
		Error("Folder selection aborted.")

#-=-=-=-=-=-#
# Variables

YTMVG = Get_Path(YTMVG)
Folder = Get_Path(Folder)

chdir(Folder)
print(f'Current working directory is "{getcwd()}"\n')
Output = path.abspath("_".join([
	"YTMVG",
	path.basename(Folder),
	str(time()).split(".")[-1].zfill(7)
	])
)

Counter = 1
Arguments = [Argument.strip("-") for Argument in Arguments]
Arguments += ["no-thumbnail"]
Function = print if Debug else system
if name == "nt":
	Python_Name = sys.executable

Files = []
Audio_Files = []
Picture = ""

print("Checking files...")
if path.exists(Folder):
	for File in Path(Folder).glob("*"):
		Files += [str(File.resolve())]
else:
	Error(f'Directory doesn\'t exists! ("{Folder}")', OSError)

#-=-=-=-=-=-#
# Add audio files

print("Adding audio files...")
for Format in Formats["Audio"]:
	for File in Files:
		if File.lower().endswith(Format.lower()):
			try:
				print('\tVerifying "{File}"...', end = "\r")
				_ = mFile(File).info.length
			except AttributeError:
				Error('File is broken. ("{0}")'.format(File.split(sep)[-1]))
			Audio_Files += [File]

Audio_Files = set(Audio_Files)
if Audio_Files:
	print("\tDone, {0} file{1} found".format(
		len(Audio_Files),
		"s" if len(Audio_Files) > 1 else ""
		)
	)
else:
	Error("Directory doesn't contain audio files!")

#-=-=-=-=-=-#
# Get picture

print("Specifying picture...")
for Format in Formats["Image"]:
	for File in Files:
		if File.lower().endswith(Format.lower()):
			try:
				print("\tVerifying...", end = "\r")
				Image.open(File)
			except OSError as err:
				Error('File is broken. ("{0}")'.format(File.split(sep)[-1]), err.__class__.__name__)
			Picture = File
			break

if Picture:
	print(f'\t"{Picture}"')
else:
	Error("Directory doesn't contain image file!", FileNotFoundError)

print("\n{0}".format("-=" * 16 + "-"))

#-=-=-=-=-=-#
# Processing

for File in Audio_Files:
	if not Debug:
		__Message = f"Processing files... [{Counter}/{len(Audio_Files)}]"
		print("\n" + __Message)
		Counter += 1
		if Counter == len(Audio_Files):
			Arguments.remove("no-thumbnail")
		__Title(__Message)
	Function(r'{0} "{1}" -a "{2}" -i "{3}" -d "{4}"{5} -v 0 -nod'.format(
		Python_Name, YTMVG,
		File, Picture, Output,
		(" --" if Arguments else "") + " --".join(Arguments)
	)
)

#-=-=-=-=-=-#
# Moving files

if not Debug:
	print("\n{0}".format("-=" * 16 + "-"))
	print("\nMoving videos...")
	for File in Path(Output).rglob("*.mp4"):
		File = str(File.resolve())
		FileName = File.split(sep)[-1]
		rename(File, path.join(Output, FileName))

	print("Moving thumbnail...")
	for File in Path(Output).rglob("*.jpg"):
		File = str(File.resolve())
		FileName = File.split(sep)[-1]
		try:
			rename(File, path.join(Output, FileName))
		except OSError:
			pass

	print("Removing folders...")
	for Folder in next(walk(Output))[1]:
		Folder = path.join(Output, Folder)
		print("\t" + Folder)
		rmtree(Folder)

#-=-=-=-=-=-#
# Ending

if not Debug:
	for x in range(2):
		sleep(.25)
		print("\a", end = "\r")

	if name == "nt":
		Command = r"start /max C:\Windows\explorer.exe"
	elif os.sys.platform.startswith("lin"):
		distro = distro_name
		if distro == "ubuntu":
			Command = "nautilus"
		elif distro == "debian":
			Command = "nemo"
		elif distro == "rhel":
			Command = "gnome-open"
		else:
			Command = "xdg-open"
	else:
		Command = "open"
	Command += ' "{0}"'.format(Output)
	if Open_Directory:
		system(Command)

	if name == "nt":
		if len(sys.argv) > 2:
			print()
			system("pause")