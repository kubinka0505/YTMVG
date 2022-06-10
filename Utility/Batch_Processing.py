"""YTMVG Batch Processing."""
import os
from os.path import *
from time import sleep
from pathlib import Path as Path_
os.chdir(os.path.abspath(os.path.dirname(__file__)))

__doc__		= open(__file__).readlines()[0].strip("\n").strip('"').strip(".")
__author__	= "kubinka0505"
__credits__	= __author__
__version__	= "1.0"
__date__	= "01.05.2022"

#-=-=-=-=-=-#

# Directory with audio files
Folder = "~/Music/Album"

# Image file location
Picture = "~/Music/Album/Cover.png"

# YTMVG Location
YTMVG = "../YTMVG.py"

#-=-=-=-#

# Allowed audio file formats
Formats = "MP3", "OGG", "FLAC", "WAV"

# Additional processing arguments
Arguments = ["-q", "-nt"]

# Process files in subdirectories
Recursive = False

# Print commands instead of processing
Debug = False

# Python name on non-windows operating systems
Python_Name = "python3"

#-=-=-=-=-=-#

def Get_Path(Path: str) -> str:
	"""Absolute path getter with additional user and variables expansion."""
	return abspath(expanduser(expandvars(str(Path_(Path).resolve()))))

def Shorten_Path(Path: str) -> str:
	"""Splits path from "~"."""
	return Path.replace(expanduser("~"), "~").replace(os.sep, "/")

#-=-=-=-=-=-#

Folder = Get_Path(Folder)
Picture = Get_Path(Picture)
YTMVG = Get_Path(YTMVG)

Formats = tuple(map(str.lower, Formats))
Arguments = list(Arguments)
Recursive = ("**/" if Recursive else "") + "*"
Function = print if Debug else os.system

os.sys.platform = os.sys.platform.lower()

#-=-=-=-=-=-#

open(Picture).close()
os.chdir(Folder)
open(YTMVG).close()

Folder = Shorten_Path(Folder)
Picture = Shorten_Path(Picture)

#-=-=-=-=-=-#

Counter = 1
Thumbnail_Processed = 0
Files = []

for File in Path_(".").glob(Recursive):
	File = str(File.resolve())
	if File.lower().endswith((Formats)):
		Files += [File]

for Audio in Files:
	if os.sys.platform.startswith("win"):
		os.system("title " + " ^| ".join(
				(
				__doc__,
				"[{0}/{1}]".format(Counter, len(Files)),
				Audio
				)
			)
		)
	Function('{0} "{1}" -i "{2}" -a "{3}"'.format(
			os.sys.executable if os.sys.platform.startswith("win") else Python_Name,
			YTMVG, Picture, Shorten_Path(Audio)
		).strip() + " " + " ".join(Arguments)
	)

	if Thumbnail_Processed > 0:
		Arguments += ["-nt"]

	Counter += 1
	Thumbnail_Processed = 1

#-=-=-=-#

if not Debug:
	for x in range(2):
		sleep(1)
		print("\a", end = "\r")

if all(
	(
		os.sys.platform.startswith("win"),
		"-q" in Arguments
	)):
	os.system("pause")
