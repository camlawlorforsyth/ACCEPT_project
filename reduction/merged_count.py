# this script assumes Python 3.5 is in use

'''
The calling code used in reduce1.py for this file, is of the form:
python ../reduction/merged_count.py 1E_0657-56 554 3184 4984 4985 4986 5355 5356 5357 5358 5361
argv[-]           argv[0]             argv[1] argv[2] ... argv[N]
'''

# imports
import os
import sys

length = len(sys.argv) # length = 12 for the example above
num_obs = length - 2 # num_obs = 12 - 2 = 10, as we can see from above
cluster = sys.argv[1] # the cluster name, as indicated

file = open("../issues.txt", "a") # open for writing in data/, appending to the
                                  # end of the file if it exists

if num_obs > 1 : # for clusters with more than 1 observation
    num_file = len(os.listdir(cluster + "/merged")) # the number of files
                                            # present in [cluster_name]/merged/
    if num_file < (num_obs + 1)*3 : # flux_obs creates 3 files for every ObsId,
                                    # plus 3 additional merged files
        file.write(cluster + "'s merged/ directory has an issue.\n")
    else :
        file.write(cluster + "'s merged/ directory is fine.\n")
    num_file = len(os.listdir(cluster + "/merged_2")) # the number of files
                                          # present in [cluster_name]/merged_2/
    if num_file < (num_obs + 1)*3 :
        file.write(cluster + "'s merged_2/ directory has an issue.\n")
    else :
        file.write(cluster + "'s merged_2/ directory is fine.\n")
else :
    file.write(cluster + " only has one observation and is therefore fine.\n")

file.close()
