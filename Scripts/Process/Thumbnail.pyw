with Image.open(Cover) as CVR:
	try:
		CVR.seek(1)
	except EOFError:
		Traceback = ""
	else:
		Traceback = "static"
	#-=-=-=-#
	Size = set(map(str, CVR.size))
	#-=-=-=-#
	if Traceback:
		Traceback = "Cover image is not " + Traceback
		Error(Traceback)

Cover_Process = Image.open(Cover)
Cover_Copy = os.path.join(Directory + "/YTMVG_" + str(time() * 2).split(".")[-1] + ".png")

#-=-=-=-#

# Rescaling Cover
if max(Cover_Process.size) > args.resolution:
	Cover_Process.thumbnail((args.resolution,) * 2, 1)
	print("{2}Cover dimensions ({0}) exceeded maximum resolution ({1}p), downscaling...{3}".format(
		"x".join(map(str, Image.open(Cover).size)), args.resolution,
		Styles.Warning, Styles.Reset
		)
	)
	print("\n" + "─" * 33 + "\n")
Cover_Process.save(Cover_Copy, quality = 100)

#-=-=-=-#

# Make Thumbnail
Thumbnail_Path = os.path.join(Directory, "Thumbnail.jpg")

print(Styles.Reset + "Making Thumbnail... | {2}1/3{4} | {1}0:00:00.000{4} | {0}0.00 KB (-0.00 KB / -0.00%){3}".format(
	Styles.OK, Styles.Info, Styles.Meta_Info_2,
	Styles.Flaw, Styles.Reset
	)
)
__START_THUMB = time()

Generate_Thumbnail(
	Cover,
	Thumbnail_Path,
	args.brightness
)

#-=-=-=-#

# Optimize Thumbnail
Size_In_Thumbnail = os.path.getsize(Thumbnail_Path)
print(("\r" if args.quiet else "\n") + Styles.Reset + \
	"Making Thumbnail... | {4}2/3{6} | {3}{0}{6} | {2}{1} (+{1} / +100.00%){5}".format(
	str(td(seconds = time() - __START_THUMB))[:-3],
	FM.Utils.Get.Size(Size_In_Thumbnail),
	Styles.OK, Styles.Info, Styles.Meta_Info_2,
	Styles.Flaw, Styles.Reset
	)
)

# jpegoptim "$IN" -m 100 -o --all-progressive --strip-all
os.system('{0} -m 100 -S2048 -o --all-progressive --strip-all --dest="{1}" "{2}" {3}'.format(
	__JPEGOptim, Directory, Thumbnail_Path, Verbose[0]
	)
)

# Re-optimize Thumbnail
Size_In_Thumbnail = os.path.getsize(Thumbnail_Path)
if Size_In_Thumbnail > 2048E3:
	print("{1}Thumbnail size exceeded 2.00 MB ({0}), trying to recompress to 1.90 MB...{2}".format(
		FM.Utils.Get.Size(Size_In_Thumbnail), Styles.Warning, Styles.Flaw
		)
	)
	os.system('{0} -m 100 -S1946 -o --all-progressive --strip-all "{1}" {2}'.format(
		__JPEGOptim, Thumbnail_Path, Verbose[0]
		)
	)

#-=-=-=-#

# Print information
Size_Out_Thumbnail = os.path.getsize(Thumbnail_Path)
print(("\r" if args.quiet else "\n") + Styles.Reset + \
	"Making Thumbnail... | {6}3/3{8} | {5}{0}{8} | {4}{1} (-{2} / -{3}%){7}".format(
	str(td(seconds = time() - __START_THUMB))[:-3],

	FM.Utils.Get.Size(Size_Out_Thumbnail), FM.Utils.Get.Size(Size_In_Thumbnail - Size_Out_Thumbnail),
	Percentage(Size_Out_Thumbnail, Size_In_Thumbnail),

	Styles.OK, Styles.Info, Styles.Meta_Info_2,
	Styles.Flaw, Styles.Reset
	)
)
print(Styles.OK + "Done!" + Styles.Reset)
print(Styles.Reset + "\n\r" + "─" * 33 + "\n")

#-=-=-=-#

# Move Thumbnail
if not args.no_thumbnail:
	os.rename(
		Thumbnail_Path,
		os.path.join(Final_Directory, "Thumbnail.jpg")
	)

#-=-=-=-#

Cover = Cover_Copy