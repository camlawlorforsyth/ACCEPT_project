# this script assumes Python 3.5 is in use

# imports
import os

def main(cluster, num_obs) :
    
    file = open("../issues.txt", "a") # open for writing in data/, appending to
                                      # the end of the file if it exists
    
    if num_obs > 1 : # for clusters with more than 1 observation
        
        num_file = len(os.listdir(cluster + "/merged")) # the number of files
                                            # present in [cluster_name]/merged/
        if num_file < (num_obs + 1)*3 : # flux_obs creates 3 files for every
                                        # ObsID, plus 3 additional merged files
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
    
    return
