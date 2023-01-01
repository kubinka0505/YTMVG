Config = load(open("Data/Config.json", encoding = "U8"))

#-=-=-=-#

Initial_Directory = Config["Settings"]["Directory"]["Initial"]

__INI_DIR_AUD = "Music"

if os.name == "nt":
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

RGB = lambda col: tuple([round(Value * 255) // 1 for Value in ColorHandler(col).rgb])

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

def Variable_Search(Query: str.lower, Variable: os.environ = "PATH") -> str:
	"""Searches for `Content` in `Variable` environment variable."""
	Query = Query.lower()
	#-=-=-=-#
	if os.name == "nt":
		for Key in os.environ[Variable].split(os.pathsep):
			if f"{Query}.exe" in Key.lower():
				if os.path.exists(Key):
					if os.path.isfile(Key):
						Value = str(path(Key).resolve())
						break
					else:
						Value = ""
	else:
		try:
			import apt
			cache = apt.Cache() 
			if cache[Query].is_installed:
				Value = Query
			else:
				Value = ""
		except ImportError:
			Value = Query
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
	return min(max(Minimum, Number), Maximum)

def Error(Traceback: str) -> SystemExit:
	"""Custom `SystemExit` wrapper."""
	raise SystemExit(Styles.Error + Traceback + Styles.Reset + "\a" + " " * 32)

def ArgParseBool(Boolean: bool) -> str:
	"""Converts default bool type to argument parser one."""
	return "store_" + str(not bool(Boolean)).lower()

def Random_String(Length: int = 16) -> str:
	"""Random string creation used in saving files"""
	return "".join(choice(printable[0:62]) for String in range(Length))

def __FixTitle(String: str) -> str.title:
	return " ".join([Element[0].upper() + Element[1:] for Element in String.split()])

#-=-=-=-#

__RAND_STR = Random_String(8)