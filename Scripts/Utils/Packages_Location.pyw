modules = __import__("pkg_resources").working_set
modules = (Module.project_name for Module in modules)

#-=-=-=-#

for Requirement in ("JPEGOptim", "FFmpeg"):
	exec("""
	__{0} = "{0}".lower()
	__{0} = Variable_Search(__{0})
	if not __{0}:
		Error("{0} not found!")
	"""[2:-2].replace("\n\t", "\n").format(Requirement)
	)

if "ffpb" in modules:
	__FFmpeg = "FFPB"
else:
	__FFmpeg += " -hide_banner -loglevel 24"

__FFmpeg = __FFmpeg.lower()