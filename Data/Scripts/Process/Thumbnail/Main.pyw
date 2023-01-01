Cover = Image.open(Cover)

try:
	Cover.seek(1)
except EOFError:
	Traceback = ""
else:
	Traceback = "static"
	Cover.seek(0)

#-=-=-=-#

if Traceback:
	Traceback = f"Cover image is not {Traceback}"
	Error(Traceback)

Cover_Process = Cover.copy()
Cover_Copy = os.path.join(Directory + f"/YTMVG_TempFile_{__RAND_STR}.png")

#-=-=-=-#

# Rescaling Cover
if max(Cover.size) > args.resolution:
	Cover_Process.thumbnail((args.resolution,) * 2, 1)
	print("{2}<WARNING>{4} | {3}Cover dimensions ({0}) exceeded maximum video resolution ({1}p), downscaling...{4}".format(
		"x".join(map(str, Cover_Process.size)), args.resolution,
		Styles.Info, Styles.Warning, Styles.Reset
		)
	)

Cover_Process.save(Cover_Copy, quality = 100)

#-=-=-=-#

# Make Thumbnail
__THUMB_NAME = f"Thumbnail.jpg"
Thumbnail_Path = os.path.join(Directory, __THUMB_NAME)

print(Styles.Reset + "Making Thumbnail... | {2}1/3{4} | {1}0:00:00.000{4} | {0}0.00 KB (-0.00 KB / -0.00%){3}".format(
	Styles.OK, Styles.Info, Styles.Meta_Info_2,
	Styles.Flaw, Styles.Reset
	)
)
__START_THUMB = time()

exec(open_("Process/Thumbnail/Colors"))

#-=-=-=-#

Size_In_Thumbnail = os.path.getsize(Thumbnail_Path)
Size_In_Thumbnail_1 = os.path.getsize(Thumbnail_Path)
print("\n{6}Making Thumbnail... | {4}2/3{6} | {3}{0}{6} | {2}{1} (+{1} / +100.00%){5}".format(
		str(td(seconds = time() - __START_THUMB))[:-3],
		FM.Utils.Get.Size(Size_In_Thumbnail),
		Styles.OK, Styles.Info, Styles.Meta_Info_2,
		Styles.Flaw, Styles.Reset
	)
)

# Optimize Thumbnail
if Size_In_Thumbnail > 2048E3:
	os.system('{0} -m 100 -S2047 -o --all-progressive --strip-all --dest="{1}" "{2}" {3}'.format(
		__JPEGOptim, Directory, Thumbnail_Path, Verbose[0]
		)
	)
else:
	print("Thumbnail size is below 2.00 MB, not optimizing.")

# Re-optimize Thumbnail
Size_In_Thumbnail = os.path.getsize(Thumbnail_Path)
if Size_In_Thumbnail > 2048E3:
	print("{1}<WARNING>{4} | {2}Thumbnail size exceeded 1.99 MB ({0}), will recompress to ≈1.85 MB.{3}".format(
		FM.Utils.Get.Size(Size_In_Thumbnail),
		Styles.Info, Styles.Warning, Styles.Flaw, Styles.Reset
		)
	)
	os.system('{0} -m 100 -S1895 -o --all-progressive --strip-all "{1}" {2}'.format(
		__JPEGOptim, Thumbnail_Path, Verbose[0]
		)
	)

#-=-=-=-#

# Print information
Size_Out_Thumbnail = os.path.getsize(Thumbnail_Path)
print("\n{8}Making Thumbnail... | {6}3/3{8} | {5}{0}{8} | {4}{1} (-{2} / -{3}%){7}".format(
		str(td(seconds = time() - __START_THUMB))[:-3],

		FM.Utils.Get.Size(Size_Out_Thumbnail) if Size_Out_Thumbnail > 2048E3 else "-0.00 KB",
		FM.Utils.Get.Size(Size_In_Thumbnail_1 - Size_Out_Thumbnail),
		Percentage(Size_Out_Thumbnail, Size_In_Thumbnail_1),

		Styles.OK, Styles.Info, Styles.Meta_Info_2,
		Styles.Flaw, Styles.Reset
	)
)
print(Styles.OK + "Done!" + Styles.Reset)

#-=-=-=-#

# Move Thumbnail
if not args.no_thumbnail:
	os.rename(
		Thumbnail_Path,
		os.path.join(Final_Directory, __THUMB_NAME.replace(f"_{__RAND_STR}.", "."))
	)

#-=-=-=-#

Cover = Cover_Copy