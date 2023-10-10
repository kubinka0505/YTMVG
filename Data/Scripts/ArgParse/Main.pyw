__YT = fg.white + "You" + bg.red + "Tube" + bg.rs + Styles.Reset

Parser = ArgumentParser(
	prog = __name__ + ".py",
	description = __doc__.split("\n")[0].replace("YouTube", __YT),
	add_help = 0,
	allow_abbrev = 0,
	formatter_class = \
	lambda prog, size = 750: \
		HelpFormatter(
			prog, width = size,
			max_help_position = size
		)
	)

#-=-=-=-#

Resolutions = (
	4320, 2160,
	1440, 1080, 720,
	480, 360, 240, 144
)

Colors_Dict = {
	"1": 1, "Wet": 1,
	"2": 2, "Dry": 2
}

#-=-=-=-#

Required = Parser.add_argument_group("Required arguments")
Background = Parser.add_argument_group("Background color arguments")
Optional = Parser.add_argument_group("Optional arguments")
Switch = Parser.add_argument_group("Switch arguments")

#-=-=-=-#
# Required

Required.add_argument(
	"-a", "--audio", type = str, required = 1,
	default = Config["Media"]["Audio"]["Path"],
	metavar = '"str"', help = "Audio file path or URL. {0}Accepts {0}".format(
		"/".join(__ALLOWED_FORMATS), Styles.OK
	)
)

Required.add_argument(
	"-i", "--image", type = str,
	default = Config["Media"]["Image"]["Path"],
	metavar = '"str"',
	help = '{1}Static{2} image file path or URL. {0}If none, tries to get an embedded front cover art from "-a"{2}'.format(
		Styles.Info, Styles.Error, Styles.Reset
	)
)

#-=-=-=-#
# Background

Background.add_argument(
	"-c", "--color", type = str,
	choices = Colors_Dict.keys(),
	default = Config["Media"]["Image"]["Thumbnail"]["Background"]["Color"]["Type"],
	metavar = "[1, 2]",
	help = "Index of the element of the image color clusters list"
)

Background.add_argument(
	"-bgb", "--brightness", type = str,
	default = Config["Media"]["Image"]["Thumbnail"]["Background"]["Properties"]["Brightness"],
	metavar = "[range(25, 75)]%",
	help = "Thumbnail background color brightness, in {0}%%".format(Styles.Warning)
)

Background.add_argument(
	"-bgs", "--saturation", type = str,
	default = Config["Media"]["Image"]["Thumbnail"]["Background"]["Properties"]["Saturation"],
	metavar = "[range(100, 250)]%",
	help = "Thumbnail background color saturation, in {0}%%".format(Styles.Warning)
)

#-=-=-=-#
# Optional

Optional.add_argument(
	"-r", "--resolution", type = str,
	choices = [str(Resolution) + "p" for Resolution in Resolutions],
	default = Config["Media"]["Video"]["Maximum_Resolution"],
	metavar = "[int]p",
	help = "Maximum video resolution"
)

Optional.add_argument(
	"-ab", "--audio-bitrate", type = str,
	default = str(Config["Media"]["Audio"]["Bitrate"]),
	metavar = "[range(96, 256)]k",
	help = "{0}Video audio bitrate{4}, in {2}kb/s{4}. If {2}> 255{4}, the {3}experimental{4} lossless {1}FLAC{4} codec is used".format(
		Styles.Info, Styles.Meta_Info_2, Styles.Warning, Styles.Error, Styles.Reset
	)
)

Optional.add_argument(
	"-d", "--directory", type = str,
	default = Config["Settings"]["Directory"]["Output"],
	metavar = '"str"',
	help = "Moves the directory with generated files to provided location"
)

Optional.add_argument(
	"-p", "--preset", type = str, default = Config["Settings"]["Preset"],
	metavar = '["{0}", ...]'.format('", "'.join([
		".".join(File.split(".")[:-1]).lower()
		for File in os.listdir("Data/Presets")[:2]
	])),
	help = "Preset name in {0}Data/Presets{2} directory. {1}Bypasses already set command flags{2}".format(
		Styles.OK, Styles.Error,
		Styles.Reset
	)
)

Optional.add_argument(
	"-v", "--verbosity", type = int,
	choices = (-1, 0, 1, 2),
	default = Config["Settings"]["Logs"]["Verbosity"],
	metavar = "[-1, 0, 1, 2]",
	help = "Verbosity level. {0}-1{2} for {1}none{2}, {0}0{2} for {1}basic FFmpeg stats{2}, {0}1{2} for {1}everything{2}, {0}2{2} for {1}extended logs{2}".format(
		Styles.Info, Styles.Meta_Info_2,
		Styles.Reset
	)
)

#-=-=-=-#
# Switch

Switch.add_argument(
	"-rt", "--resize-thumbnail", action = ArgParseBool(Config["Media"]["Image"]["Thumbnail"]["Resize"]),
	help = "Resizes thumbnail to {0}1280x720{1} if one of cover's dimensions exceeds {0}1280{1}".format(
		Styles.Info, Styles.Reset
	)
)

Switch.add_argument(
	"-webm", "--webm-encode", action = ArgParseBool(not Config["Media"]["Video"]["WebM"]),
	help = "Encodes {0}WebM{3} file instead of {1}MP4{3} one, resulting in smaller file size. {2}Extremely slow{3}!".format(
		Styles.OK, Styles.Meta_Info_2, Styles.Error, Styles.Reset
	)
)

Switch.add_argument(
	"-nv", "--no-video", action = ArgParseBool(Config["Media"]["Video"]["Generate"]),
	help = "Doesn't generate the video file"
)

Switch.add_argument(
	"-nt", "--no-thumbnail", action = ArgParseBool(Config["Media"]["Image"]["Thumbnail"]["Generate"]),
	help = "Doesn't generate the thumbnail image"
)

Switch.add_argument(
	"-nd", "--no-description", action = ArgParseBool(Config["Media"]["Description"]["Generate"]),
	help = "Doesn't generate the description file"
)

Switch.add_argument(
	"-nb", "--no-bell", action = ArgParseBool(Config["Settings"]["Logs"]["Sound"]),
	help = 'Doesn\'t print the {0}"BEL"{1} character at the final print'.format(Styles.Meta_Info_2, Styles.Reset)
)

Switch.add_argument(
	"-nod", "--no-open-directory",
	action = ArgParseBool(Config["Settings"]["Directory"]["Open"]),
	help = "Doesn't open directory after finishing"
)

Switch.add_argument(
	"-cst", "--color-sorting-test",
	action = "store_true",
	help = SUPPRESS
)

Switch.add_argument("-h", "--help", action = "help", help = "Shows this message")

#-=-=-=-#

for Argument in Parser._actions:
	if not Argument.help.endswith((SUPPRESS, "!")):
		Argument.help += Styles.Reset + "."

args = Parser.parse_args()