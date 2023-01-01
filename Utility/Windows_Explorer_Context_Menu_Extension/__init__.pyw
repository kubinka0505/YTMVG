__doc__ = """Registry Setter

Script that allows batch values setting into the
Windows Registry editor with administrator privileges.

Can be used as standalone `Registry_Set` function
(with modules) or as an ArgumentParser one.
"""

import os, sys

# Because I obviously can't have an icon in normal terms...
os.chdir("..")
exec(open("__init__.pyw", encoding = "U8").read())
os.chdir(path.basename(path.dirname(__file__)))

#-=-=-=-=-=-=-=-=-=-=-#

__name__	= open(__file__).readlines()[0].strip('"').strip("\n")
__author__	= "kubinka0505"
__credits__	= __author__
__version__	= "1.0"
__date__	= "12.05.2023" 

#-=-=-=-=-=-=-=-=-=-=-#

# Non-NT OS handling
if name == "nt":
	import pyuac
	import ctypes
	import winreg
else:
	MsgBox.showerror("Error", "Windows Only!")
	raise SystemExit()

#-=-=-=-=-=-=-=-=-=-=-#

# Main Class
class Registry:
	Values = {
		"Hives": {
			"HKCR": "HKEY_CLASSES_ROOT",
			"HKCU": "HKEY_CURRENT_USER",
			"HKLM": "HKEY_LOCAL_MACHINE",
			"HKU": "HKEY_USERS",
			"HKCC": "HKEY_CURRENT_CONFIG"
		},
		"Types": [
			"SZ", "Multi SZ", "Expand SZ",
			"Binary", "D-Word", "Q-Word",
		]
	}

	#-=-=-=-#

	def __init__(self, Path: str):
		Main_Key = Path.replace("/", sep).strip(sep) + sep
		Main_Key = Main_Key.split(sep)
		for Short, Extended in self.__class__.Values["Hives"].items():
			Main_Key[0] = Main_Key[0].upper().replace(Short, Extended)

		self.Key = path.join(*Main_Key)
		self.RegKey = getattr(winreg, Main_Key[0]), path.join(*Main_Key[1:])


	def set(self, Name: str = None, Value: str = None, Type: str = "SZ") -> tuple:
		"""Set the value."""
		__DefaultType = "SZ"
		if not Type:
			Type = __DefaultType

		for Value_Types in self.__class__.Values["Types"]:
			Type = Type.replace("-", "")
			Type = Type.upper().strip().replace(" ", "_").lstrip("REG_")

			Value_Types = Value_Types.replace("-", "")
			Value_Types = Value_Types.upper().replace(" ", "_")

			if Type == Value_Types:
				DisplayType = "REG_" + Type
				Type = getattr(winreg, DisplayType)
				break

		if not isinstance(Type, int):
			Type = __DefaultType

		#-=-=-=-#

		winreg.CreateKey(*self.RegKey)
		with winreg.OpenKey(*self.RegKey, 0, winreg.KEY_ALL_ACCESS) as Registry_Key:
			winreg.SetValueEx(Registry_Key, Name, 0, Type, Value)

		return self.Key, Name, Value, DisplayType

	#-=-=-=-#

	def relcd(self, Target: str):
		"""Changes directory to relative."""
		Target = path.join(path.abspath(self.Key), Target)
		Target = path.abspath(Target)

		self.Key = Target.split(getcwd())[1][1:].replace("/", sep)
		self.RegKey = getattr(winreg, self.Key.split(sep)[0]), path.join(*self.Key.split(sep)[1:])

	def cwd(self):
		"""Gets current key path."""
		return self.Key

	def dir(self):
		"""Gets current key name."""
		return path.dirname(self.Key)

	def hive(self):
		"""Gets current key hive."""
		return self.Key.split(sep)[0]

	def name(self):
		"""Gets current key name."""
		return path.basename(self.Key)

	getcwd = cwd
	dirname = dir
	basename = name
	anchor = hive