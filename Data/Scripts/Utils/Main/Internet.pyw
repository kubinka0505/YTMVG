# This file can be removed without any consequences, but it's not recommended.
#
# Besides update notificator it also contains the message fetcher that will be
# used to inform users about future plans of the program, along with informations
# including packages changes/deprecation and such.
try:
	# Update notice
	with get(f"https://api.github.com/repos/{__Repo}/releases") as Site:
		if Site.ok:
			__version_latest__ = Site.json()[0]["tag_name"]

			if float(__version_latest__) > float(__version__):
				print("{1}<WARNING>{2} You are using not using recent version of the program. ({0})".format(__version_latest__, Styles.Info, Styles.Warning))
				print("Please consider updating if possible - updates may contain bug fixes and new features!{0}\n".format(Styles.Reset))

	# Notification
	with get(f"https://raw.githubusercontent.com/{__Repo}/master/Data/Scripts/Utils/Notification.pyw") as Site:
		if Site.ok:
			eval(Site.text)
			print("\n")
except exceptions.ConnectionError:
	pass