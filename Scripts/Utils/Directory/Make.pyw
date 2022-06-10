Audio_Name = []
Audio_Name += [".".join(Audio.split(os.sep)[-1].replace("_", " ").split(".")[:-1])]
Audio_Name += [Audio_Name[0] + "_" + str(time() * 2).split(".")[-1]]
Final_Directory = os.path.join(Directory, Audio_Name[1])

#-=-=-=-#

os.mkdir(Final_Directory)