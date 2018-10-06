import sys
import os

f = open("good.txt", "a")

'''
The calling code used in verify_reproj.py for this file, is of the form:
python checks/expcor_count.py 1E0657_56 3184 5356 5361 0.296 1.1945
arg[-]       arg[0]             arg[1]  arg[3]...arg[-3] arg[-2] arg[-1]
'''

length = len(sys.argv) # length = 7 for the example above
obsnum = length - 4 # obsnum = 7 - 4 = 3, as we can see from above
cluster = sys.argv[1] # the cluster name, as indicated

if obsnum > 1: # for clusters with more than 1 observation
    filenum = len(os.listdir(cluster + "/expcor_mosaic_2")) # the number of files present in [cluster_name]/expcor_mosaic_2/
    if filenum < (obsnum + 1)*3: # flux_obs creates 3 files for every ObsId, plus 3 additional merged files
        f.write(cluster + " is bad\n")
    else:
        f.write(cluster + " is good\n")
else:
    f.write(cluster + " is good\n")

f.close()
