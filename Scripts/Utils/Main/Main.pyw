Config = load(open("Config.json", encoding = "U8"))

#-=-=-=-#

Initial_Directory = Config["Settings"]["Directory"]["Initial"]

__INI_DIR_AUD = "Music"

if os.sys.platform.startswith("win"):
	__INI_DIR_IMG = "Pictures"
else:
	__INI_DIR_IMG = "Downloads"

__INI_DIR_AUD = "~/" + __INI_DIR_IMG
__INI_DIR_IMG = "~/" + __INI_DIR_AUD

if Initial_Directory["Audio"]:
	__INI_DIR_AUD = Initial_Directory["Audio"]

if Initial_Directory["Image"]:
	__INI_DIR_IMG = Initial_Directory["Image"]

Initial_Directory["Audio"] = __INI_DIR_AUD
Initial_Directory["Image"] = __INI_DIR_IMG

#-=-=-=-=-=#

class Styles:
	"""Colored Prints."""
	OK = "#0C0"
	Info = "#4AF"
	Flaw = "#F25"
	Error = "#C10"
	Warning = "#FC0"
	Meta_Info = "#999"
	Meta_Info_2 = "#93F"

Class = Styles
for Variable in list(vars(Class))[2:-2]:
	exec('{0}.{1} = "{2}"'.format(
		Class.__name__, Variable,
		fg(*RGB(getattr(Class, Variable)))
		)
	)

Styles.Reset = fg.rs

Image.MAX_IMAGE_PIXELS = float("inf")
ImageFile.LOAD_TRUNCATED_IMAGES = 1

os.system("")
os.sys.platform = os.sys.platform.lower()
stdout_ = os.sys.stdout

#-=-=-=-#

exec(open_("Utils/Main/FileManager"))

def Generate_Thumbnail(Input: os.path.abspath, Output: os.path.abspath, Luminance: float):
	"""Creates YouTube Music Video Thumbnail."""
	def __GTL(Log: str, Info: str = 0, Tabs: int = 2):
		if Info:
			Log += "\t" * Tabs + str(Info)
		return print(Log)

	#-=-=-=-#

	Picture = Image.open(Input)
	Picture_RGB = Picture.convert("RGB")
	__GTL("Opened image", Input, 3)

	#-=-=-=-#

	# Calculate dimensions
	Dimensions = Image.new("RGB", (16, 9), "red")
	Dimensions = contain(Dimensions, (float("inf"), max(Picture.size)))
	Size = Dimensions.size

	__GTL("Calculated dimensions", "x".join(map(str, Size)))

	#-=-=-=-#

	# Get Clusters
	Colors = Get_Clusters(Picture_RGB)
	if args.cluster == 1: args.cluster = (len(Colors) - 1) // 2
	if args.cluster == 2: args.cluster = -1 

	BgCol = Colors[args.cluster]
	BgCol = Image.new("RGB", (1, 1), tuple(BgCol))

	BgColCover = contain(Picture_RGB, (3, 3)).getpixel((2, 2))

	#-=-=-=-#

	# Apply Brightness
	BgCol = Brightness(BgCol).enhance(Luminance)
	__GTL("Applied brightness", " | ".join(
			(
			str(Luminance) + "x",
			str(Luminance * 100) + "%"
			)
		)
	)

	#-=-=-=-#

	# Specify color
	BgCol = BgCol.getpixel((0, 0))
	__BgCol = []
	__BgCol += [
		color("#" + "".join("{:02X}".format(RGB) for RGB in BgCol)),
		color("#" + "".join("{:02X}".format(RGB) for RGB in BgColCover[:3]))
	]
	__BgCol = [Color.hex_l.upper() for Color in __BgCol]

	__GTL("Specified the color", __BgCol[0])

	#-=-=-=-#

	# Generate Background
	Background = Image.new("RGB", Size, BgCol)
	__GTL(
		"Generated background",
		fg(*RGB(__BgCol[0])) + "■" * 3 + Styles.Flaw
	)
	
	# Paste original picture
	Background.paste(
		Picture, (
			(Background.size[0] - Picture.size[0]) // 2,
			(Background.size[1] - Picture.size[1]) // 2
		), Picture.convert("RGBA")
	)
	__GTL(
		"Pasted original picture",
		"".join(
			(
				fg(*RGB(__BgCol[0])) + "■",
				fg(*RGB(__BgCol[1])) + "■",
				fg(*RGB(__BgCol[0])) + "■" + Styles.Flaw
			)
		)
	)

	#-=-=-=-#

	Background.convert("RGB").save(Output, quality = 100)
	return __GTL("Saved image", Output, 3)

def Get_Clusters(Picture: Image) -> tuple:
	"""Gets color clusters based on the palettized image."""
	Palettized = Picture.quantize(colors = args.palette_size, kmeans = 3).convert("RGB")
	Colors = []
	for Color in sorted(Palettized.getcolors(), reverse = 1):
		Color = Color[1]
		if all((
			Color != (0,) * 3,
			Color != (255,) * 3
			)):
			Colors += [Color]
	return Colors[1:-1]

def Variable_Search(Query: str.lower, Extension: str.lower = "EXE", Variable: os.environ = "PATH") -> str:
	"""Searches for `Content` in `Variable` environment variable."""
	if os.sys.platform.startswith("win"):
		for Key in os.environ[Variable].split(os.pathsep):
			Key = Key.lower()
			Query = Query.lower()
			Extension = Extension.lower()
			#-=-=-=-#
			if Query + "." + Extension in Key:
				Value = Key
	else:
		Value = Query.lower()
	#-=-=-=#
	return Value

def Percentage(Part: float, Whole: float) -> str:
	"""Returns `Part` of `Whole`."""
	RetVal = "0.00"
	if Part != Whole:
		RetVal = round((100 - (Part / Whole) * 100), 2)
	return str(RetVal)

def Clamp(Number: float, Minimum: float, Maximum: float) -> float:
	"""Limits `Number` in range (`Minimum`, `Maximum`)."""
	return max(min(Maximum, Number), Minimum)

def Error(Traceback: str) -> SystemExit:
	"""Custom `SystemExit` handler."""
	raise SystemExit(Styles.Error + Traceback + Styles.Reset + "\a")

def ArgParseBool(Boolean: bool) -> str:
	"""Converts default bool type to argument parser one."""
	return "store_" + str(not bool(Boolean)).lower()