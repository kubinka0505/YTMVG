class FM:
	"""Various functions for files managing."""

	class Utils:
		"""Utility functions."""

		def Cleanup_Directory(Directory: os.path.abspath, Ignore_Formats: tuple):
			"""Clears non-directory files and removes empty folders."""
			Formats = tuple(("." + Format.lower() for Format in tuple(Ignore_Formats)))
			try:
				for File in os.listdir(Directory):
					File = os.path.join(Directory, File)
					#-=-=-=-#
					if not File.lower().endswith(Formats):
						if os.path.isfile(File):
							os.remove(File)
						else:
							if not os.listdir(File):
								os.rmdir(File)
			except PermissionError:
				pass

			return

		#-=-=-=-#

		class Get:
			"""Grabbing Values from files."""

			def Size(Bytes: int) -> str:
				"""Returns human-readable file size."""
				for Unit in ("", "K", "M", "G", "T"):
					if Bytes < 1024:
						break
					Bytes /= 1024

				return str(round(Bytes, 2)) + " " + Unit + "B"

			def File(Path: os.path.abspath, Verbose: bool = False) -> str:
				"""File download handler."""
				if Path.lower().startswith(("http://", "https://", "ftp://")):
					Path = Path.split("//")
					Path[1] = utils.quote(Path[1]).strip("/")
					Path  = "//".join(Path)
					try:
						# Normalize URL
						File_Name = utils.unquote(Path.split("/")[-1])
						for Delimiter in (("?", "&", "#")):
							File_Name = File_Name.split(Delimiter)[0]
						File_Location = os.path.join(_TMP_DIR, File_Name)

						# Download
						with get(Path, stream = 1) as Site:
							if Site.ok:
								if Site.headers["content-type"].split()[0].split(";")[0].split("/")[0].lower() == "audio":
									with open(File_Location, "wb") as File:
										if Verbose:
											print("{2}<INFO>{3} Downloading {0}...{1}".format(
												File_Name, " " * 32,
												Styles.Info, Styles.Reset
												)
											)
										for Chunk in Site.iter_content(chunk_size = 1024): 
											if Chunk:
												File.write(Chunk)
												
									return File_Location, 1
								else:
									Error("Provided URL is not an audio file.")
							else:
								Error("Failed to fetch the URL due to {0} status code. ({1})".format(
									Site.status_code, Site.reason.title()
									)
								)
					except exceptions.ConnectionError:
						Error("Could not fetch the URL due to internet connection problems.")
					except exceptions.MissingSchema:
						Error("Failed to analyze the URL - please check for potential misspelling and try again!")

				return Path, 0

			def Path(Path: os.path.abspath) -> str:
				"""Absolute path getter with additional user and variables expansion."""
				Path = os.path.expandvars(Path)		# Windows
				Path = os.path.expanduser(Path)		# Linux
				Path = os.path.abspath(Path)			# Full
				Path = str(path(Path).resolve())		# Normalize

				return Path

			def hideFile(Path: os.path.abspath) -> str:
				"""Hides a file or a directory."""
				if os.sys.platform == "win32":
					return ctypes.windll.kernel32.SetFileAttributesW(File, 2)

	#-=-=-=-#

	class Upload:
		"""File uploading manager."""

		def Media(Path: os.path.abspath, Method: type, Type: str) -> str:
			"""Media uploader and verification handler."""
			if os.path.exists(Path):
				if os.path.isfile(Path):
					try:
						Method(Path)
						Traceback = ""
					except Exception:
						Traceback = f"Not an {Type} file"
				else:
					Traceback = "Not a file"
			else:
				Traceback = "File doesn't exist"
			
			if Traceback:
				raise Error('{0}! ("{1}")'.format(Traceback, Path))

			return Path

#-=-=-=-#

# Temp File directory
_TMP_DIR =  "~/AppData/Local/Temp" if os.sys.platform == "win32" else "/tmp"
_TMP_DIR = FM.Utils.Get.Path(_TMP_DIR)

#-=-=-=-#
# Initial directories
Initial_Directory = Config["Settings"]["Directory"]["Initial"]

# Initial audio directory
if Initial_Directory["Audio"]:
	__INI_DIR_AUD = Initial_Directory["Audio"]
else:
	__INI_DIR_AUD = "~/Music"

# Initial image directory
if Initial_Directory["Image"]:
	__INI_DIR_IMG = Initial_Directory["Image"]
else:
	__INI_DIR_IMG = "~/" + ("Pictures" if os.sys.platform == "win32" else "Downloads")

Initial_Directory["Audio"] = FM.Utils.Get.Path(__INI_DIR_AUD)
Initial_Directory["Image"] = FM.Utils.Get.Path(__INI_DIR_IMG)