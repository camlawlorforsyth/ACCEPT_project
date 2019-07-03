# this script assumes Python 3.5 is in use

'''
For information regarding how this script is initialized, see the 'README.md'
file in reduction/README.md.

The calling code used in get_all_data.py for this file, is of the form:
subprocess.run(['python','reduction/reduce1.py','1E_0657-56','104.6234458','-55.94438611','0.296','1.1945','11.64','5.19e+20','554','3184','4984','4985','4986','5355','5356','5357','5358','5361'])
                 argv[-]         argv[0]           argv[1]      argv[2]        argv[3]    argv[4]  argv[5]  argv[6]  argv[7] argv[8] ... argv[N]
'''

# imports
import os
import sys
import subprocess

import check_coords
import merged_count
import ROI_count

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

cmd = "chandra_repro '*' outdir=''" # reprocess all ObsIDs, do not save
                                    # intermediate files
subprocess.run(cmd, shell=True) # pass the reprocess command to the system

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
cmd = "reproject_obs '*/repro/*evt2*' reproj/" # reproject all ObsIDs
subprocess.run(cmd, shell=True)

subprocess.run("punlearn flux_obs", shell=True)  # restore system defaults
cmd = ("flux_obs 'reproj/*reproj_evt.fits' merged/ bin=0.5 units=time " + 
       "psfecf=0.393") # psfmerge=expmap doesn't work # for GGM filtering
subprocess.run(cmd, shell=True)
cmd = ("flux_obs 'reproj/*reproj_evt.fits' merged_2/ bin=2 units=time " +
       "psfecf=0.393") # for CAS analysis and unsharp mask
subprocess.run(cmd, shell=True)

## STEP 5 - CHECK ALL MERGED FILES ARE PRESENT ##

merged_count.main(cluster, length-8) # prints to data/issues.txt

## STEP 6 - DEFINE REGION OF INTEREST, MEASURE TOTAL COUNTS, SAVE ROI ##

# http://cxc.harvard.edu/ciao/ahelp/dmmakereg.html

quality = ROI_count.main('merged_2/broad_flux.img', RA, Dec, redshift,Rout_Mpc)
    # determine if cluster has sufficient data
    # if data is sufficient, create ds9_fk5.reg file, and bk.reg file

with open('../cas_process_all_data.py', 'a') as file :
    file.write("subprocess.run(['python','reduction/reduce2.py','" + cluster +
               "','" + str(RA) + "','" + str(Dec) + "','" + str(redshift) +
               "','" + str(Rout_Mpc) + "','" + str(kT) + "','" + str(nH) +
               "','" + quality + "'])\n" ) # append quality flag to
                                           # cas_process_all_data.py
    
## STEP 7 - PERFORM NEXT STEPS IF DATA IS OF SUFFICIENT QUALITY ##

if quality == "sufficient" :
    
## STEP 8 - RENAME AND COPY NECESSARY FILES ##

# http://cxc.harvard.edu/ciao/ahelp/dmcopy.html
    
    subprocess.run("mkdir bin", shell=True)
    subprocess.run("mkdir bin_2", shell=True)
    
    subprocess.run("punlearn dmcopy", shell=True)
    subprocess.run("dmcopy 'merged/broad_flux.img' bin/broad_flux.fits",
                   shell=True)
    subprocess.run("dmcopy 'merged/broad_thresh.img' bin/broad_thresh.fits",
                   shell=True)
    subprocess.run("dmcopy 'merged/broad_thresh.expmap' " +
                   "bin/broad_thresh_expmap.fits", shell=True)
    subprocess.run("dmcopy 'merged/broad_thresh.psfmap' " +
                   "bin/broad_thresh_psfmap.fits", shell=True)
	
    subprocess.run("dmcopy 'merged_2/broad_flux.img' bin_2/broad_flux.fits",
                   shell=True)
    subprocess.run("dmcopy 'merged_2/broad_thresh.img' bin_2/broad_thresh.fits",
                   shell=True)
    subprocess.run("dmcopy 'merged_2/broad_thresh.expmap' " +
                   "bin_2/broad_thresh_expmap.fits", shell=True)
    subprocess.run("dmcopy 'merged_2/broad_thresh.psfmap' " +
                   "bin_2/broad_thresh_psfmap.fits", shell=True)

## STEP 9 - DETECT POINT SOURCES ##
    
# http://cxc.harvard.edu/ciao/guides/esa.html
# http://cxc.harvard.edu/ciao/threads/detect_overview/
# http://cxc.harvard.edu/ciao/threads/wavdetect/
# http://cxc.harvard.edu/ciao/threads/wavdetect_merged/
# http://cxc.harvard.edu/ciao/ahelp/wavdetect.html
	
    subprocess.run("mkdir sources", shell=True)
    
    subprocess.run("punlearn wavdetect", shell=True) # restore system defaults
    subprocess.run("pset wavdetect infile=bin/broad_thresh.fits",
                   shell=True) # wavdetect will not work with fluxed images
    subprocess.run("pset wavdetect psffile=bin/broad_thresh_psfmap.fits",
                   shell=True)
    subprocess.run("pset wavdetect expfile=bin/broad_thresh_expmap.fits",
                   shell=True)
    subprocess.run("pset wavdetect scales='1 2 4 8 16'", shell=True)
    subprocess.run("pset wavdetect outfile=sources/broad_thresh_src.fits",
                   shell=True)
    subprocess.run("pset wavdetect scellfile=sources/broad_thresh_scell.fits",
                   shell=True)
    subprocess.run("pset wavdetect imagefile=sources/broad_thresh_recon.fits",
                   shell=True)
    subprocess.run("pset wavdetect defnbkgfile=sources/broad_thresh_nbkgd.fits",
                   shell=True)
    subprocess.run("pset wavdetect regfile=sources.reg", shell=True)
    subprocess.run("pset wavdetect ellsigma=4", shell=True)
    subprocess.run("wavdetect infile=bin/broad_thresh.fits " +
                   "outfile=sources/broad_thresh_src.fits " +
                   "scellfile=sources/broad_thresh_scell.fits " +
                   "imagefile=sources/broad_thresh_recon.fits " +
                   "defnbkgfile=sources/broad_thresh_nbkgd.fits " +
                   "scales='1 2 4 8 16' " +
                   "psffile=bin/broad_thresh_psfmap.fits", shell=True)
    
## STEPS 10-13 - CREATE BACKGROUND REGION FOR bin=0.5 REGION OF INTEREST ##
    
    os.chdir("bin")
    
## STEP 10 - CONVERT SOURCE LIST TO FITS FORMAT ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmmakereg.html
    
    subprocess.run("punlearn dmmakereg", shell=True) # restore system defaults
    subprocess.run("dmmakereg 'region(../bk.reg)' bkg_reg.fits " +
                   "wcsfile=broad_flux.fits", shell=True) # convert
    # the modified source list into FITS format
    
## STEP 11 - CREATE SOURCE AND BACKGROUND REGIONS ##
    
# http://cxc.harvard.edu/ciao/ahelp/roi.html
    
    subprocess.run("mkdir sources_bk", shell=True)
    subprocess.run("punlearn roi", shell=True) # restore system defaults
    subprocess.run("pset roi infile=bkg_reg.fits", shell=True)
    subprocess.run("pset roi outsrcfile=sources_bk/src%d.fits", shell=True)
    subprocess.run("pset roi bkgfactor=0.5", shell=True)
    subprocess.run("roi infile=bkg_reg.fits fovregion='' " +
                   "streakregion='' outsrcfile=sources_bk/src%d.fits " +
                   "radiusmode=mul bkgradius=3", shell=True) # create source
    # and background regions for each source, combine nearby regions
    
## STEP 12 - SPLIT REGIONS INTO SOURCES AND BACKGROUNDS ##
    
# http://cxc.harvard.edu/ciao/ahelp/splitroi.html
    
    subprocess.run("splitroi 'sources_bk/src*.fits' exclude", shell=True)
    
## STEP 13 - FILL IN HOLES ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmfilth.html
    
    subprocess.run("punlearn dmfilth", shell=True)
    subprocess.run("pset dmfilth infile=broad_flux.fits", shell=True)
    subprocess.run("pset dmfilth outfile=broad_flux_bkg.fits", shell=True)
    subprocess.run("pset dmfilth method=POISSON", shell=True)
    subprocess.run("pset dmfilth srclist=@exclude.src.reg", shell=True)
    subprocess.run("pset dmfilth bkglist=@exclude.bg.reg", shell=True)
    subprocess.run("pset dmfilth randseed=0", shell=True)
    subprocess.run("dmfilth infile=broad_flux.fits " +
                   "outfile=broad_flux_bkg.fits method=POISSON " +
                   "srclist=@exclude.src.reg bkglist=@exclude.bg.reg",
                   shell=True) # remove regions and fill with Poisson
    # distribution of the background
    
    os.chdir("..") # move back up to the cluster directory
    
## STEP 14 - REPEAT STEPS 10-13 FOR bin=2 REGION OF INTEREST ##
    
    os.chdir("bin_2")
    
    subprocess.run("punlearn dmmakereg", shell=True)
    subprocess.run("dmmakereg 'region(../bk.reg)' bkg_reg.fits " +
                   "wcsfile=broad_flux.fits", shell=True)
    
    subprocess.run("mkdir sources_bk", shell=True)
    subprocess.run("punlearn roi", shell=True)
    subprocess.run("pset roi infile=bkg_reg.fits", shell=True)
    subprocess.run("pset roi outsrcfile=sources_bk/src%d.fits", shell=True)
    subprocess.run("pset roi bkgfactor=0.5", shell=True)
    subprocess.run("roi infile=bkg_reg.fits fovregion='' " +
                   "streakregion='' outsrcfile=sources_bk/src%d.fits " +
                   "radiusmode=mul bkgradius=3", shell=True)
    
    subprocess.run("splitroi 'sources_bk/src*.fits' exclude", shell=True)
    
    subprocess.run("punlearn dmfilth", shell=True)
    subprocess.run("pset dmfilth infile=broad_flux.fits", shell=True)
    subprocess.run("pset dmfilth outfile=broad_flux_bkg.fits", shell=True)
    subprocess.run("pset dmfilth method=POISSON", shell=True)
    subprocess.run("pset dmfilth srclist=@exclude.src.reg", shell=True)
    subprocess.run("pset dmfilth bkglist=@exclude.bg.reg", shell=True)
    subprocess.run("pset dmfilth randseed=0", shell=True)
    subprocess.run("dmfilth infile=broad_flux.fits " +
                   "outfile=broad_flux_bkg.fits method=POISSON " +
                   "srclist=@exclude.src.reg bkglist=@exclude.bg.reg",
                   shell=True)
    
## STEP 15 - FIND STANDARD DEVIATION OF bin=2 BACKGROUND REGION ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmstat.html
    
    subprocess.run("punlearn dmstat", shell=True)
    subprocess.run("dmstat 'broad_flux_bkg.fits[sky=region(../bk.reg)]' " +
                   "centroid=no verbose=0", shell=True)
    subprocess.run("pget dmstat out_sigma > bkg_sigma.txt", shell=True)
    
    os.chdir("..")
    
## STEP 16 - CHECK COORDINATES OF REGION FILES ##
    
    check_coords.main(cluster) # prints to data/issues.txt
    
## STEP 17 - CLEANUP ##

cmd = "rm -rf reproj merged merged_2" # delete unnecessary ObsID files,
                                      # intermediate files
for i in range(8, length) : # creates a space-separated list of the ObsIDs
    cmd += " " + str(sys.argv[i])

subprocess.run(cmd, shell=True) # pass the cleanup command to the system

os.chdir("..") # go back to the data/ directory

'''
the sources in sources.reg can now be viewed in ds9 and any spurious detections
can be deleted. now save this file as 'sources_mod.reg' in CIAO+physical

ds9 ROI_2/broad_flux_ROI.fits -cmap bb -scale log -region sources.reg
'''
