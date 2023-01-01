Video_Names = []
for Path in ("Video", Audio_Names[0]):
	Name = os.path.join(Final_Directory, Path)
	if len(Name) > 252:
		Name = Name[:-4]
		print("{1}<WARNING>{2} | {0}Video final path exceeds 256 characters, name will be truncated.{2}".format(
			Styles.Info, Styles.Warning, Styles.Reset
			)
		)
	Video_Names += [f"{Name}.mp4"]

#-=-=-=-#

# Make Video
print(Styles.Reset + "Making Video... | {2}1/3{4} | {1}0:00:00.000{4} | {0}0.00 KB (-0.00 KB / -0.00%){3}".format(
	Styles.OK, Styles.Info, Styles.Meta_Info_2,
	Styles.Warning, Styles.Reset
	)
)

__START_VIDEO = time()

os.system("""
	{0} -r 12 -i "{1}" -loop 1 -i "{2}"
	{3} -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2"
	-tune stillimage -pix_fmt yuv420p
	-shortest -strict -2 "{4}" -y {5}
	"""[2:-2].replace("\n\t", " ").format(
		__FFmpeg, Audio, Cover,
		Audio_Quality,
		Video_Names[0], Verbose[1]
	)
)

#-=-=-=-#

# Trim Duration
Size_In_Video = os.path.getsize(Video_Names[0])
End_Time = str(round(mFile(Video_Names[0]).info.length, 3))

print("\n{6}Making Video... | {4}2/3{6} | {3}{0}{6} | {2}{1} (+{1} / +100.00%){5}".format(
	str(td(seconds = time() - __START_VIDEO))[:-3], FM.Utils.Get.Size(Size_In_Video),
	Styles.OK, Styles.Info, Styles.Meta_Info_2,
	Styles.Warning, Styles.Reset
	)
)


os.system("""
	{0} -r 12 -i "{1}" -t {3}{2}
	-c:v libx264 -c:a aac {4} -ac {5}
	-fflags +bitexact -flags:v +bitexact -flags:a +bitexact
	-map 0 -map_metadata 0:s:0 -shortest -strict -2 "{6}" -y {7}
	"""[2:-2].replace("\n\t", " ").format(
		__FFmpeg, Video_Names[0],
		' -vf "scale={0}:-1:flags=bilinear"'.format(args.resolution),
		End_Time, Audio_Quality, args.channels,
		Video_Names[1], Verbose[1]
	)
)

#-=-=-=-#

# Print Information
Size_Out_Video = os.path.getsize(Video_Names[1])
print("\n{8}Making Video... | {6}3/3{8} | {5}{0}{8} | {4}{1} (-{2} / -{3}%){7}".format(
	str(td(seconds = time() - __START_VIDEO))[:-3],

	FM.Utils.Get.Size(Size_Out_Video), FM.Utils.Get.Size(Size_In_Video - Size_Out_Video),
	Percentage(Size_Out_Video, Size_In_Video),

	Styles.OK, Styles.Info, Styles.Meta_Info_2,
	Styles.Warning, Styles.Reset
	)
)
print(Styles.OK + "Done!" + Styles.Reset)

#-=-=-=-#

os.remove(Video_Names[0])