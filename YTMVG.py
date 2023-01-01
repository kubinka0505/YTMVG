"""YouTube Music Video Generator

Pack of scripts providing customizable
YouTube Music Videos generation."""
__START = __import__("time").time()

try:
	import os
	from time import *
	from math import sqrt
	from json import load
	from io import BytesIO
	from argparse import *
	from random import choice
	from string import printable
	from pathlib import Path as path
	from datetime import datetime as dt, timedelta as td
	from tkinter import Tk, PhotoImage, filedialog as fd, TclError

	try:
		# Commented lines moved to "Data/Scripts/Process/Thumbnail/Colors.pyw"
		import cv2
		from sty import *
		import numpy as np
		#from sklearn import metrics
		from PIL.ImageEnhance import *
		from colorsys import rgb_to_hsv
		from PIL import Image, ImageFile
		from PIL.ImageOps import contain
		from mutagen import File as mFile
		#from sklearn.cluster import KMeans
		from colour import Color as ColorHandler

		if os.name != "nt":
			from distro import id as distro_name

	except ImportError as Error:
		exit(f"{Error} - have you installed the requirements?\a")
except (EOFError, KeyboardInterrupt):
	raise SystemExit()

#-=-=-=-#

__name__	= "".join(filter(
	lambda Line: Line.isupper(),
	open(__file__).readlines()[0].rstrip("\n").strip('"')
	)
)
__author__	= "kubinka0505"
__credits__	= __author__
__version__	= "1.1"
__date__		= "01.01.2023"

__BaseDir = os.path.abspath(os.path.dirname(__file__))
os.chdir(__BaseDir)

#-=-=-=-#

def open_(File: os.path.abspath, Title: bool = True) -> open:
	"""File opening handler."""
	File = os.path.join(__BaseDir, "Data/Scripts", File + ".pyw")
	#---#
	FileName = File.replace(__BaseDir, "")
	FileName = FileName.replace("_", " ")
	FileName = FileName.replace(os.sep, "/")[1:]
	#---#
	if os.name == "nt":
		os.system(f"title YTMVG ^| {FileName}")
	return open(File, encoding = "U8").read()

exec(open_("Utils/Main/Main"))

__FileList = [
	"Utils/Main/File_Manager",
	"Utils/Main/Tkinter",
	"ArgParse/Main",
	"ArgParse/Settings",
	"Utils/Directory/Make",
	"Utils/Main/Tkinter",
	"Utils/Packages_Location"
]

# Verbosity
__V = "-v -1", "-v=-1", "-v 0", "-v=0"
__V = not [x for x in __V if x in " ".join(os.sys.argv)]

__InfoString = " | ".join(("{2}<SETUP>{3}", "{2}{1}{3}", 'Loading "Data/{0}"...'))
__InfoString += " " * 8
try:
	__START_LOAD = time()
	for File in __FileList:
		LoadTime_File = str(td(seconds = time() - __START_LOAD))[2:-3]
		if __V:
			print(__InfoString.format(
				File, LoadTime_File,
				Styles.Info, Styles.Reset), end = "\r"
			)
		exec(open_(File))
except (EOFError, KeyboardInterrupt):
	raise SystemExit()
__InfoString = __InfoString.replace("{", "}").replace("}", "")

try:
	# Description
	if not args.no_description:
		exec(open_("Process/Description/Setup"))
	print()

	# Thumbnail
	print(Styles.Reset + "\n" + "─" * 32 + "\n")
	if args.no_thumbnail:
		Thumbnail_Path = None
	else:
		exec(open_("Process/Thumbnail/Main"))

	# Video & Thumbnail
	if not any((args.no_video, args.no_thumbnail)):
		print(Styles.Reset + "\n" + "─" * 32 + "\n")

	# Video
	if not args.no_video:
		try:
			exec(open_("Process/Video"))
		except KeyboardInterrupt:
			os.rename(Video_Names[0], Video_Names[1])
except KeyboardInterrupt:
	FM.Utils.Cleanup_Directory(Directory, ["MD"])
	#-=-=-=-#
	print(Styles.Reset + "\n" + "─" * 32 + "\n")
	Error("YTMVG was interrupted by the user, exiting.")

#-=-=-=-#

if os.path.basename(Directory) in os.listdir():
	FM.Utils.Cleanup_Directory(Directory, ["MD"])

#-=-=-=-#

if args.directory != Directory:
	import shutil
	try:
		os.makedirs(args.directory)
	except OSError:
		pass
	shutil.move(Final_Directory, args.directory)
	Final_Directory = os.path.join(args.directory, Audio_Names[1])

if not args.no_open_directory:
	exec(open_("Utils/Directory/Open"))

# Print information
print(Styles.Reset + "\n" + "─" * 32 + "\n")

Lines = {
	"Video":		Video_Names[-1],
	"Thumbnail":	str(Thumbnail_Path),
	"Directory":	Final_Directory,
	"\nRuntime":	Styles.Warning + str(td(seconds = time() - __START))[:-3]
}

if args.no_video:
	del Lines["Video"]

if args.no_thumbnail:
	del Lines["Thumbnail"]

for Type, Line in Lines.items():
	Type = Styles.Info + Type
	Line = "\t" + Styles.Meta_Info + Line + Styles.Reset
	for Element in (Type, Line):
		print(Element)
		sleep(1 / 80)

#-=-=-=-#

os.sys.stdout = stdout_

for x in range(2):
	print(BEL, end = "\r")
	sleep(1 / 7)