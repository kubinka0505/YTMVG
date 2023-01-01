Keys = []
Formats = ["MP3", "OGG", "FLAC"]

for Key in f"Shell/{Main_File_Name}", f"ContextMenus/{Main_File_Name}":
	Key = f"HKEY_CURRENT_USER/Software/Classes/*/{Key}"
	Key = Key.replace("/", sep)
	Keys += [Key]

__Formats_String = [Format.lower() for Format in (Formats + [Formats[0]])]
__Formats_String = " OR System.FileExtension:=.".join(__Formats_String)
__Formats_String = __Formats_String.lstrip(f"{Formats[0].lower()} OR")

#-=-=-=-=-=-#

Prompt = MsgBox.askyesnocancel(
	title = f"Add {Main_File_Name} to Explorer Context Menu",
	message = """
		Do you want to select preset?
		
		Warning: Selecting preset will override the
		settings associated with its certain options.

		See "ReadMe.md" for more information.
		"""[1:-1].replace("\t", ""),
	icon = "warning",
	default = "no"
)

Preset = ""
if Prompt:
	Presets = path.join(Main_File_Directory, "Data/Presets")
	if not path.exists(Presets):
		Presets = Main_File_Directory

	File = fd.askopenfilename(
		title = "Select preset file",
		initialdir = Presets,
		filetypes = [
			("Text files", "*.txt"), 
			("All files", "*.*")
		],
		defaultextension = "*.txt"
	)
	Preset = "-p " + ".".join(path.basename(File).split(".")[:-1])
elif Prompt == None:
	exit()

#-=-=-=-=-=-#

Shell_Key = Registry(Keys[0])
Shell_Key.set(None, Main_File_Name)
Shell_Key.set("AppliesTo", __Formats_String)
Shell_Key.set("ExtendedSubCommandsKey", path.join("*", Keys[1].split(f"{sep}*{sep}")[-1]))
Shell_Key.set("Icon", Icon_HQ)
Shell_Key.set("MultiSelectModel", "Document")

#-=-=-=-#

__CMD_KEY = "Commands/Make"
__CMD_VDTHB = "01_VideoAndThumbnail"
__CMD_VIDEO = "02_Video"
__CMD_THUMB = "03_Thumbnail"
__EXT_SUBKY = path.join(
	"*",
	Keys[1].split(f"{sep}*{sep}")[-1],
	__CMD_KEY.replace("/", sep)
)

Config = {
	"Shell": {
		"01_Make_VideoAndThumbnail_01": ["Make Video and Thumbnail", "WMPLoc.dll,-1050", path.join(__EXT_SUBKY, __CMD_VDTHB)],
		"02_Make_Video_02": ["Make Video", "WMPLoc.dll,-503", path.join(__EXT_SUBKY, __CMD_VIDEO)],
		"03_Make_Thumbnail_03": ["Make Thumbnail", "WMPhoto.dll,-400", path.join(__EXT_SUBKY, __CMD_THUMB)],
		"04_SEP_01": [],
		# Shell32.dll,-22
		# ImageRes.dll,-5334
		"05_Open_MainDirectory_01": ["Open YTMVG Main Directory", "Explorer.exe", "", fr'explorer.exe "{Main_File_Directory}"'],
		# ImageRes.dll,-1005
		"06_Open_VideoDirectory_01": ["Open YTMVG Videos Directory", "WMPLoc.dll,-29557", "", fr'explorer.exe "{Main_File_Directory}"'],
	},
	__CMD_KEY: {
		__CMD_VDTHB: {
			"01_CMD_01_MakeClusterC1_01": ["HD 1080p (Cluster 01)", "ImageRes.dll,-71", fr'py "{Main_File}" -a "%1" -r 1080p -c 1{Preset}'],
			"02_CMD_02_MakeClusterC1_02": ["HD 1080p (Cluster 02)", "ImageRes.dll,-83", fr'py "{Main_File}" -a "%1" -r 1080p -c 2{Preset}']
		},
		__CMD_VIDEO: {
			"03_CMD_03_MakeVideo2160_01": ["4K 2160p", "WMPLoc.dll,-503", fr'py "{Main_File}" -a "%1" -r 216p -nt -nd{Preset}'],
			"04_CMD_04_MakeVideo1080_02": ["HD 1080p", "ImageRes.dll,-23", fr'py "{Main_File}" -a "%1" -r 1080p -nt -nd{Preset}'],
			"05_CMD_05_MakeVideo720_03": ["HD 720p", "WMPLoc.dll,-29538", fr'py "{Main_File}" -a "%1" -r 720p -nt -nd']
		},
		__CMD_THUMB: {
			"06_CMD_05_MakeThumbnailC1_01": ["Cluster 01", "Shell32.dll,-63001", fr'py "{Main_File}" -a "%1" -c 1 -nv -nd{Preset}'],
			"07_CMD_06_MakeThumbnailC1_02": ["Cluster 02", "ImageRes.dll,-70", fr'py "{Main_File}" -a "%1" -c 2 -nv -nd{Preset}']
		}
	}
}

#-=-=-=-=-=-#

for Setting, Value in Config.items():
	Context_Key = Registry(Keys[1])
	_CWD_1 = Context_Key.cwd()

	Context_Key.relcd(Setting)
	if Setting == "Shell":
		for Key, Values in Value.items():
			Context_Key.relcd(Key)

			if Values:
				Context_Key.set(None, Values[0])
				Context_Key.set("Icon", Values[1])

				if len(Values) > 3:
					Context_Key.relcd("command")
					Context_Key.set(None, Values[3])
					Context_Key.relcd("..")
				elif len(Values) < 4:
					Context_Key.set("ExtendedSubCommandsKey", Values[2])
			else:
				Context_Key.set("CommandFlags", 8, "D-Word")

			Context_Key.relcd("..")
	else:
		Reg = Registry(_CWD_1 + f"/{Setting}")
		_CWD_2 = Reg.cwd()

		for Name, Directory in Value.items():
			Reg = Registry(_CWD_2 + f"/{Name}/Shell")

			_CWD_3 = Reg.cwd()
			for Name, Value in Directory.items():
				Reg = Registry(_CWD_3 + Name)

				Reg.set(None, Value[0])
				Reg.set("Icon", Value[1])

				Reg.relcd("command")
				Reg.set(None, Value[2])