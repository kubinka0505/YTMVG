Tags = 0
try:
	Tags = Audio_File.tags
except Exception as Traceback:
	Tags = 0
	print('\n{1}<WARNING>{2} | {0}Couldn\'t create description - File doesn\'t start with an ID3 tag.{2}'.format(
		Styles.Warning, Styles.Info, Styles.Reset
		)
	)

if Tags:
	exec(open_("Process/Description/Main"))