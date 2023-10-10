if os.sys.platform == "win32":
	open_command = r"start /max C:\Windows\explorer.exe"

	if not args.no_video:
		open_command += " /select,"
elif os.sys.platform.startswith("linux"):
	distro = distro_name()
	if distro == "ubuntu":
		open_command = "nautilus"
	elif distro == "debian":
		open_command = "nemo"
	elif distro == "rhel":
		open_command = "gnome-open"
	else:
		open_command = "xdg-open"
else:
	open_command = "open"

#-=-=-=-#

# Null device
if os.sys.platform == "win32":
	null_device = ""
else:
	null_device = ">/dev/null 2>&1"

if args.no_video:
	open_target = Final_Directory
else:
	open_target = Video_Names[-1]

#-=-=-=-#

open_command += ' "{0}" {1}'.format(open_target, null_device)
os.system(open_command)