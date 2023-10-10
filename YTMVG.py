"""YouTube Music Video Generator

Pack of scripts providing customizable
YouTube Music Videos generation."""
__START = __import__("time").perf_counter()

try:
	import os
	import logging
	from math import sqrt
	from json import load
	from io import BytesIO
	from argparse import *
	from random import choice
	from string import printable
	from pathlib import Path as path
	from time import sleep, perf_counter as time
	from requests import Session, utils, exceptions
	from datetime import datetime as dt, timedelta as td
	from tkinter import Tk, PhotoImage, filedialog as fd, TclError

	if os.sys.platform == "win32":
		import ctypes

	try:
		# Commented lines has been moved to
		# "Data/Scripts/Process/Thumbnail/Colors.pyw"
		# script in order to optimize the program.
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

		if os.sys.platform != "win32":
			from distro import id as distro_name

	except ImportError as Error:
		exit(f"{Error.__class__.__name__} - {Error}.\a")
except (EOFError, KeyboardInterrupt):
	raise SystemExit()

#-=-=-=-#

__name__		= "".join((c for c in open(__file__).readlines()[0].strip('"').rstrip("\n") if c.isupper()))
__author__	= "kubinka0505"
__credits__	= __author__
__version__	= "1.2"
__date__		= "10.10.2023"

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
	if os.sys.platform == "win32":
		os.system(f"title {__name__} ^| {FileName}")
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
__V = not [x for x in __V if x in " ".join(os.sys.argv).lower()]
__H = any(("-h" in " ".join(os.sys.argv).lower(), len(os.sys.argv) < 2))

try:
	__START_LOAD = time()
	for File in __FileList:
		if __V:
			if not __H:
				print('{1}<SETUP>{3} Loading {2}"{0}"{3} script...'.format(
					File,
					Styles.Info, Styles.Meta_Info, Styles.Reset
					) + " " * 32, end = "\r"
				)
		exec(open_(File))
except (EOFError, KeyboardInterrupt):
	raise SystemExit()

# Updater
try:
	exec(open_("Utils/Main/Internet"))
except FileNotFoundError:
	pass

try:
	# Begin
	print('{2}<INFO>{3} Beggining processing the {1}"{0}"{3} file...'.format(
		os.path.basename(args.audio),
		Styles.OK, Styles.Info, Styles.Reset
		) + " " * 32
	)

	print(__BreakString)

	#-=-=-=-#

	# Thumbnail
	if args.no_thumbnail:
		Thumbnail_Path = None
	else:
		exec(open_("Process/Thumbnail/Setup"))
		print(__BreakString)

	# Description
	if not args.no_description:
		exec(open_("Process/Description/Setup"))

	# Video & Thumbnail
	if not any((args.no_video, args.no_thumbnail)):
		print(__BreakString)

	# Video
	if not args.no_video:
		try:
			exec(open_("Process/Video"))
		except KeyboardInterrupt:
			FM.Utils.Cleanup_Directory(Directory, ["MD"])
			os.rename(Video_Names[0], Video_Names[1])
except KeyboardInterrupt:
	FM.Utils.Cleanup_Directory(Directory, ["MD"])
	#-=-=-=-#
	print(__BreakString)
	Error("YTMVG was interrupted by the user, exiting.")

#-=-=-=-#

# Cleanup
if os.path.basename(Directory) in os.listdir():
	FM.Utils.Cleanup_Directory(Directory, ["MD"])

# Remove temporary files 
for File in __FILES_TO_REMOVE:
	os.remove(File)

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
print(__BreakString)

Lines = {
	"Video path": Video_Names[-1],
	"Thumbnail path": str(Thumbnail_Path),
	"Directory path": Final_Directory,

	"Runtime": Styles.Warning + str(td(seconds = time() - __START))[:-3]
}

if args.no_video:
	del Lines["Video path"]

if args.no_thumbnail:
	del Lines["Thumbnail path"]

for Type, Line in Lines.items():
	Type = "{1}<INFO>{2} {0}".format(Type, Styles.Info, Styles.Reset)
	Line = "{2}{0}{1}{3}".format(
		Line,
		"" if list(Lines.values())[-1] == Line else "\n",
		Styles.Meta_Info, Styles.Reset
	)
	for Element in (Type, Line):
		print(Element)

#-=-=-=-#

os.sys.stdout = stdout_

__BeepTime = 2, 1 / 7
for x in range(__BeepTime[0]):
	print(BEL, end = "\r")
	sleep(__BeepTime[1])