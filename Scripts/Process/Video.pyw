Video_Paths = []
for Path in ("Video", Audio_Name[0]):
	Video_Paths += [os.path.join(Final_Directory, Path + ".mp4")]

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
	{3} -ar 44100 -c:v libx264
	-vf "pad=ceil(iw/2)*2:ceil(ih/2)*2"
	-tune stillimage -pix_fmt yuv420p
	-shortest -strict -2 "{4}" -y {5}
	"""[2:-2].replace("\n\t", " ").format(
		__FFmpeg, Audio, Cover,
		Audio_Quality,
		Video_Paths[0], Verbose[1]
	)
)

#-=-=-=-#

# Trim Duration
Size_In_Video = os.path.getsize(Video_Paths[0])
End_Time = str(round(mFile(Video_Paths[0]).info.length, 3))

print(("\r" if args.quiet else "\n") + Styles.Reset + \
	"Making Video... | {4}2/3{6} | {3}{0}{6} | {2}{1} (+{1} / +100.00%){5}".format(
	str(td(seconds = time() - __START_VIDEO))[:-3], FM.Utils.Get.Size(Size_In_Video),
	Styles.OK, Styles.Info, Styles.Meta_Info_2,
	Styles.Warning, Styles.Reset
	)
)

os.system("""
	{0} -r 12 -i "{1}" -t {2} -c:v libx264 {3}
	-fflags +bitexact -flags:v +bitexact -flags:a +bitexact
	-map 0 -map_metadata 0:s:0 -shortest -strict -2 "{4}" -y {5}
	"""[2:-2].replace("\n\t", " ").format(
		__FFmpeg, Video_Paths[0], End_Time, Audio_Quality, Video_Paths[1], Verbose[1]
	)
)

#-=-=-=-#

# Print Information
Size_Out_Video = os.path.getsize(Video_Paths[1])
print(("\r" if args.quiet else "\n") + Styles.Reset + \
	"Making Video... | {6}3/3{8} | {5}{0}{8} | {4}{1} (-{2} / -{3}%){7}".format(
	str(td(seconds = time() - __START_VIDEO))[:-3],

	FM.Utils.Get.Size(Size_Out_Video), FM.Utils.Get.Size(Size_In_Video - Size_Out_Video),
	Percentage(Size_Out_Video, Size_In_Video),

	Styles.OK, Styles.Info, Styles.Meta_Info_2,
	Styles.Warning, Styles.Reset
	)
)
print(Styles.OK + "Done!" + Styles.Reset)
print(Styles.Reset + "\n\r" + "─" * 33 + "\n")

#-=-=-=-#

os.remove(Video_Paths[0])