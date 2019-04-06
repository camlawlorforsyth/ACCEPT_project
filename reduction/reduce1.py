# this script assumes Python 3.5 is in use

'''
For information regarding how this script is initialized, see the 'README.md'
file in reduction/README.md.

The calling code used in get_all_data.py for this file, is of the form:
python reduction/reduce1.py 1E_0657-56 0.296 1.1945 554 3184 4984 4985 4986 5355 5356 5357 5358 5361
argv[-]       argv[0]        argv[1]  argv[2] argv[3] ... argv[N]
'''

# imports
import os
import sys

length = len(sys.argv) # length = 14 for the example above
cluster = sys.argv[1] # the cluster name, as indicated
redshift = float(sys.argv[2]) # the given redshift
Rout_Mpc = float(sys.argv[3]) # the maximum outer radius used by Cavagnolo+

## STEP 0 - CREATE CLUSTER DIRECTORY ##

os.system("mkdir " + cluster) # create a new directory for the cluster
os.chdir(cluster) # change directory to the cluster directory

## STEP 1 - OBTAIN DATA FROM THE CHANDRA DATA ARCHIVE ##

# http://cxc.harvard.edu/ciao/threads/intro_data/
# http://cxc.harvard.edu/ciao/threads/archivedownload/
# http://cxc.harvard.edu/ciao/ahelp/download_chandra_obsid.html

cmd = "download_chandra_obsid " # download Chandra data 

for i in range(4, length-1) :
    cmd += str(sys.argv[i]) + "," # creates a comma-separated list of the
                                  # passed ObsIds
cmd += str(sys.argv[length-1]) + "-q" # append the last ObsId

os.system("echo " + cmd) # pass the download command to the system
os.system(cmd)
cmd = ""

## STEP 2 - REDUCE/REPROCESS DATA TO LEVEL=2 ##

# http://cxc.harvard.edu/ciao/threads/createL2/
# http://cxc.harvard.edu/ciao/ahelp/chandra_repro.html

cmd = "chandra_repro '*' outdir=''" # reprocess all ObsIds, do not save
                                    # intermediate files
os.system("echo " + cmd) # pass the reprocess command to the system
os.system(cmd)
cmd = ""

## STEP 3 - REPROJECT AND COMBINE ##

# http://cxc.harvard.edu/ciao/threads/merge_all/
# http://cxc.cfa.harvard.edu/ciao/threads/combine/
# http://cxc.harvard.edu/ciao/ahelp/punlearn.html
# http://cxc.harvard.edu/ciao/ahelp/merge_obs.html
# http://cxc.harvard.edu/ciao/ahelp/reproject_obs.html
# http://cxc.harvard.edu/ciao/ahelp/flux_obs.html

os.system("punlearn reproject_obs") # restore system default parameter values

cmd = "reproject_obs '*/repro/*evt2*' reproj/" # reproject all ObsIds
os.system("echo " + cmd)
os.system(cmd)
cmd = ""

os.system("punlearn flux_obs")  # restore system default parameter values

cmd = "flux_obs 'reproj/*reproj_evt.fits' merged/ bin=0.5 units=time" # for GGM
os.system("echo " + cmd)                                            # filtering
os.system(cmd)
cmd = "flux_obs 'reproj/*reproj_evt.fits' merged_2/ bin=2 units=time" # for CAS
os.system("echo " + cmd)                            # analysis and unsharp mask
os.system(cmd)
cmd = ""

## STEP 4 - CHECK MERGED FILES ARE PRESENT ##

cmd = "python ../reduction/merged_count.py " + cluster

for i in range(4, length) :
    cmd += (" " + str(sys.argv[i])) # a space-separated list of the ObsIds

os.system("echo " + cmd) # pass the check command to the system
os.system(cmd)
cmd = ""

## STEP 5 - DEFINE REGION OF INTEREST, MEASURE TOTAL COUNTS, SAVE ROI ##

# http://cxc.harvard.edu/ciao/ahelp/dmmakereg.html

os.system("python ../reduction/ROI_count.py " + cluster +
          "merged_2/broad_flux.img " + str(redshift) + " " + str(Rout_Mpc) +
          " >> cas_process_all_data.py") # determine if cluster has sufficient
    # data and append quality flag to cas_process_all_data.py
    # if data is sufficient, create ds9_fk5.reg file, and bk.reg file

## STEP 6 - CLEANUP ##

# do some cleanup, ie. delete unnecessary ObsIds files

os.chdir("..") # go back to the data/ directory
