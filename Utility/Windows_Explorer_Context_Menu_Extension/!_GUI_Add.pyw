for File in "Init", "Main":
	exec(open(f"__{File.lower()}__.pyw", encoding = "U8").read())

#-=-=-=-=-=-=-=-=-=-=-#

Message = """
Successfully injected the values into the HKEY_CURRENT_USER hive.

From now on, you can make the videos by selecting
{0} files WITH EMBEDDED FRONT COVER ART
and chosing the appropriate option from the "{1}"
dropdown menu by right-clicking.
"""[1:-1].format(" / ".join(Formats), Main_File_Name)

print(Message)
if __file__.endswith(".pyw"):
	MsgBox.showinfo("Success!", Message)
else:
	system("pause")