# this script assumes Python 3.5 is in use

'''
For information regarding how this script is initialized, see the 'README.md'
file in reduction/README.md.

The calling code used in reduce_all_data.py for this file, is of the form:
subprocess.run(['python','reduction/reduce2.py','1E_0657-56','sufficient'])
                 argv[-]         argv[0]           argv[1]      argv[2]
'''

# imports
import os
import sys
import subprocess

# constants
cluster = sys.argv[1] # the cluster name, as indicated
quality = sys.argv[2] # quality flag

## STEP 1 - MOVE INTO CLUSTER DIRECTORY ##

os.chdir(cluster)

## STEP 2 - PERFORM NEXT STEPS IF DATA IS OF SUFFICIENT QUALITY ##

if quality == "sufficient" :
    
## STEPS 3-6 - REMOVE POINT SOURCES FOR bin=2 IMAGE ##
    
    os.chdir("bin_2") # move into the bin_2 directory
    
## STEP 3 - CONVERT SOURCE LIST TO FITS FORMAT ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmmakereg.html
    
    subprocess.run("punlearn dmmakereg", shell=True) # restore system defaults
    subprocess.run("dmmakereg 'region(../sources_mod.reg)' " +
                   "sources_mod.fits wcsfile=broad_thresh.fits", shell=True)
    # convert the modified source list into FITS format
    
## STEP 4 - CREATE SOURCE AND BACKGROUND REGIONS ##
    
# http://cxc.harvard.edu/ciao/ahelp/roi.html
    
    subprocess.run("mkdir sources", shell=True)
    subprocess.run("punlearn roi", shell=True) # restore system defaults
    subprocess.run("pset roi infile=sources_mod.fits", shell=True)
    subprocess.run("pset roi outsrcfile=sources/src%d.fits", shell=True)
    subprocess.run("pset roi bkgfactor=0.5", shell=True)
    subprocess.run("pset roi fovregion=''", shell=True)
    subprocess.run("pset roi streakregion=''", shell=True)
    subprocess.run("pset roi radiusmode=mul", shell=True)
    subprocess.run("pset roi bkgradius=3", shell=True)
    subprocess.run("roi mode=h", shell=True) # create source and background
    # regions for each source, combine nearby regions
    
## STEP 5 - SPLIT REGIONS INTO SOURCES AND BACKGROUNDS ##
    
# http://cxc.harvard.edu/ciao/ahelp/splitroi.html
    
    subprocess.run("splitroi 'sources/src*.fits' exclude", shell=True)
    
## STEP 6 - FILL IN HOLES ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmfilth.html
    
    subprocess.run("punlearn dmfilth", shell=True) # restore system defaults
    subprocess.run("pset dmfilth infile=broad_thresh.fits", shell=True)
    subprocess.run("pset dmfilth outfile=broad_nps.fits", shell=True)    
    subprocess.run("pset dmfilth method=POISSON", shell=True)
    subprocess.run("pset dmfilth srclist=@exclude.src.reg", shell=True)
    subprocess.run("pset dmfilth bkglist=@exclude.bg.reg", shell=True)
    subprocess.run("pset dmfilth randseed=0", shell=True)
    subprocess.run("dmfilth mode=h", shell=True) # remove regions and fill with
    # Poisson distribution of the background
    
    os.chdir("..") # move back up to the cluster directory
    
    subprocess.run("cp bin_2/broad_nps.fits SPA/broad_nps.fits", shell=True)
    
## STEP 7 - CONSTRAIN DATA TO REGION OF INTEREST (Rout_Mpc/SPA_box) ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmcopy.html
    
    subprocess.run("mkdir ROI_2", shell=True) # trim the images to the ROI
    subprocess.run("mkdir SPA_box", shell=True) # trim the images to the box
    
    subprocess.run("punlearn dmcopy", shell=True) # restore system defaults
    subprocess.run("dmcopy 'bin_2/broad_nps.fits[sky=region(roi_sky.reg)]' " +
                   "ROI_2/broad_nps_ROI.fits", shell=True)
    subprocess.run("dmcopy 'bin_2/background.fits[sky=region(roi_sky.reg)]' " +
                   "ROI_2/background_ROI.fits", shell=True)
    subprocess.run("dmcopy 'bin_2/broad_expmap.fits[sky=region(roi_sky.reg)]' " +
                   "ROI_2/expmap_ROI.fits", shell=True)
    
    subprocess.run("dmcopy 'SPA/broad_nps.fits[sky=region(box_sky.reg)]' " +
                   "SPA_box/broad_nps_box.fits", shell=True)
    subprocess.run("dmcopy 'SPA/background.fits[sky=region(box_sky.reg)]' " +
                   "SPA_box/background_box.fits", shell=True)
    subprocess.run("dmcopy 'SPA/broad_expmap.fits[sky=region(box_sky.reg)]' " +
                   "SPA_box/expmap_box.fits", shell=True)    
    
## STEP 8 - BACKGROUND SUBTRACTION ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmimgcalc.html
    
    subprocess.run("punlearn dmimgcalc", shell=True)    
    subprocess.run("dmimgcalc ROI_2/broad_nps_ROI.fits " +
                   "ROI_2/background_ROI.fits ROI_2/diffuse.fits sub",
                   shell=True) # subtract background of region of interest from
    # broad counts image, creating diffuse emission image
    
## STEP 9 - EXPOSURE CORRECT IMAGES ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmimgcalc.html
    
    subprocess.run("punlearn dmimgcalc", shell=True) # restore system defaults
    subprocess.run("dmimgcalc ROI_2/diffuse.fits ROI_2/expmap_ROI.fits " +
                   "ROI_2/final.fits div", shell=True) # divide diffuse emission
    # image by exposure map, thus creating final merged, background-subtracted,
    # exposure-corrected, cluster image
    
## STEP 10 - ADDITIONAL CLEANUP ##
    
    subprocess.run("rm -rf SPA", shell=True) # delete unnecessary files
    
## STEP 11 - RETURN TO THE DATA DIRECTORY ##

os.chdir("..") # go back to the data/ directory
