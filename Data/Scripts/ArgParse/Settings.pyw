# Settings
args.directory = FM.Utils.Get.Path(args.directory)

if args.verbosity == -1:
	os.sys.stdout = open(os.devnull, "w", encoding = "U8")
	Verbose = ["-q", "-8"]
elif args.verbosity == 0:
	os.sys.stdout = open(os.devnull, "w", encoding = "U8")
	Verbose = ["-q", "16"]
elif args.verbosity == 1:
	Verbose = ["-v", "16"]
elif args.verbosity == 2:
	Verbose = ["-v", "32"]

if args.verbosity > -1:
	Verbose[1] += " -stats"

Verbose[1] = "-hide_banner -loglevel " + Verbose[1]

BEL = "" if args.no_bell else "\a"

Directory = FM.Utils.Get.Path("Videos")
if not os.path.exists(Directory):
	os.mkdir(Directory)

## Presets
exec(open_("ArgParse/Presets"))

#-=-=-=-#

if args.no_video:
	Video_Names = (0,)

if all((args.no_video, args.no_thumbnail)):
	Error("I'm not doing anything.")

#-=-=-=-=-=-#

GUI = 0
if any((not args.audio, args.audio == "<select>")):
	GUI = 1
	__Wait = "Select tagged audio file"
	try:
		print(__Wait, " " * 64, end = "\r")
		args.audio = fd.askopenfilename(
			title = __Wait,
			initialdir = FM.Utils.Get.Path("~/Music"),
			filetypes = [
				("MPEG Audio Layer 3", "*.mp3"),
				("Free Lossless Audio Codec", "*.flac"),
				("Ogg Vorbis", "*.ogg"),
				("All files", "*.*"),
			],
			defaultextension = "*.mp3"
		)
	except TclError:
		pass

args.audio = FM.Utils.Get.Path(args.audio)
if not args.audio.upper().endswith(("MP3", "FLAC", "OGG")):
	raise Error("Unsupported audio file format.")
Audio = FM.Utils.Get.Path(
	FM.Upload.Media(args.audio, mFile, "audio")
)
Audio_File = mFile(Audio)

if not args.image:
	File = Audio_File
	try:
		Type = File.mime[0].split("/")[-1].capitalize()
	except AttributeError:
		Error("Not an audio file!")
	if len(Type) < 5:
		Type = Type.upper()

	#-=-=-=-#

	try:
		if Type == "MP3":
			File = File.tags["APIC:"].data
		elif Type == "FLAC":
			File = File.pictures[0].data
		elif Type == "Vorbis":
			File = File.tags["coverart"]
		else:
			raise KeyError
		File = BytesIO(File)
	except (KeyError, IndexError):
		if GUI:
			print(Styles.Warning + "Front cover art was not found in file! Please select one.")
			File = fd.askopenfilename(
				title = "Select image file",
				initialdir = FM.Utils.Get.Path("~"),
				filetypes = [
					("Portable Network Graphics", "*.png"),
					("Lossy JPEG File", "*.jpg *.jpeg"),
					("Web Picture", "*.webp"),
					("Bitmap", "*.bmp"),
					("All files", "*.*"),
				],
				defaultextension = "*.*"
			)
			if not File:
				Error("Image selection aborted.")

	#-=-=-=-#

	# Slow loading cause
	try:
		im = Image.open(File).convert("RGB")
	except AttributeError:
		Error("File has no embedded correct front cover art image.")

	args.image = f"{Directory}/Cover_{__RAND_STR}.png"
	# Faster saving
	cv2.imwrite(
		args.image,
		cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
	)
	#im.save(args.image)

args.image = FM.Utils.Get.Path(args.image)
Cover = FM.Upload.Media(args.image, Image.open, "image")

#-=-=-=-#

## Thumbnail
args.color = Colors_Dict[str(args.color.title())]

args.brightness = float(args.brightness.strip("%"))
args.brightness = Clamp(args.brightness, 25, 75)
args.brightness /= 100

args.saturation = float(args.saturation.strip("%"))
args.saturation = Clamp(args.saturation, 75, 250)
args.saturation /= 100

#-=-=-=-#

## Video
args.resolution = int("".join(filter(lambda Character: Character.isdigit(), args.resolution)))

# Audio
args.audio_bitrate = "".join((Character for Character in args.audio_bitrate if Character.isdigit()))
args.audio_bitrate = Clamp(int(args.audio_bitrate), 96, 256)

if Audio_File.info.channels > 1:
	args.channels = "2"
else:
	args.channels = "1"

if args.audio_bitrate > 256:
	args.audio_options = "FLAC"
else:
	args.audio_options = "OPUS -ab {0}k".format(args.audio_bitrate)

Audio_Quality = "-c:a " + args.audio_options.lower()