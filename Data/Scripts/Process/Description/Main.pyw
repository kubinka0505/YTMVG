print("{1}<INFO>{3} Making Description... │ {2}1/2{3} │ {0}0.00 KB (-0.00 KB / -0.00%){3}".format(
	Styles.OK, Styles.Info, Styles.Meta_Info_2, Styles.Reset
	)
)

#-=-=-=-#

Metadata = ""
Missing_Fields = []
Final_Tags = {}

# Get _Tags
if Type == "MP3":
	_Tags = {Tag: str(Audio_Tags[Tag]) for Tag in list(Audio_Tags)}

if Type in ("FLAC", "VORBIS"):
	_Tags = {Key: ", ".join(Value) for Key, Value in dict(Audio_Tags).items()}

#-=-=-=-#

# Assign tags appropriately
for Key, Value in Audio_Tags_List[Type].items():
	if not Value in _Tags:
		Missing_Fields += [Key]
		_Tags[Value] = f"<INSERT_{Key.upper()}>"
	Final_Tags[Key] = _Tags[Value]
	exec(f'{Key} = "{_Tags[Value]}"')

# Skip basic tags
__LastBasicTagIndex = list(Final_Tags.keys()).index("Organization") + 1
Final_Tags = dict(list(Final_Tags.items())[__LastBasicTagIndex:])

#-=-=-=-#

# Description variables
for Delimiter in ("&", "ft", "ft.", "feat", "feat.", "featuring"):
	Delimiter = f" {Delimiter} "
	Artist = Artist.replace(Delimiter, Delimiter.upper())
	Artist = Artist.replace(Delimiter.upper(), " · ")

Artists = Artist.split(",")
Artists = (Artist.strip(".").strip() for Artist in Artists)
Artist = ", ".join(Artists)

Now = dt.now()
Release_Date = Now.strftime("%Y-%m-%d")

#-=-=-=-#

if Final_Tags:
	Metadata = "\n".join((f"{Key}: {Value}" for Key, Value in Final_Tags.items()))

if Missing_Fields:
	print("{1}<WARNING>{2} {0} audio tag fields were not detected, description file will be incomplete.{3}".format(
		len(Missing_Fields),
		Styles.Info, Styles.Warning, Styles.Reset
		)
	)

#-=-=-=-#
# Description fill

Description = Description[1:-1].replace("\n", "\n\n")
Description = Description.format(
	__name__,
	Title, Artist,
	Album,
	Year,
	Organization, Release_Date,
	Metadata
)

with open(Text_File, "w", encoding = "U8") as File:
	File.write(Description)
	print("\n{2}<INFO>{4} Making Description... │ {3}2/2{4} │ {1}{0} (+{0} / +100.00%){4}".format(
		FM.Utils.Get.Size(len(Description)),
		Styles.OK, Styles.Info, Styles.Meta_Info_2, Styles.Reset
		)
	)
	print("{0}Done!{1}".format(
		Styles.OK, Styles.Reset
		)
	)