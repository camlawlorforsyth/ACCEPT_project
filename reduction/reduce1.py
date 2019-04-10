# this script assumes Python 3.5 is in use

'''
For information regarding how this script is initialized, see the 'README.md'
file in reduction/README.md.

The calling code used in get_all_data.py for this file, is of the form:
subprocess.run(['python','reduction/reduce1.py','1E_0657-56','104.6234458','-55.94438611','0.296','1.1945','554','3184','4984','4985','4986','5355','5356','5357','5358','5361'])
                 argv[-]         argv[0]           argv[1]      argv[2]        argv[3]    argv[4]  argv[5] argv[6] ... argv[N]
'''

# imports
import os
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

# http://cxc.harvard.edu/ciao/threads/all.html
# http://cxc.harvard.edu/ciao/threads/imag.html
# http://cxc.harvard.edu/ciao/threads/diffuse_emission/

subprocess.run("mkdir " + cluster, shell=True) # create a new directory for the
                                               # cluster
os.chdir(cluster) # change to the cluster directory

## STEP 1 - OBTAIN DATA FROM THE CHANDRA DATA ARCHIVE ##

# http://cxc.harvard.edu/ciao/threads/intro_data/
# http://cxc.harvard.edu/ciao/threads/archivedownload/
# http://cxc.harvard.edu/ciao/ahelp/download_chandra_obsid.html

cmd = "download_chandra_obsid " # download Chandra data 

for i in range(6, length-1) :
    cmd += str(sys.argv[i]) + "," # creates a comma-separated list of the
                                  # passed ObsIds
cmd += str(sys.argv[length-1]) + " -q" # append the last ObsId

subprocess.run(cmd, shell=True) # pass the download command to the system

## STEP 2 - REDUCE/REPROCESS DATA TO LEVEL=2 ##

# http://cxc.harvard.edu/ciao/threads/createL2/
# http://cxc.harvard.edu/ciao/ahelp/chandra_repro.html

cmd = "chandra_repro '*' outdir=''" # reprocess all ObsIds, do not save
                                    # intermediate files
subprocess.run(cmd, shell=True) # pass the reprocess command to the system

## STEP 3 - REPROJECT AND COMBINE ##

# http://cxc.harvard.edu/ciao/threads/merge_all/
# http://cxc.harvard.edu/ciao/threads/reproject_image/
# http://cxc.harvard.edu/ciao/threads/combine/
# http://cxc.harvard.edu/ciao/ahelp/punlearn.html
# http://cxc.harvard.edu/ciao/ahelp/merge_obs.html
# http://cxc.harvard.edu/ciao/ahelp/reproject_obs.html
# http://cxc.harvard.edu/ciao/ahelp/flux_obs.html

subprocess.run("punlearn reproject_obs", shell=True) # restore system default
                                                     # parameter values
cmd = "reproject_obs '*/repro/*evt2*' reproj/" # reproject all ObsIds
subprocess.run(cmd, shell=True)

subprocess.run("punlearn flux_obs", shell=True)  # restore system defaults
cmd = ("flux_obs 'reproj/*reproj_evt.fits' merged/ bin=0.5 units=time " + 
       "psfecf=0.393 psfmerge=expmap") # for GGM filtering
subprocess.run(cmd, shell=True)
cmd = ("flux_obs 'reproj/*reproj_evt.fits' merged_2/ bin=2 units=time " +
       "psfecf=0.393 psfmerge=expmap") # for CAS analysis and unsharp mask
subprocess.run(cmd, shell=True)

## STEP 4 - CHECK ALL MERGED FILES ARE PRESENT ##

merged_count.main(cluster, length-6) # prints to data/issues.txt

## STEP 5 - DEFINE REGION OF INTEREST, MEASURE TOTAL COUNTS, SAVE ROI ##

# http://cxc.harvard.edu/ciao/ahelp/dmmakereg.html

quality = ROI_count.main('merged_2/broad_flux.img', RA, Dec, redshift,Rout_Mpc)
    # determine if cluster has sufficient data
    # if data is sufficient, create ds9_fk5.reg file, and bk.reg file

with open('../cas_process_all_data.py', 'a') as file :
    file.write("subprocess.run(['python','reduction/reduce2.py','" + cluster +
               "','" + str(RA) + "','" + str(Dec) + "','" + str(redshift) +
               "','" + str(Rout_Mpc) + "','" + quality + "'])\n" ) # append
               # quality flag to cas_process_all_data.py

## STEP 6 - CONSTRAIN DATA TO REGION OF INTEREST (Rout_Mpc) ##

if quality == "sufficient" :
    
    subprocess.run("mkdir ROI", shell=True) # trim the images to the ROI
    subprocess.run("mkdir ROI_2", shell=True)    
    
    subprocess.run("punlearn dmcopy", shell=True)
    subprocess.run("dmcopy 'merged/broad_flux.img[sky=region(ds9_fk5.reg)]' " +
                   "ROI/broad_flux_ROI.fits", shell=True)
    subprocess.run("dmcopy 'merged/broad_thresh.img[sky=region(ds9_fk5.reg)]' " +
                   "ROI/broad_thresh_ROI.fits", shell=True)
    subprocess.run("dmcopy 'merged/broad_thresh.expmap[sky=region(ds9_fk5.reg)]' " +
                   "ROI/broad_thresh_expmap_ROI.fits", shell=True)
    subprocess.run("dmcopy 'merged/broad_thresh.psfmap[sky=region(ds9_fk5.reg)]' " +
                   "ROI/broad_thresh_psfmap_ROI.fits", shell=True)   
    
    subprocess.run("dmcopy 'merged_2/broad_flux.img[sky=region(ds9_fk5.reg)]' " +
                   "ROI_2/broad_flux_ROI.fits", shell=True)
    subprocess.run("dmcopy 'merged_2/broad_thresh.img[sky=region(ds9_fk5.reg)]' " +
                   "ROI_2/broad_thresh_ROI.fits", shell=True)
    subprocess.run("dmcopy 'merged_2/broad_thresh.expmap[sky=region(ds9_fk5.reg)]' " +
                   "ROI_2/broad_thresh_expmap_ROI.fits", shell=True)
    subprocess.run("dmcopy 'merged_2/broad_thresh.psfmap[sky=region(ds9_fk5.reg)]' " +
                   "ROI_2/broad_thresh_psfmap_ROI.fits", shell=True)  
    
## STEP 7 - DETECT POINT SOURCES ##

# http://cxc.harvard.edu/ciao/guides/esa.html
# http://cxc.harvard.edu/ciao/threads/detect_overview/
# http://cxc.harvard.edu/ciao/threads/wavdetect/
# http://cxc.harvard.edu/ciao/threads/wavdetect_merged/
# http://cxc.harvard.edu/ciao/ahelp/wavdetect.html
    
    subprocess.run("punlearn wavdetect", shell=True) # restore system defaults
    subprocess.run("pset wavdetect infile=ROI_2/broad_thresh_ROI.fits",
                   shell=True) # wavdetect will not work with fluxed images
    subprocess.run("pset wavdetect psffile=ROI_2/broad_thresh_psfmap_ROI.fits",
                   shell=True)
    subprocess.run("pset wavdetect expfile=ROI_2/broad_thresh_expmap_ROI.fits",
                   shell=True)
    subprocess.run("pset wavdetect scales='1 2 4 8 16'", shell=True)
    subprocess.run("pset wavdetect outfile=broad_thresh_src.fits", shell=True)
    subprocess.run("pset wavdetect scellfile=broad_thresh_scell.fits",
                   shell=True)
    subprocess.run("pset wavdetect imagefile=broad_thresh_recon.fits",
                   shell=True)
    subprocess.run("pset wavdetect defnbkgfile=broad_thresh_nbkgd.fits",
                   shell=True)
    subprocess.run("pset wavdetect regfile=sources.reg", shell=True)
    subprocess.run("pset wavdetect ellsigma=4", shell=True)
    subprocess.run("wavdetect infile=ROI_2/broad_thresh_ROI.fits " +
                   "outfile=broad_thresh_src.fits " +
                   "scellfile=broad_thresh_scell.fits " +
                   "imagefile=broad_thresh_recon.fits " +
                   "defnbkgfile=broad_thresh_nbkgd.fits " +
                   "scales='1 2 4 8 16' " +
                   "psffile=ROI_2/broad_thresh_psfmap_ROI.fits", shell=True)

## STEP 8 - CLEANUP ##

# do some cleanup, ie. delete unnecessary ObsIds files

os.chdir("..") # go back to the data/ directory

'''
the sources in sources.reg can now be viewed in ds9 and any spurious detections
can be deleted. now save this file as 'sources_mod.reg' in CIAO+physical
'''
