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

if all((args.no_video, args.no_thumbnail, args.no_description)):
	Error("It looks like I'm not doing anything.")

#-=-=-=-=-=-#

GUI = 0
if any((not args.audio, args.audio == "<select>")):
	GUI = 1
	__Wait = "Please select tagged audio file."
	try:
		print(__Wait, " " * 32, end = "\r")
		args.audio = fd.askopenfilename(
			title = __Wait,
			initialdir = Initial_Directory["Audio"],
			filetypes = [
				("MPEG Audio Layer 3", "*.mp3"),
				("Free Lossless Audio Codec", "*.flac"),
				("Ogg Vorbis", "*.ogg"),
				("All files", "*.*"),
			],
			defaultextension = "*.mp3"
		)
		if not args.audio:
			Error("File selection aborted.")
	except TclError:
		pass

# Audio
args.audio = FM.Utils.Get.File(args.audio, 0)
if args.audio[-1]: __FILES_TO_REMOVE += [args.audio[0]]
args.audio = FM.Utils.Get.Path(args.audio[0])

if not args.audio.upper().endswith(__ALLOWED_FORMATS):
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
	except (KeyError, TypeError, IndexError):
		if GUI:
			print("{0}Front cover art was not found in file! Please select one.{1}".format(
				Styles.Warning, Styles.Reset
				)
			)
			File = fd.askopenfilename(
				title = "Please select image file",
				initialdir = Initial_Directory["Image"],
				filetypes = [
					("Portable Network Graphics", "*.png"),
					("Lossy JPEG file", "*.jpg *.jpeg"),
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
		Error("Provided file has no embedded correct front cover art image.")

	args.image = os.path.join(Directory, f"Cover_{__RAND_STR}.png")
	cv2.imwrite(
		args.image,
		cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
	)

# Image
args.image = FM.Utils.Get.File(args.image, 0)
if args.image[-1]: __FILES_TO_REMOVE += [args.image[0]]
args.image = FM.Utils.Get.Path(args.image[0])
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
Video_Codec = "libx264"

# Audio
args.audio_bitrate = "".join((Character for Character in args.audio_bitrate if Character.isdigit()))
args.audio_bitrate = Clamp(int(args.audio_bitrate), 96, 257)
Audio_Quality = "{0}k".format(args.audio_bitrate)

if Audio_File.info.channels > 1:
	Channels = "2"
else:
	Channels = "1"

if args.audio_bitrate > 256:
	Audio_Codec = "flac"
else:
	Audio_Codec = "opus"