# this script assumes Python 3.5 is in use

'''
For information regarding how this script is initialized, see the 'README.md'
file in reduction/README.md.

The calling code used in get_all_data.py for this file, is of the form:
subprocess.run(['python','reduction/reduce1.py','1E_0657-56','104.6234458','-55.94438611','0.296','1.1945','11.64','4.89E+20','554','3184','4984','4985','4986','5355','5356','5357','5358','5361'])
                 argv[-]         argv[0]           argv[1]      argv[2]        argv[3]    argv[4]  argv[5]  argv[6]  argv[7] argv[8] ... argv[N]
'''

# imports
import os
import sys
import subprocess

import roi_count

# constants
length = len(sys.argv) # length = 18 for the example above
cluster = sys.argv[1] # the cluster name, as indicated
RA = float(sys.argv[2]) # the right ascension of the cluster
Dec = float(sys.argv[3]) # the declination of the cluster
redshift = float(sys.argv[4]) # the given redshift
Rout_Mpc = float(sys.argv[5]) # the maximum outer radius used by Cavagnolo+
kT = float(sys.argv[6]) # the cluster temperature in keV, from Cavagnolo+
nH = float(sys.argv[7]) # galactic column density in cm^(-2)

## STEP 1 - CREATE CLUSTER DIRECTORY AND MOVE INTO IT ##

# http://cxc.harvard.edu/ciao/threads/all.html
# http://cxc.harvard.edu/ciao/threads/imag.html
# http://cxc.harvard.edu/ciao/threads/diffuse_emission/

subprocess.run("mkdir " + cluster, shell=True) # create a new directory for the
                                               # cluster
os.chdir(cluster) # change to the cluster directory

## STEP 2 - OBTAIN DATA FROM THE CHANDRA DATA ARCHIVE ##

# http://cxc.harvard.edu/ciao/threads/intro_data/
# http://cxc.harvard.edu/ciao/threads/archivedownload/
# http://cxc.harvard.edu/ciao/ahelp/download_chandra_obsid.html

cmd = "download_chandra_obsid " # download Chandra data
for i in range(8, length-1) :
    cmd += str(sys.argv[i]) + "," # creates a comma-separated list of the
                                  # passed ObsIDs
cmd += str(sys.argv[length-1]) + " -q" # append the last ObsID
subprocess.run(cmd, shell=True) # pass the download command to the system

## STEP 3 - REDUCE/REPROCESS DATA TO LEVEL=2 ##

# http://cxc.harvard.edu/ciao/threads/createL2/
# http://cxc.harvard.edu/ciao/ahelp/chandra_repro.html

subprocess.run("chandra_repro '*' outdir='' set_ardlib=no", shell=True)
    # reprocess all ObsIDs, do not save intermediate files

## STEP 4 - REPROJECT AND COMBINE ##

# http://cxc.harvard.edu/ciao/threads/merge_all/
# http://cxc.harvard.edu/ciao/threads/reproject_image/
# http://cxc.harvard.edu/ciao/threads/combine/
# http://cxc.harvard.edu/ciao/ahelp/punlearn.html
# http://cxc.harvard.edu/ciao/ahelp/merge_obs.html
# http://cxc.harvard.edu/ciao/ahelp/reproject_obs.html
# http://cxc.harvard.edu/ciao/ahelp/flux_obs.html

subprocess.run("punlearn reproject_obs", shell=True) # restore system default
    # parameter values
subprocess.run("reproject_obs '*/repro/*evt2*' reproj/", shell=True) # reproject
    # all ObsIDs

subprocess.run("punlearn flux_obs", shell=True)  # restore system defaults
subprocess.run("flux_obs 'reproj/*reproj_evt.fits' merged_2/ bin=2 " +
               "units=time psfecf=0.393", shell=True) # for CAS analysis and UM
subprocess.run("flux_obs 'reproj/*reproj_evt.fits' SPA_temp/ bin=2 units=area",
               shell=True) # for SPA, requires exposure map with units of cm^2

## STEP 5 - DEFINE REGION OF INTEREST, MEASURE TOTAL COUNTS, SAVE ROI ##

# http://cxc.harvard.edu/ciao/ahelp/dmmakereg.html

quality = roi_count.main('merged_2/broad_flux.img', RA, Dec, redshift, Rout_Mpc)
    # determine if cluster has sufficient data
    # if data is sufficient, create roi_sky.reg file, roi_phys.reg file,
    # box_sky.reg file, and box_phys.reg file

with open('../reduce_all_data.py', 'a') as file :
    file.write("subprocess.run(['python','reduction/reduce2.py','" + cluster +
               "','" + str(RA) + "','" + str(Dec) + "','" + str(redshift) +
               "','" + str(Rout_Mpc) + "','" + str(kT) + "','" + str(nH) +
               "','" + quality + "'])\n" ) # append quality flag to
                                           # reduce_all_data.py

## STEP 6 - PERFORM NEXT STEPS IF DATA IS OF SUFFICIENT QUALITY ##

if quality == "sufficient" :
    
## STEP 7 - RENAME AND COPY NECESSARY FILES ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmcopy.html
    
    subprocess.run("mkdir bin_2", shell=True)
    subprocess.run("mkdir SPA", shell=True)
	
    subprocess.run("punlearn dmcopy", shell=True)
    subprocess.run("dmcopy 'merged_2/broad_thresh.img' " +
                   "bin_2/broad_thresh.fits", shell=True)
    subprocess.run("dmcopy 'merged_2/broad_thresh.expmap' " +
                   "bin_2/broad_expmap.fits", shell=True)
    subprocess.run("dmcopy 'merged_2/broad_thresh.psfmap' " +
                   "bin_2/broad_psfmap.fits", shell=True)
    
    subprocess.run("dmcopy 'SPA_temp/broad_thresh.img' " +
                   "SPA/broad_thresh.fits", shell=True)
    subprocess.run("dmcopy 'SPA_temp/broad_thresh.expmap' " +
                   "SPA/broad_expmap.fits", shell=True)
    
## STEP 8 - DETECT POINT SOURCES ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmcopy.html
# http://cxc.harvard.edu/ciao/guides/esa.html
# http://cxc.harvard.edu/ciao/threads/detect_overview/
# http://cxc.harvard.edu/ciao/threads/wavdetect/
# http://cxc.harvard.edu/ciao/threads/wavdetect_merged/
# http://cxc.harvard.edu/ciao/ahelp/wavdetect.html
    
    subprocess.run("mkdir sources", shell=True)
    
    subprocess.run("punlearn dmcopy", shell=True)
    subprocess.run("dmcopy 'bin_2/broad_thresh.fits[sky=region(box_sky.reg)]' " +
                   "sources/broad.fits", shell=True)
    subprocess.run("dmcopy 'bin_2/broad_expmap.fits[sky=region(box_sky.reg)]' " +
                   "sources/expmap.fits", shell=True)
    subprocess.run("dmcopy 'bin_2/broad_psfmap.fits[sky=region(box_sky.reg)]' " +
                   "sources/psfmap.fits", shell=True)
    
    subprocess.run("punlearn wavdetect", shell=True) # restore system defaults
    subprocess.run("pset wavdetect infile=sources/broad.fits", shell=True)
    subprocess.run("pset wavdetect psffile=sources/psfmap.fits", shell=True)
    subprocess.run("pset wavdetect expfile=sources/expmap.fits", shell=True)
    subprocess.run("pset wavdetect scales='1 2 4 8 16'", shell=True)
    subprocess.run("pset wavdetect outfile=sources/broad_src.fits", shell=True)
    subprocess.run("pset wavdetect scellfile=sources/broad_scell.fits", shell=True)
    subprocess.run("pset wavdetect imagefile=sources/broad_recon.fits", shell=True)
    subprocess.run("pset wavdetect defnbkgfile=sources/broad_nbkgd.fits", shell=True)
    subprocess.run("pset wavdetect regfile=sources.reg", shell=True)
    subprocess.run("pset wavdetect ellsigma=4", shell=True)
    subprocess.run("pset wavdetect clobber=yes", shell=True)
    subprocess.run("wavdetect mode=h", shell=True) # wavdetect will not work
    # with fluxed images
    
    subprocess.run("rm -rf sources", shell=True) # delete unnecessary files
    
## STEPS 9-12 - CREATE BACKGROUND REGION FOR bin=2 REGION OF INTEREST ##
    
    os.chdir("bin_2") # move into the bin_2 directory
    
## STEP 9 - CONVERT SOURCE LIST TO FITS FORMAT ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmmakereg.html
    
    subprocess.run("punlearn dmmakereg", shell=True) # restore system defaults
    subprocess.run("dmmakereg 'region(../roi_phys.reg)' bkg_reg.fits " +
                   "wcsfile=broad_thresh.fits", shell=True) # convert the
    # modified source list into FITS format
    
## STEP 10 - CREATE SOURCE AND BACKGROUND REGIONS ##
    
# http://cxc.harvard.edu/ciao/ahelp/roi.html
    
    subprocess.run("mkdir sources_bk", shell=True)
    subprocess.run("punlearn roi", shell=True) # restore system defaults
    subprocess.run("pset roi infile=bkg_reg.fits", shell=True)
    subprocess.run("pset roi outsrcfile=sources_bk/src%d.fits", shell=True)
    subprocess.run("pset roi bkgfactor=0.5", shell=True)
    subprocess.run("pset roi fovregion=''", shell=True)
    subprocess.run("pset roi streakregion=''", shell=True)
    subprocess.run("pset roi radiusmode=mul", shell=True)
    subprocess.run("pset roi bkgradius=3", shell=True)
    subprocess.run("roi mode=h", shell=True) # create source and background
    # regions for each source, combine nearby regions
    
## STEP 11 - SPLIT REGIONS INTO SOURCES AND BACKGROUNDS ##
    
# http://cxc.harvard.edu/ciao/ahelp/splitroi.html
    
    subprocess.run("splitroi 'sources_bk/src*.fits' exclude", shell=True)
    
## STEP 12 - FILL IN HOLES ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmfilth.html
    
    subprocess.run("punlearn dmfilth", shell=True)
    subprocess.run("pset dmfilth infile=broad_thresh.fits", shell=True)
    subprocess.run("pset dmfilth outfile=background.fits", shell=True)
    subprocess.run("pset dmfilth method=POISSON", shell=True)
    subprocess.run("pset dmfilth srclist=@exclude.src.reg", shell=True)
    subprocess.run("pset dmfilth bkglist=@exclude.bg.reg", shell=True)
    subprocess.run("pset dmfilth randseed=0", shell=True)
    subprocess.run("dmfilth mode=h", shell=True) # remove regions and fill with
    # Poisson distribution of the background
    
    subprocess.run("mv exclude.bg.reg exclude.src.reg bkg_reg.fits sources_bk",
                   shell=True)
    
    os.chdir("..") # move back up to the cluster directory
    
## STEP 13 - REPEAT STEPS 9-12 FOR bin=2 SPA REGION ##
    
    os.chdir("SPA")
    
    subprocess.run("punlearn dmmakereg", shell=True)
    subprocess.run("dmmakereg 'region(../box_phys.reg)' bkg_reg.fits " +
                   "wcsfile=broad_thresh.fits", shell=True)
    
    subprocess.run("mkdir sources_bk", shell=True)
    subprocess.run("punlearn roi", shell=True)
    subprocess.run("pset roi infile=bkg_reg.fits", shell=True)
    subprocess.run("pset roi outsrcfile=sources_bk/src%d.fits", shell=True)
    subprocess.run("pset roi bkgfactor=0.5", shell=True)
    subprocess.run("pset roi fovregion=''", shell=True)
    subprocess.run("pset roi streakregion=''", shell=True)
    subprocess.run("pset roi radiusmode=mul", shell=True)
    subprocess.run("pset roi bkgradius=3", shell=True)
    subprocess.run("roi mode=h", shell=True)
    
    subprocess.run("splitroi 'sources_bk/src*.fits' exclude", shell=True)
    
    subprocess.run("punlearn dmfilth", shell=True)
    subprocess.run("pset dmfilth infile=broad_thresh.fits", shell=True)
    subprocess.run("pset dmfilth outfile=background.fits", shell=True)
    subprocess.run("pset dmfilth method=POISSON", shell=True)
    subprocess.run("pset dmfilth srclist=@exclude.src.reg", shell=True)
    subprocess.run("pset dmfilth bkglist=@exclude.bg.reg", shell=True)
    subprocess.run("pset dmfilth randseed=0", shell=True)
    subprocess.run("dmfilth mode=h", shell=True)
    
    subprocess.run("mv exclude.bg.reg exclude.src.reg bkg_reg.fits sources_bk",
                   shell=True)
    
    os.chdir("..")
    
## STEP 14 - INITIAL CLEANUP ##

cmd = "rm -rf reproj merged_2 SPA_temp" # delete unnecessary files
for i in range(8, length) : # creates a space-separated list of the ObsIDs
    cmd += " " + str(sys.argv[i])
subprocess.run(cmd, shell=True) # pass the cleanup command to the system

## STEP 15 - RETURN TO THE DATA DIRECTORY ##

os.chdir("..") # go back to the data/ directory
