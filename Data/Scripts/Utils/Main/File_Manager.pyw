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

			def Path(Path: os.path.abspath) -> str:
				"""Absolute path getter with additional user and variables expansion."""
				if Path.lower().startswith(("http:", "ftp:")):
					Error("Program does not accept URLs!")
				else:
					Path = str(path(
						os.path.abspath(
							os.path.expanduser(
								os.path.expandvars(
									Path
								)
							)
						)
					).resolve()
				)
				return Path

	#-=-=-=-#

	class Upload:
		"""File uploading manager."""

		def Media(Path: os.path.abspath, Method: type, Type: str) -> str:
			"""Media uploader handler."""
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
				raise Error(Traceback + '! ("' + Path + '")')
			
			#-=-=-=-#

			if os.name == "nt":
				Path = os.path.join(
					os.sep.join(Path.split(os.sep)[:-1]),
					Path.split(os.sep)[-1][0].upper() + \
					Path.split(os.sep)[-1][1:]
				)
			return Path