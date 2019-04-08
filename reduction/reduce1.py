# this script assumes Python 3.5 is in use

'''
For information regarding how this script is initialized, see the 'README.md'
file in reduction/README.md.

The calling code used in get_all_data.py for this file, is of the form:
subprocess.run(['python','reduction/reduce1.py','1E_0657-56','104.6234458','-55.94438611','0.296','1.1945','554','3184','4984','4985','4986','5355','5356','5357','5358','5361'])
                 argv[-]         argv[0]           argv[1]      argv[2]        argv[3]    argv[4]  argv[5] argv[6] ... argv[N]
'''

# imports
import sys
import subprocess

import merged_count
import ROI_count

# constants
length = len(sys.argv) # length = 16 for the example above
cluster = sys.argv[1] # the cluster name, as indicated
RA = float(sys.argv[2]) # the right ascension of the cluster
Dec = float(sys.argv[3]) # the declination of the cluster
redshift = float(sys.argv[4]) # the given redshift
Rout_Mpc = float(sys.argv[5]) # the maximum outer radius used by Cavagnolo+

## STEP 0 - CREATE CLUSTER DIRECTORY ##

subprocess.run("mkdir " + cluster, shell=True) # create a new directory for the
                                               # cluster
subprocess.run("cd " + cluster, shell=True) # change to the cluster directory

## STEP 1 - OBTAIN DATA FROM THE CHANDRA DATA ARCHIVE ##

# http://cxc.harvard.edu/ciao/threads/intro_data/
# http://cxc.harvard.edu/ciao/threads/archivedownload/
# http://cxc.harvard.edu/ciao/ahelp/download_chandra_obsid.html

cmd = "download_chandra_obsid " # download Chandra data 

for i in range(6, length-1) :
    cmd += str(sys.argv[i]) + "," # creates a comma-separated list of the
                                  # passed ObsIds
cmd += str(sys.argv[length-1]) + "-q" # append the last ObsId

subprocess.run(cmd, shell=True) # pass the download command to the system

## STEP 2 - REDUCE/REPROCESS DATA TO LEVEL=2 ##

# http://cxc.harvard.edu/ciao/threads/createL2/
# http://cxc.harvard.edu/ciao/ahelp/chandra_repro.html

cmd = "chandra_repro '*' outdir=''" # reprocess all ObsIds, do not save
                                    # intermediate files
subprocess.run(cmd, shell=True) # pass the reprocess command to the system

## STEP 3 - REPROJECT AND COMBINE ##

# http://cxc.harvard.edu/ciao/threads/merge_all/
# http://cxc.cfa.harvard.edu/ciao/threads/combine/
# http://cxc.harvard.edu/ciao/ahelp/punlearn.html
# http://cxc.harvard.edu/ciao/ahelp/merge_obs.html
# http://cxc.harvard.edu/ciao/ahelp/reproject_obs.html
# http://cxc.harvard.edu/ciao/ahelp/flux_obs.html

subprocess.run("punlearn reproject_obs", shell=True) # restore system default
                                                     # parameter values
cmd = "reproject_obs '*/repro/*evt2*' reproj/" # reproject all ObsIds
subprocess.run(cmd, shell=True)

subprocess.run("punlearn flux_obs", shell=True)  # restore system default
                                                 # parameter values
cmd = "flux_obs 'reproj/*reproj_evt.fits' merged/ bin=0.5 units=time" # for GGM
subprocess.run(cmd, shell=True)                                     # filtering
cmd = "flux_obs 'reproj/*reproj_evt.fits' merged_2/ bin=2 units=time" # for CAS
subprocess.run(cmd, shell=True)                     # analysis and unsharp mask

## STEP 4 - CHECK ALL MERGED FILES ARE PRESENT ##

merged_count.main(cluster, length-6) # prints to data/issues.txt

## STEP 5 - DEFINE REGION OF INTEREST, MEASURE TOTAL COUNTS, SAVE ROI ##

# http://cxc.harvard.edu/ciao/ahelp/dmmakereg.html

quality = ROI_count.main('merged_2/broad_flux.img', RA, Dec, redshift,Rout_Mpc)

with open('../cas_process_all_data.py', 'a') as file :
    file.write("subprocess.run(['python','reduction/reduce2.py','" + cluster +
               "','" + str(redshift) + "','" + str(Rout_Mpc) + "','" +
               quality + "'])" )

## STEP 6 - DETECT POINT SOURCES ##

    #================================= 6. POINT SOURCES =====================================#
#Only sources very near to xray bright emission are really necessary to remove: only those in region of extraction
#Make region around point sources in bin=2 broad_thresh.img and save regions in ciao format with physical coords: 
#make sure region of extraction is not included

#if quality == "sufficient" :
    
#    subprocess.run("", shell=True)
    

#os.system("python ../reduction/ROI_count.py " + cluster +
#          "merged_2/broad_flux.img " + str(redshift) + " " + str(Rout_Mpc) +
#          " >> cas_process_all_data.py") # determine if cluster has sufficient
    # data and append quality flag to cas_process_all_data.py
    # if data is sufficient, create ds9_fk5.reg file, and bk.reg file

## STEP 7 - CLEANUP ##

# do some cleanup, ie. delete unnecessary ObsIds files

subprocess.run("cd ..", shell=True) # go back to the data/ directory
