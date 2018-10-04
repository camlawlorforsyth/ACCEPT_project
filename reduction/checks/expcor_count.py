import sys
import os

f = open("good.txt", "a")

length = len(sys.argv)
obsnum = length - 4
cluster = sys.argv[1]

if obsnum > 1:
    filenum = len(os.listdir(cluster + "/expcor_mosaic_2"))
    if filenum < (obsnum + 1)*3:
        f.write(cluster + " is bad\n")
    else:
        f.write(cluster + " is good\n")
else:
    f.write(cluster + " is good\n")

f.close()
