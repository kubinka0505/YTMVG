ID = str(time()).split(".")[-1].zfill(7)

#-=-=-=-#

Audio_Names = []
Audio_Names += [".".join(os.path.basename(Audio).split(".")[:-1])]
Audio_Names += ["_".join((*Audio_Names[0].split(), ID))]

Final_Directory = os.path.join(Directory, Audio_Names[1])

#-=-=-=-#

os.mkdir(Final_Directory)