import os
from glob import glob
import shutil


path = "G:\\Shared drives\\TriplegangersGroom_ext\\Groom_INTERNAL\\"

grooms = [x for x in glob(path+"**\\maya\\**\\scenes\\")]

#rename files in directory to base.ma and base__{collection}.xgen

# in each individual directory
for groom in grooms:
    print("new dir", groom)
    #search for directory with any files
    files = glob(groom+"*.*")
    print("files = \n", files)
    ## if there are two files
    if "base.ma" != files[0].split("\\")[-1]:
        for file in files:
            #print(file)
            if ".ma" in file:
                newpath = "\\".join(file.split("\\")[:-1])+"\\base.ma"
                print("rename {0} to {1}".format(file, newpath))
                shutil.move(file, newpath)
            elif ".xgen" in file:
                path = file.split("__")[0]
                coll = file.split("__")[1]
                newpath = "\\".join(path.split("\\")[:-1])+"\\base__{}".format(coll)
                print("rename {0} to {1}".format(file, newpath))
                shutil.move(file, newpath)
    else:
        print("already complete")

