__YT = fg.white + "You" + bg.red + "Tube" + bg.rs + Styles.Reset

Parser = ArgumentParser(
	prog = __name__ + ".py",
	description = __doc__.split("\n")[0].replace("YouTube", __YT),
	add_help = 0,
	allow_abbrev = 0,
	formatter_class = \
	lambda prog, size = float("inf"): \
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

Palette_Sizes = [Number for Number in range(8, 16 + 1, 1)]

Clusters = {
	"1": 1, "DOM": 1, "Dominant": 1,
	"2": 2, "AVG": 2, "Average": 2,
	"3": 3, "ALT": 3, "Alternative": 3	
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
	metavar = '"str"', help = "Audio file path. {0}Accepts MP3/FLAC/WAV/OGG".format(Styles.OK)
)

Required.add_argument(
	"-i", "--image", type = str,
	default = Config["Media"]["Image"]["Path"],
	metavar = '"str"',
	help = '{1}Static{2} image file path. {0}If unspecified, attempts to get embedded cover art from "-a"{2}'.format(
		Styles.Info, Styles.Error, Styles.Reset
	)
)

#-=-=-=-#
# Background

Background.add_argument(
	"-bgs", "--palette-size", type = int,
	choices = Palette_Sizes,
	default = Config["Media"]["Image"]["Thumbnail"]["Background"]["Cluster"]["Palette_Size"],
	metavar = "8>=int<=16",
	help = "Size of the color palette used to generate the clusters"
)

Background.add_argument(
	"-c", "--cluster", type = str,
	choices = Clusters.keys(),
	default = Config["Media"]["Image"]["Thumbnail"]["Background"]["Cluster"]["Number"],
	metavar = "1>=int<=3",
	help = 'Number of cluster used as a background image color. {0}Dominant{1}/{0}Average{1}/{0}Alternative{1}'.format(
		Styles.OK, Styles.Reset
	)
)

Background.add_argument(
	"-bgb", "--brightness", type = str,
	default = Config["Media"]["Image"]["Thumbnail"]["Background"]["Properties"]["Brightness"],
	metavar = "[25>=float<=100]%",
	help = "Thumbnail background brightness, in {0}%%".format(Styles.Warning)
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
	"-ab", "--bitrate", type = str,
	default = str(Config["Media"]["Audio"]["Bitrate"]),
	metavar = "[96>=int<=512]k",
	help = "{0}Video audio bitrate{4}, in {2}kb/s{4}. If {2}< 1{4}, the {3}experimental{4} lossless {1}FLAC{4} codec is used".format(
		Styles.Info, Styles.Meta_Info_2, Styles.Warning, Styles.Error, Styles.Reset
	)
)

#-=-=-=-#
# Switch

Optional.add_argument(
	"-d", "--directory", type = str,
	default = Config["Settings"]["Directory"]["Output"],
	metavar = '"str"',
	help = "Moves the directory with generated files to the given location"
)

Switch.add_argument(
	"-nv", "--no-video", action = ArgParseBool(not Config["Media"]["Video"]["Generate"]),
	help = "Doesn't generate the video"
)

Switch.add_argument(
	"-nt", "--no-thumbnail", action = ArgParseBool(not Config["Media"]["Image"]["Thumbnail"]["Generate"]),
	help = "Doesn't generate the thumbnail"
)

Switch.add_argument(
	"-ni", "--no-information", action = ArgParseBool(not Config["Settings"]["Logs"]["Information"]),
	help = "Doesn't print the final files paths & runtime"
)

Switch.add_argument(
	"-nb", "--no-bell", action = ArgParseBool(not Config["Settings"]["Logs"]["Sound"]),
	help = 'Doesn\'t print the {0}"BEL"{1} character'.format(Styles.Meta_Info_2, Styles.Reset)
)

Switch.add_argument(
	"-q", "--quiet", action = ArgParseBool(not Config["Settings"]["Logs"]["Main"]),
	help = 'Doesn\'t print anything. {0}It\'s prior over all other output arguments, except "-nb"'.format(
		Styles.Error
	)
)

Switch.add_argument(
	"-nod", "--no-open-directory",
	action = ArgParseBool(not Config["Settings"]["Directory"]["Open"]),
	help = SUPPRESS
)

Switch.add_argument("-h", "--help", action = "help", help = "Shows this message")

#-=-=-=-#

for Argument in Parser._actions:
	if not Argument.help.endswith((SUPPRESS, "!")):
		Argument.help += Styles.Reset + "."

args = Parser.parse_args()