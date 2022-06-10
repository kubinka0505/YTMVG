"""YouTube Music Video Generator

Pack of scripts providing customizable
YouTube Music Videos generation."""
__START = __import__("time").time()
import os

try:
	from sty import *
	from colour import Color as color
	from mutagen import File as mFile
	from PIL import Image, ImageFile
	from PIL.ImageOps import contain
	from PIL.ImageColor import getrgb as RGB
	from PIL.ImageEnhance import *
	if not os.sys.platform.startswith("win"):
		from distro import id
except ImportError:
	exit("Did you installed the requirements?\a")

from time import *
from json import load
from io import BytesIO
from argparse import *
from shutil import move
from textwrap import dedent
from pathlib import Path as path
from datetime import timedelta as td

#-=-=-=-#

__name__	= "".join(filter(
	lambda Line: Line.isupper(),
	open(__file__).readlines()[0].rstrip("\n").strip('"')
	)
)
__author__	= "kubinka0505"
__credits__	= __author__
__version__	= "1.0"
__date__	= "05.05.2022"

__BaseDir = os.path.abspath(os.path.dirname(__file__))
os.chdir(__BaseDir)

#-=-=-=-#

open_ = lambda _open: open(os.path.join(__BaseDir, "Scripts", _open + ".pyw"), encoding = "U8").read()

exec(open_("Utils/Main/Main"))
exec(open_("ArgParse/Main"))
exec(open_("ArgParse/Settings"))
exec(open_("Utils/Packages_Location"))
exec(open_("Utils/Directory/Make"))

try:
	#if not any((args.no_thumbnail, args.no_video)):
	#	print(Styles.Reset + "\n\r" + "─c" * 33 + "\n")
	#-=-=-=-#
	if not args.no_thumbnail:
		exec(open_("Process/Thumbnail"))
	else:
		Thumbnail_Path = None
	#-=-=-=-#
	if not args.no_video:
		try:
			exec(open_("Process/Video"))
		except KeyboardInterrupt:
			pass

except KeyboardInterrupt:
	FM.Utils.Cleanup_Directory(Directory, ["MD"])
	#-=-=-=-#
	print(Styles.Reset + "\n\r" + "─" * 33 + "\n")
	Error("YTMVG was interrupted by the user, exiting")

#-=-=-=-#

if os.path.basename(Directory) in os.listdir():
	FM.Utils.Cleanup_Directory(Directory, ["MD"])

#-=-=-=-#

if args.directory != Directory:
	move(Final_Directory, args.directory)
	Final_Directory = os.path.join(args.directory, Audio_Name[1])

if not args.no_open_directory:
	exec(open_("Utils/Directory/Open"))

# Print information
Lines = {
	"Video":		Video_Paths[-1],
	"Thumbnail":	str(Thumbnail_Path),
	"Directory":	Final_Directory,
	"\nRuntime":	Styles.Warning + str(td(seconds = time() - __START))[:-3]
}

if args.no_video:
	del Lines["Video"]

if args.no_thumbnail:
	del Lines["Thumbnail"]

if not args.no_information:
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