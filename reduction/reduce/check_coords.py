# this script assumes Python 3.5 is in use

'''
The calling code used in reduce2.py for this file, is of the form:
python ../reduce/check_coords.py 1E_0657-56 complete
argv[-]          argv[0]         argv[1]    argv[2]
'''

# imports
import os
import sys

cluster = sys.argv[1] # the cluster name, as indicated
quality = sys.argv[2] # quality flag indicating if enough data is present

file = open("issues.txt", "a") # open for writing, appending to the end of
                               # the file if it exists

if quality == "complete" :
    
    os.chdir(cluster)
    
    if (not os.path.isfile("ds9_fk5.reg")) :
        file.write(cluster + " is labelled correctly," +
                   " but 'ds9_fk5.reg' is missing.\n")
    else :
        newfile = open("ds9_fk5.reg", "r") # open for reading
        newfile.readline() # read the first line of ds9_fk5.reg
        f6 = newfile.read(6) # read the first 6 characters
        if (f6 != "global") :
            file.write(cluster + "'s ds9_fk5.reg file is saved in the wrong " +
                       "coordinates.\n")
        newfile.close()
    
    if (not os.path.isfile("merged_2/bk.reg")) :
        file.write(cluster + " is labelled correctly," +
                   " but 'bk.reg' is missing.\n")
    else :
        newfile = open("merged_2/bk.reg", "r")
        newfile.readline()
        f6 = newfile.read(6)
        if (f6 != "circle") :
            file.write(cluster + "'s bk.reg file is saved in the wrong " +
                       "coordinates.\n")
        newfile.close()
    
    if (not os.path.isfile("merged_2/sources_mod.reg")) :
        file.write(cluster + " is labelled correctly," +
                   " but bin2 'sources_mod.reg' is missing.\n")
    else :
        newfile = open("merged_2/sources_mod.reg", "r")
        newfile.readline()
        f6 = newfile.read(6)
        if (f6 != "circle") :
            file.write(cluster + "'s bin2 'sources_mod.reg' file is saved " +
                       "in the wrong coordinates.\n")
        newfile.close()
    
    if (not os.path.isfile("merged/sources_mod.reg")) :
        file.write(cluster + " is labelled correctly," +
                   " but bin0.5 'sources_mod.reg' is missing.\n")
    else :
        newfile = open("merged/sources_mod.reg", "r")
        newfile.readline()
        f6 = newfile.read(6)
        if (f6 != "circle") :
            file.write(cluster + "'s bin0.5 'sources_mod.reg' file is saved " +
                       "in the wrong coordinates.\n")
        newfile.close()
    
    os.chdir("..")

file.close()
