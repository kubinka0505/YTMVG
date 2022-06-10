# Settings
args.directory = FM.Utils.Get.Path(args.directory)

if args.quiet:
	os.sys.stdout = open(os.devnull, "w", encoding = "U8")
	Verbose = ("-q", "-loglevel 0")
else:
	Verbose = ("-v", "")

BEL = "" if args.no_bell else "\a"

Directory = FM.Utils.Get.Path("./Videos")
if not os.path.exists(Directory):
	os.mkdir(Directory)

#-=-=-=-#

if args.no_video:
	Video_Paths = (0,)

if all((args.no_video, args.no_thumbnail)):
	Error("I'm not doing anything.")

#-=-=-=-=-=-#

args.audio = FM.Utils.Get.Path(args.audio)
Audio = FM.Utils.Get.Path(
	FM.Upload.Media(args.audio, mFile, "audio")
)

if not args.image:
	File = mFile(Audio)
	try:
		Type = File.mime[0].split("/")[-1].capitalize()
	except AttributeError:
		Error("Not an audio file!")
	if len(Type) < 5:
		Type = Type.upper()

	#-=-=-=-#

	Traceback = 'Front cover art was not found in file! ("' + os.path.basename(Audio) + '")'

	try:
		if Type in ("WAV", "MP3"):
			File = File.tags["APIC:"].data
		elif Type == "FLAC":
			File = File.pictures[0].data
		elif Type == "Vorbis":
			File = File.tags["coverart"]
		else:
			raise KeyError
	except (KeyError, IndexError):
		Error(Traceback)

	#-=-=-=-#

	im = Image.open(BytesIO(File)).convert("RGBA").convert("RGB")
	args.image = os.path.join(Directory, "Cover.png")
	im.save(args.image, quality = 100)

Cover = FM.Upload.Media(
	FM.Utils.Get.Path(args.image), Image.open, "image"
)

#-=-=-=-#

## Thumbnail
args.cluster = Clusters[str(args.cluster)] - 1

args.brightness = float(args.brightness.strip("%"))
args.brightness = Clamp(args.brightness, 25, 100)

args.brightness /= 100

## Video
args.resolution = int("".join(filter(lambda Character: Character.isdigit(), args.resolution)))

# Audio
args.bitrate = "".join((Character for Character in args.bitrate if Character.isdigit()))
args.bitrate = Clamp(int(args.bitrate), 96, 265)

#-=-=-=-#

if args.bitrate < 1:
	args.audio_options = "FLAC"
else:
	args.audio_options = "AAC -b:a {0}k".format(args.bitrate)

Audio_Quality = "-c:a " + args.audio_options.lower()