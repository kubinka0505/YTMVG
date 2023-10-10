exec(open("__init__.pyw", encoding = "U8").read())

with redirect_stdout(None):
	from pyshortcuts import make_shortcut

Initial_Directory = path.abspath(path.expanduser("~/Desktop"))

#---#

Folder = fd.askdirectory(
	title = "Select directory to create the shortcut in",
	initialdir = Initial_Directory
)
Folder = path.abspath(Folder)

if Folder == getcwd():
	Folder = Initial_Directory
	raise SystemExit("Directory selection aborted.")

chdir(Folder)

#---#

Name = "YTMVG"
try:
	for Shortcut in next(walk("."))[2]:
		if Shortcut.startswith(Name + ".lnk"):
			print("Removing previous shortcut...")
			remove(path.abspath(Shortcut))
			break
except IndexError:
	pass

#---#

print("Making shortcut...")
make_shortcut(
	script = Main_File + ' -a ""',
	name = Name,
	description = "Generate the YouTube Music Video",
	icon = Icon_HQ,
	folder = Folder,
	terminal = 1,
	startmenu = 0,
)

#---#

Message = 'Successfully created shortcut in the "' + Folder.split(sep)[-1] + '" directory.'
print(Message)

if __file__.lower().endswith("pyw"):
	MsgBox.showinfo(
		title = "Success",
		message = Message,
	)
elif name == "nt":
	print()
	system()