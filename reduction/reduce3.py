# this script assumes Python 3.5 is in use

'''
For information regarding how this script is initialized, see the 'README.md'
file in reduction/README.md.

The calling code used in cas_process_all_data.py for this file, is of the form:
subprocess.run(['python','reduction/reduce3.py','1E_0657-56','3.454298987842798','sufficient'])
                 argv[-]         argv[0]           argv[1]         argv[2]          argv[3]
'''

# imports
import os
import sys
import subprocess

import concen_calc
import asymm_calc
import clumpy_calc
import um_creation
import save_images

from astropy.io import fits

# constants
cluster = sys.argv[1] # the cluster name, as indicated
scale = float(sys.argv[2]) # number of pixels that correspond to 15 kpc
quality = sys.argv[3] # quality flag

## STEP 1 - MOVE INTO CLUSTER DIRECTORY ##

os.chdir(cluster)

## STEP 2 - PERFORM NEXT STEPS IF DATA IS OF SUFFICIENT QUALITY ##

if quality == "sufficient" :

## STEPS 3-5 - COMPUTE CAS PARAMETERS FOR bin=2 IMAGE ##
    
    os.chdir("ROI_2") # move into the ROI_2 directory
    
## STEP 3 - COMPUTE CONCENTRATION PARAMETER ##
    
    concen, concen_err = concen_calc.main('final.fits')
    
## STEP 4 - COMPUTE ASYMMETRY PARAMETER ##
    
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.rot90.html
    
    asymm, asymm_err = asymm_calc.main('final.fits')
    
## STEP 5 - COMPUTE CLUMPINESS PARAMETER ##
    
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter.html
    
    clumpy, clumpy_err = clumpy_calc.main('final.fits', scale)
    
## STEP 6 - CREATE UNSHARP MASK (UM) IMAGE ##
    
# http://cxc.harvard.edu/ciao/gallery/smooth.html
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter.html
    
    um_creation.main('final.fits', scale)
        
    os.chdir("..")
    
## STEP 7 - COPY AND REBIN bin=2 FINAL IMAGE FILE TO bin=0.5 DIRECTORY ##
    
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
    
## STEP 8 - CREATE GAUSSIAN GRADIENT MAGNITUDE (GGM) IMAGE ##
    
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
    
## STEP 9 - SAVE IMAGES TO PDF ##
    
    save_images.main('ROI_2/final.fits', 'ggm/ggm.fits',
                     'ROI_2/unsharp_mask.fits', cluster)

## STEP 10 - WRITE CAS PARAMETER VALUES TO TEXT FILE ##
    
    with open('../CAS_parameters_v2.txt', 'a') as file :
        file.write(cluster + "," + str(concen) + "," + str(concen_err) +
                   "," + str(asymm) + "," + str(asymm_err) +
                   "," + str(clumpy) + "," + str(clumpy_err) + "\n" )
    
else:
    with open('../CAS_parameters_v2.txt', 'a') as file :
        file.write(cluster + ",,,,,,\n")
        
## STEP 11 - RETURN TO THE DATA DIRECTORY ##

os.chdir("..") # go back to the data/ directory
