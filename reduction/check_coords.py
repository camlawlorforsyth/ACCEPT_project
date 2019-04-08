# this script assumes Python 3.5 is in use

# imports
import os

def main(cluster) :
    
    file = open("../issues.txt", "a") # open for writing in data/, appending to
                                      # the end of the file if it exists
    
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
    
    file.close()
    
    return
