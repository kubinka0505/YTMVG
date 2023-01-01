if os.name == "nt":
	Command = r"start /max C:\Windows\explorer.exe"
elif os.sys.platform.startswith("lin"):
	distro = distro_name()
	if distro == "ubuntu":
		Command = "nautilus"
	elif distro == "debian":
		Command = "nemo"
	elif distro == "rhel":
		Command = "gnome-open"
	else:
		Command = "xdg-open"
else:
	Command = "open"

if os.name != "nt":
	DevNull = ">/dev/null 2>&1"
else:
	DevNull = ""

#-=-=-=-#

Command +=  ' "{0}" {1}'.format(Final_Directory, DevNull)
os.system(Command)
