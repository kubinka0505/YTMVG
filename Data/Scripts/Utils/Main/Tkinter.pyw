try:
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
except OSError:
	pass
Icon = os.path.abspath("Documents/Pictures/Icons/Icon.png")

#---#

try:
	root = Tk()
	root.withdraw()
	root.call("wm", "iconphoto", root._w, PhotoImage(file = Icon))

	root.update_idletasks()
	root.winfo_screenwidth()
	root.attributes("-fullscreen", 1)
	root.state("iconic")
	__geometry = root.winfo_geometry()
	root.destroy()
except TclError:
	pass