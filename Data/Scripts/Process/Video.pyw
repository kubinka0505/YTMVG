Video_Names = []
for Path in ("Video", Audio_Names[0]):
	Name = os.path.join(Final_Directory, Path)
	if len(Name) > 252:
		Name = Name[:-4]
		print("{0}<WARNING>{2} {1}Video final path exceeds 256 characters, name will be truncated.{2}".format(
			Styles.Info, Styles.Warning, Styles.Reset
			)
		)
	Video_Names += [f"{Name}.mp4"]

#-=-=-=-#

# Make Video
print("{1}<INFO>{4} Making Video... │ {2}1/3{4} │ {1}0:00:00.000{4} │ {0}0.00 KB (-0.00 KB / -0.00%){3}".format(
	Styles.OK, Styles.Info, Styles.Meta_Info_2,
	Styles.Warning, Styles.Reset
	)
)

__START_VIDEO = time()

os.system("""
	{package} -r 12 -i "{audio_in}" -loop 1 -i "{image_in}"
	-ab {audio_quality} -c:a {audio_codec} -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2"
	-tune stillimage -pix_fmt yuv420p
	-shortest -strict -2 "{video_out}" -y {verbosity}
	"""[2:-2].replace("\n\t", " ").format(
		package = __FFmpeg,
		verbosity = Verbose[1],

		audio_in = Audio,
		image_in = Cover,
		video_out = Video_Names[0],

		audio_quality = Audio_Quality,
		audio_codec = Audio_Codec
	)
)

#-=-=-=-#

# Trim Duration
Size_In_Video = os.path.getsize(Video_Names[0])
End_Time = str(round(mFile(Video_Names[0]).info.length, 3))

print("\n{3}<INFO>{6} Making Video... │ {4}2/3{6} │ {3}{0}{6} │ {2}{1} (+{1} / +100.00%){5}".format(
	str(td(seconds = time() - __START_VIDEO))[:-3], FM.Utils.Get.Size(Size_In_Video),
	Styles.OK, Styles.Info, Styles.Meta_Info_2,
	Styles.Warning, Styles.Reset
	)
)

# WebM optimization setup
if args.webm_encode:
	Video_Names[1] = Video_Names[1].rstrip(".mp4") + ".webm"

	Video_Codec = "libvpx-vp9"
	# Video_Codec = "libvpx-vp8" 
	Audio_Codec = "libvorbis"

os.system("""
	{package} -r 12 -i "{video_in}" -t {video_ending}
	-c:v {video_codec}{video_quality} {video_scaleFix}
	-c:a {audio_codec}{audio_quality} -ac {audio_channels}
	-fflags +bitexact -flags:v +bitexact -flags:a +bitexact
	-map 0 -map_metadata 0:s:0 -shortest -strict -2 "{video_out}" -y {verbosity}
	"""[2:-2].replace("\n\t", " ").format(
		package = __FFmpeg,
		verbosity = Verbose[1],

		video_in = Video_Names[0],
		video_out = Video_Names[1],
		video_codec = Video_Codec,
		video_ending = End_Time,
		video_quality = " -q:v 5" if args.webm_encode else "",
		video_scaleFix = '-vf "scale={0}:-1:flags=bilinear"'.format(args.resolution),

		audio_codec = Audio_Codec,
		audio_quality = "" if args.webm_encode else f" -ab {Audio_Quality}",
		audio_channels = Channels
	)
)

#-=-=-=-#

# Print Information
Size_Out_Video = os.path.getsize(Video_Names[1])
print("\n{5}<INFO>{8} Making Video... │ {6}3/3{8} │ {5}{0}{8} │ {4}{1} (-{2} / -{3}%){7}".format(
	str(td(seconds = time() - __START_VIDEO))[:-3],

	FM.Utils.Get.Size(Size_Out_Video), FM.Utils.Get.Size(Size_In_Video - Size_Out_Video),
	Percentage(Size_Out_Video, Size_In_Video),

	Styles.OK, Styles.Info, Styles.Meta_Info_2,
	Styles.Warning, Styles.Reset
	)
)
print("{0}Done!{1}".format(
	Styles.OK, Styles.Reset
	)
)

#-=-=-=-#

os.remove(Video_Names[0])