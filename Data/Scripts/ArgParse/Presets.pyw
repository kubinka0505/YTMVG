__CantLoad = "Couldn\'t load the \"{0}\" preset!"

if args.preset:
	args.preset = args.preset.lower().strip()

	__Presets = FM.Utils.Get.Path("Data/Presets")

	for File in path(__Presets).glob("*.txt"):
		File = str(File.resolve())

		if os.path.isfile(File):
			File_Name = ".".join(os.path.basename(File).split(".")[:-1])

			if File_Name.lower() == args.preset:
				Content = open(File).readlines()

				for Line in Content:
					Line = [Chunk.strip().replace(" ", "_") for Chunk in Line.strip().split("=")]
					Line[0] = Line[0].lower()

					if Line[0] in args:
						try:
							exec('args.{0} = {1}'.format(*Line))
						except Exception as Error:
							print('\n{3}<ERROR>{5} | {0} ({4}{1} - {2}{5})'.format(
								__CantLoad.format(File_Name),
								Error.__class__.__name__, Error,
								Styles.Info, Styles.Error, Styles.Reset
								)
							)	
							break
					else:
						print('\n{2}<WARNING>{4} | {3}{0} ({1} not in arguments.{4})'.format(
							__CantLoad.format(File_Name),
							Styles.Info, Styles.OK, Styles.Reset
							)
						)				
						break

				print('\n{1}<INFO>{3} | {2}Successfully loaded the "{0}" preset.{3}'.format(
					File_Name,
					Styles.Info, Styles.OK, Styles.Reset
					)
				)
				break