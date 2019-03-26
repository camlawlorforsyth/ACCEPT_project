# this script assumes Python 3.5 is in use

# imports
import sys
import os

file = open("issues.txt", "a")

'''
The calling code used in verify_reproj.py for this file, is of the form:
python checks/expcor_count.py 1E_0657-56 0.296 1.1945 554 3184 4984 4985 4986 5355 5356 5357 5358 5361
argv[-]       argv[0]         argv[1]   argv[3] argv[4] ... argv[N]
'''

length = len(sys.argv) # length = 14 for the example above
num_obs = length - 4 # num_obs = 14 - 4 = 10, as we can see from above
cluster = sys.argv[1] # the cluster name, as indicated

if num_obs > 1 : # for clusters with more than 1 observation
    num_file = len(os.listdir(cluster + "/expcor_mosaic_2")) # the number of
                            # files present in [cluster_name]/expcor_mosaic_2/
    if num_file < (num_obs + 1)*3 : # flux_obs creates 3 files for every ObsId,
                                    # plus 3 additional merged files
        file.write(cluster + " has an issue.\n")
    else:
        file.write(cluster + " is fine.\n")
else:
    file.write(cluster + " only has one observation and is therefore fine.\n")

file.close()
