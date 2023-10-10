Config = load(open("Data/Config.json", encoding = "U8"))

#-=-=-=-#

session = Session()
session.headers.update(
	{
		"User-Agent":
		"Mozilla/5.0 (Windows NT 10.0; Win32; x32) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
	}
)
get = session.get

#-=-=-=-#

RGB = lambda col: tuple([round(Value * 255) // 1 for Value in ColorHandler(col).rgb])

class Styles:
	"""Colored Prints."""
	OK = "#0C0"
	Info = "#4AF"
	Flaw = "#F25"
	Error = "#C10"
	Warning = "#FC0"
	Meta_Info = "#888"
	Meta_Info_2 = "#93F"

for Variable_Name in list(vars(Styles))[2:-2]:
	Variable = getattr(Styles, Variable_Name)
	__clr = fg(*RGB(Variable))

	if Variable_Name.lower().startswith(("flaw", "err", "warn")):
		__clr = ef.b + __clr

	exec('{0}.{1} = "{2}"'.format(Styles.__name__, Variable_Name, __clr))

Styles.Reset = fg.rs + ef.rs

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
	if os.sys.platform == "win32":
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
	raise SystemExit("{1}{0}{2}\a".format(
		Traceback,
		Styles.Error, Styles.Reset
		) + " " * 32
	)

def ArgParseBool(Boolean: bool) -> str:
	"""Converts default bool type to argument parser one."""
	return "store_" + str(bool(Boolean)).lower()

def Random_String(Length: int = 16) -> str:
	"""Random string generation."""
	return "".join(choice(printable[0:62]) for String in range(Length))

def __FixTitle(String: str) -> str.title:
	return " ".join([Element[0].upper() + Element[1:] for Element in String.split()])

#-=-=-=-#

__Repo = "/".join((__author__, __name__))
__BreakString = Styles.Reset + "\n" + "─" * 32 + "\n"

__ALLOWED_FORMATS = "MP3", "FLAC", "OGG"
__RAND_STR = Random_String(8)
__FILES_TO_REMOVE = []