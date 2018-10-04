import os
import sys

clusterName = sys.argv[1]
bad = sys.argv[2]

L = open("good.txt", "a")

if bad == "d":
    os.chdir(clusterName)

    if ( not os.path.isfile("ds9_fk.reg")):
        L.write(clusterName + " is labeled good, but 'ds9_fk.reg' is missing!\n")
    else: 
        f = open("ds9_fk.reg", "r")
        f.readline()
        f6 = f.read(6)
        if (f6 != "global"):
            L.write(clusterName + "'s ds9_fk.reg file is saved in the wrong coordinates!\n")
    	f.close()

    if ( not os.path.isfile("expcor_mosaic_2/bk.reg")):
        L.write(clusterName + " is labeled good, but 'bk.reg' is missing!\n")
    else: 
        f = open("expcor_mosaic_2/bk.reg", "r")
        f.readline()
        f6 = f.read(6)
        if (f6 != "circle"):
            L.write(clusterName + "'s bk.reg file is saved in the wrong coordinates!\n")            
	    f.close()

    if ( not os.path.isfile("expcor_mosaic_2/sources_mod.reg")):
        L.write(clusterName + " is labeled good, but bin2 'sources_mod.reg' is missing!\n")
    else: 
        f = open("expcor_mosaic_2/sources_mod.reg", "r")
        f.readline()
        f6 = f.read(6)
        if (f6 != "circle"):
            L.write(clusterName + "'s bin2 'sources_mod.reg' file is saved in the wrong coordinates!\n")            
	    f.close()

    if ( not os.path.isfile("expcor_mosaic/sources_mod.reg")):
        L.write(clusterName + " is labeled good, but bin0.5 'sources_mod.reg' is missing!\n")
    else: 
        f = open("expcor_mosaic/sources_mod.reg", "r")
        f.readline()
        f6 = f.read(6)
        if (f6 != "circle"):
            L.write(clusterName + "'s bin0.5 'sources_mod.reg' file is saved in the wrong coordinates!\n")            
	    f.close()
    os.chdir("..")
L.close()
