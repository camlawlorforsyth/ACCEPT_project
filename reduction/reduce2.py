# this script assumes Python 3.5 is in use

'''
For information regarding how this script is initialized, see the 'README.md'
file in reduction/README.md.

The calling code used in cas_process_all_data.py for this file, is of the form:
subprocess.run(['python','reduction/reduce2.py','1E_0657-56','104.6234458','-55.94438611','0.296','1.1945','11.64','4.89E+20','sufficient'])
                 argv[-]         argv[0]           argv[1]      argv[2]        argv[3]    argv[4]  argv[5]  argv[6]  argv[7]     argv[8]
'''

# imports
import os
import sys
import subprocess

import concen_calc
import asymm_calc
import clumpy_calc
import save_images

from astropy.cosmology import FlatLambdaCDM
from astropy.io import fits
import astropy.units as u

# constants
cluster = sys.argv[1] # the cluster name, as indicated
RA = float(sys.argv[2]) # the right ascension of the cluster
Dec = float(sys.argv[3]) # the declination of the cluster
redshift = float(sys.argv[4]) # the given redshift
Rout_Mpc = float(sys.argv[5]) # the maximum outer radius used by Cavagnolo+
kT = float(sys.argv[6]) # the cluster temperature in keV, from Cavagnolo+
nH = float(sys.argv[7]) # galactic column density in cm^(-2)
quality = sys.argv[8] # quality flag

cosmo = FlatLambdaCDM(H0 = 70, Om0 = 0.3) # specify the cosmology being used
pixel_scale = 0.984*u.arcsec # 1 pixel = 0.984" for Chandra
scale_of_interest = 15*u.kpc # bubbles and cavities are often found on such
                             # scales. See paper for more information

kpc_per_pixel = 1/(cosmo.arcsec_per_kpc_proper(redshift).value)

with open('spa_process_all_data.py', 'a') as file :
    file.write("subprocess.run(['python','reduction/reduce3.py','" + cluster +
               "','" + str(redshift) + "','" + str(kpc_per_pixel) +
               "','" + str(kT) + "','" + str(nH) + "','" + quality + 
               "'])\n" ) # append quality flag to spa_process_all_data.p

## STEP 1 - MOVE INTO CLUSTER DIRECTORY ##

os.chdir(cluster)

## STEP 2 - PERFORM NEXT STEPS IF DATA IS OF SUFFICIENT QUALITY ##

if quality == "sufficient" :
    
## STEPS 3-6 - REMOVE POINT SOURCES FOR bin=2 IMAGE ##
    
    os.chdir("bin_2")
    
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
    
## STEP 10 - COMPUTE CONCENTRATION PARAMETER ##
    
    os.chdir("ROI_2") # move into the bin=2 directory
    concen, concen_err = concen_calc.main('final.fits', RA, Dec, redshift, Rout_Mpc)
    
## STEP 11 - COMPUTE ASYMMETRY PARAMETER ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmregrid2.html
    
    science = fits.open('final.fits')
    header = science[0].header
    science.close()
    
    x_length, y_length = header['NAXIS1'], header['NAXIS2']
    
    subprocess.run("punlearn dmregrid2", shell=True) # restore system defaults
    subprocess.run("dmregrid2 final.fits rot.fits resolution=0 theta=180" +
                   " rotxcenter=" + str(x_length/2) +
                   " rotycenter=" + str(y_length/2), shell=True)
    
    asymm, asymm_err = asymm_calc.main('final.fits', 'rot.fits')
    
## STEP 12 - COMPUTE CLUMPINESS PARAMETER ##
    
# http://cxc.harvard.edu/ciao/ahelp/csmooth.html
# http://cxc.harvard.edu/ciao/ahelp/dmimgcalc.html
    
    scale = (cosmo.arcsec_per_kpc_proper(redshift) *
             scale_of_interest/pixel_scale).value # determine number of pixels
             # that correspond to 15 kpc in projected size, to highlight
             # AGN driven features like bubbles and cavities
    
    subprocess.run("punlearn csmooth", shell=True) # restore system defaults
    subprocess.run("csmooth final.fits sclmap='' outfile=smoothed.fits " +
                   "outsigfile=clumpy_sig.fits outsclfile=clumpy_scl.fits " +
                   "sclmode=compute conmeth=fft conkerneltype=gauss " +
                   "sclmin=" + str(scale) + " sclmax=" + str(scale) +
                   " sigmin=4 sigmax=5", shell=True)
    
    clumpy, clumpy_err = clumpy_calc.main('final.fits', 'smoothed.fits')
    
## STEP 13 - CREATE UNSHARP MASK (UM) IMAGE ##
    
# http://cxc.harvard.edu/ciao/gallery/smooth.html
# http://cxc.harvard.edu/ciao/ahelp/csmooth.html
# http://cxc.harvard.edu/ciao/ahelp/dmimgcalc.html
    
    subprocess.run("punlearn csmooth", shell=True)
    subprocess.run("csmooth final.fits sclmap='' outfile=smoothed_3.fits " +
                   "outsigfile=um3_sig.fits outsclfile=um3_scl.fits " +
                   "sclmode=compute conmeth=fft conkerneltype=gauss " +
                   "sclmin=3 sclmax=3 sigmin=4 sigmax=5", shell=True)
    subprocess.run("csmooth final.fits sclmap='' outfile=smoothed_30.fits " +
                   "outsigfile=um30_sig.fits outsclfile=um30_scl.fits " +
                   "sclmode=compute conmeth=fft conkerneltype=gauss " +
                   "sclmin=30 sclmax=30 sigmin=4 sigmax=5", shell=True)
    
    subprocess.run("punlearn dmimgcalc", shell=True)
    subprocess.run("dmimgcalc smoothed_3.fits smoothed_30.fits " +
                   "unsharp_mask.fits sub", shell=True)
    
    os.chdir("..")
    
## STEP 14 - COPY AND REBIN bin=2 FINAL IMAGE FILE TO bin=0.5 DIRECTORY ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmregrid.html
    
    subprocess.run("mkdir ggm", shell=True)
    
    science = fits.open("ROI_2/final.fits") # open the final science image
    header = science[0].header # get the science header that will be used
    science.close()
    
    xhi, yhi = header['NAXIS1'], header['NAXIS2'] # images might not be square
    
    subprocess.run("punlearn dmregrid", shell=True) # restore system defaults
    subprocess.run("dmregrid 'ROI_2/final.fits' ggm/final.fits '1:" +
                   str(xhi) + ":0.25,1:" + str(yhi) + ":0.25' rotangle=0 " +
                   "rotxcenter=0 rotycenter=0 xoffset=0 yoffset=0 npts=0",
                   shell=True) # for GGM filtering
    subprocess.run("rm ~/cxcds_param4/dmregrid.par", shell=True)
    
## STEP 15 - CREATE GAUSSIAN GRADIENT MAGNITUDE (GGM) IMAGE ##
    
# http://cxc.harvard.edu/ciao/gallery/smooth.html
# https://github.com/jeremysanders/ggm
# https://github.com/camlawlorforsyth/ggm
    
    os.chdir("ggm") # move into the bin=0.5 directory
    
    science = fits.open('final.fits')
    header = science[0].header
    science.close()
    
    x_length, y_length = header['NAXIS1'], header['NAXIS2']
    
    for sigma in [1,2,4,8,16,32] :
        outfilename = cluster + "_" + str(sigma) + ".fits"
        subprocess.run(['python',
                        '../../reduction/ggm/gaussian_gradient_magnitude.py',
                        'final.fits', outfilename, str(sigma)])
    
    file = open('input.yml','w') # open for writing
    file.write("image:\n")
    file.write("        centre: [" + str(x_length/2) + "," + str(y_length/2) + "]\n")
    file.write("        outfilename: ggm.fits\n")
    file.write("data:\n")
    
    dim = min(x_length/2, y_length/2)
    
    radii = "[0,"
    for sigma in [32,16,8,4,2,1] :
        radii += str( int(dim/sigma) ) + ","
    radii += str( int(dim) ) + "]\n"
    
    file.write("        - filename: " + cluster + "_1.fits\n")
    file.write("          weightrad: " + radii)
    file.write("          weightvals: [1,1,0,0,0,0,0,0]\n")
    
    file.write("        - filename: " + cluster + "_2.fits\n")
    file.write("          weightrad: " + radii)
    file.write("          weightvals: [2,2,2,0,0,0,0,0]\n")
    
    file.write("        - filename: " + cluster + "_4.fits\n")
    file.write("          weightrad: " + radii)
    file.write("          weightvals: [0,4,4,4,0,0,0,0]\n")
    
    file.write("        - filename: " + cluster + "_8.fits\n")
    file.write("          weightrad: " + radii)
    file.write("          weightvals: [0,0,8,8,8,0,0,0]\n")
    
    file.write("        - filename: " + cluster + "_16.fits\n")
    file.write("          weightrad: " + radii)
    file.write("          weightvals: [0,0,0,10,10,10,0,0]\n")
    
    file.write("        - filename: " + cluster + "_32.fits\n")
    file.write("          weightrad: " + radii)
    file.write("          weightvals: [0,0,0,0,10,10,10,10]\n")
    
    file.close()
    
    subprocess.run(['python','../../reduction/ggm/ggm_combine/interactive.py',
                    'input.yml'])
    
    subprocess.run("rm -f " + cluster + "* tmp*", shell=True)
    
    os.chdir("..")
    
## STEP 16 - SAVE IMAGES TO PDF ##
    
    save_images.main('ROI_2/final.fits', 'ggm/ggm.fits',
                     'ROI_2/unsharp_mask.fits', cluster)
    
## STEP 17 - ADDITIONAL CLEANUP ##
    
    subprocess.run("rm -rf bin_2 SPA", shell=True) # delete unnecessary files
    
## STEP 18 - WRITE CAS PARAMETER VALUES TO TEXT FILE ##
    
    with open('../CAS_parameters_v1.txt', 'a') as file :
        file.write(cluster + "," + str(concen) + "," + str(concen_err) +
                   "," + str(asymm) + "," + str(asymm_err) +
                   "," + str(clumpy) + "," + str(clumpy_err) + "\n" )
    
else:
    with open('../CAS_parameters_v1.txt', 'a') as file :
        file.write(cluster + ",,,,,,\n")

## STEP 19 - RETURN TO THE DATA DIRECTORY ##

os.chdir("..") # go back to the data/ directory
