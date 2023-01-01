for Requirement in ("JPEGOptim", "FFmpeg"):
	exec("""
	__{0} = "{0}".lower()
	__{0} = Variable_Search(__{0})
	if not __{0}:
		Error("{0} not found!")
	"""[2:-2].replace("\n\t", "\n").format(Requirement)
	)