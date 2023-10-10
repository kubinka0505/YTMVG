from sklearn import metrics
from sklearn.cluster import KMeans

#-=-=-=-#

def __GTL(Log: str, Info: str = "", End: str = "\n"):
	return print("{2}<IMAGE>{3} {0:<50}{1}".format(
			str(Log), str(Info) if Info else "",
			Styles.Warning, Styles.Flaw, 
		), end = End
	)

def __StepSort(R: int, G: int, B: int, Repetitions: int = 1, Smooth: bool = True) -> tuple:
	L = sqrt(0.241 * R + 0.691 * G + 0.068 * B)
	H, S, V = rgb_to_hsv(R, G, B)
	H2 = int(H * Repetitions)
	L2 = int(L * Repetitions)
	V2 = int(V * Repetitions)
	if all((Smooth, H2 % 2)):
		V2 = Repetitions - V
		L = Repetitions - L
	return (H2, L, V2)

def __RGB2(IT):
	IT = "#" + "".join(("{:02X}".format(x) for x in IT))
	return ColorHandler(IT)

#-=-=-=-#

Picture = Cover.convert("RGB")
ThumbChar = "■"

#-=-=-=-#

# Calculate dimensions (aspect ratio)
Dimensions = Image.new("RGB", (16, 9), "red")
Dimensions = contain(Dimensions, (float("inf"), min(Picture.size)))
Size = Dimensions.size
__GTL("Calculated dimensions", " x ".join(map(str, Size)))

#-=-=-=-#

# --- USE COLOR ALGORITHM HERE --- #
	
# PIL to CV2
image = np.array(Picture)
image = image[:, :, ::-1].copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (2 ** 7,) * 2)

__GTL("Retrieving clusters...", End = "\r")
image_array = image.reshape((image.shape[0] * image.shape[1], 3))
Cluster = KMeans(n_init = 10)
Cluster.fit(image_array)

numLabels = np.arange(0, len(np.unique(Cluster.labels_)) + 1)
hist = np.histogram(Cluster.labels_, bins = numLabels)[0].astype("float")
hist /= hist.sum()

# Very rare exception
# https://stackoverflow.com/a/10063039

Colors = []
try:
	zipped = sorted(zip(hist, Cluster.cluster_centers_))
	zipped.sort(reverse = 1, key = lambda x: x[0])
	hist, Cluster.cluster_centers = zip(*zipped)

	# Convert to list of RGB tuples
	zipped = [list(x[1]) for x in zipped]
	Colors = [tuple([int(y) for y in x]) for x in zipped]
	#Colors = [tuple([int(y) // 1 for y in x]) for x in zipped]
except ValueError:
	# Add individual resampling modes
	for Mode in range(1, 5 + 1):
		Colors += [contain(Picture, (2, 2), Mode).getpixel((0, 0))]

# Remove grayscale occurences
if Cover.mode != "L":
	__GO = 0
	for Grayscale in range(255):
		Grayscale = (Grayscale,) * 3
		if Grayscale in Colors:
			Colors.remove(Grayscale)
			__GO += 1
	__GTL("Removed monochrome colors", f"{__GO} found")

# Remove duplicates
__RD = len(Colors)
Colors = list(set(Colors))
__RD = __RD - len(Colors)
__GTL("Removed duplicated colors", f"{__RD} found")

# Sort
__CBS = Colors
Colors = sorted(Colors, key = lambda C: __StepSort(*C, 8, 0))
Colors = dict(zip([__RGB2(x).saturation for x in Colors], Colors))
Colors = list(dict(sorted(Colors.items())).values())[::-1]
__CBS = [i for i, x in enumerate(zip(Colors, __CBS)) if x[0] != x[1]]
__CBS = len(__CBS) if __CBS else 0
__GTL("Sorted colors", f"{__CBS} changed its place")

"""
# Balance primitively
__RD = [len(Colors), 0, 0]
for c in range(len(Colors)):
	threshold = 6.25
	#---#
	threshold /= 100
	threshold = (2 * threshold, 1 - threshold)
	try:
		c_ = __RGB2(Colors[c])
		#---#
		if threshold[1] > c_.luminance:
			Colors.remove(Colors[c])
			__RD[1] += 1
		#---#
		if c_.luminance < threshold[0]:
			Colors.remove(Colors[c])
			__RD[2] += 1
	except IndexError:
		pass

__RD[0] = __RD[0] - len(Colors)
__GTL("Balanced colors", f"{__RD[0]} removed ({__RD[2]} bright, {__RD[1]} dark)")
"""

if not Colors:
	for Mode in range(6):
		Colors += [contain(Picture, (2, 2), Mode).getpixel((0, 0))]

# COLOR SORTING TEST
# Create and show resized `Image` with every color from `Colors`
if args.color_sorting_test:
	__GTL("Launched color sorting test")
	__Counter = 0
	CSTI = Image.new("RGB", (len(Colors), 1), (0,) * 3)
	for C in Colors:
		CSTI.putpixel((__Counter, 0), C)
		__Counter += 1
	SIZE = int(max(__geometry.split("+")[0].split("x"))) // 6
	CSTI = CSTI.resize((CSTI.size[0] * SIZE, CSTI.size[1] * SIZE), 0)
	CSTI.show()	

# Determine color index
if args.color == 1:
	args.color = 0
if args.color == 2:
	args.color = -3

BgCol = Colors[args.color]
BgCol = Image.new("RGB", (1, 1), tuple(BgCol))
__GTL(
	"Determined color",
	__RGB2(BgCol.getpixel((0, 0))).hex_l.upper()
)

# Apply brightness
BgCol = Brightness(BgCol).enhance(args.brightness)
__GTL("Applied brightness", " │ ".join(
	(
		str(args.brightness) + "x",
		str(args.brightness * 100) + "%"
		)
	)
)

# Apply saturation
BgCol = Color(BgCol).enhance(args.saturation)
__GTL("Applied saturation", " │ ".join(
	(
		str(args.saturation) + "x",
		str(args.saturation * 100) + "%"
	)
))

BgColCover = contain(Picture, (2, 2))
BgColCover = Color(BgColCover).enhance(4)
BgColCover = BgColCover.getpixel((0, 0))

#-=-=-=-#
# Specify color

BgCol = BgCol.getpixel((0, 0))
__BgCol = []
__BgCol += [
	__RGB2(BgCol),
	__RGB2(BgColCover[:3])
]
__BgCol = [Color.hex_l.upper() for Color in __BgCol]
__GTL("Specified the color", __BgCol[0])

#-=-=-=-#
# Generate background
Background = Image.new("RGB", Size, BgCol)
__GTL(
	"Generated background",
	fg(*RGB(__BgCol[0])) + ThumbChar * 3
)

# Paste original picture
Background.paste(
	Picture, (
		(Background.size[0] - Picture.size[0]) // 2,
		(Background.size[1] - Picture.size[1]) // 2
	), Picture.convert("RGBA")
)
__GTL(
	"Pasted original picture",
	"".join(
		(
			fg(*RGB(__BgCol[0])) + ThumbChar,
			fg(*RGB(__BgCol[1])) + ThumbChar,
			fg(*RGB(__BgCol[0])) + ThumbChar + Styles.Flaw
		)
	)
)

#-=-=-=-#

if args.resize_thumbnail:
	if max(Background.size) > 1280:
		__GTL('Resized to "MaxResDefault.jpg" size', "1280 x 720")
		Background = contain(Background, (1280, 720), 3)

Background.convert("RGB").save(Thumbnail_Path, quality = 100, optimize = 1)
__GTL("Saved image", FM.Utils.Get.Size(os.path.getsize(Thumbnail_Path)))