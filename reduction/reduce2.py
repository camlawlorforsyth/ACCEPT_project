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
    
## STEPS 3-6 - REMOVE POINT SOURCES FOR bin=0.5 IMAGE ##
    
    os.chdir("bin")
    
## STEP 3 - CONVERT SOURCE LIST TO FITS FORMAT ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmmakereg.html
    
    subprocess.run("punlearn dmmakereg", shell=True) # restore system defaults
    subprocess.run("dmmakereg 'region(../sources_mod.reg)' sources_mod.fits " +
                   "wcsfile=broad_flux.fits", shell=True) # convert
    # the modified source list into FITS format
    
## STEP 4 - CREATE SOURCE AND BACKGROUND REGIONS ##
    
# http://cxc.harvard.edu/ciao/ahelp/roi.html
    
    subprocess.run("mkdir sources", shell=True)
    subprocess.run("punlearn roi", shell=True) # restore system defaults
    subprocess.run("pset roi infile=sources_mod.fits", shell=True)
    subprocess.run("pset roi outsrcfile=sources/src%d.fits", shell=True)
    subprocess.run("pset roi bkgfactor=0.5", shell=True)
    subprocess.run("roi infile=sources_mod.fits fovregion='' " +
                   "streakregion='' outsrcfile=sources/src%d.fits "+
                   "radiusmode=mul bkgradius=3", shell=True) # create source
    # and background regions for each source, combine nearby regions
    
## STEP 5 - SPLIT REGIONS INTO SOURCES AND BACKGROUNDS ##
    
# http://cxc.harvard.edu/ciao/ahelp/splitroi.html
    
    subprocess.run("splitroi 'sources/src*.fits' exclude", shell=True)
    
## STEP 6 - FILL IN HOLES ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmfilth.html
    
    subprocess.run("punlearn dmfilth", shell=True) # restore system defaults
    subprocess.run("pset dmfilth infile=broad_flux.fits", shell=True)
    subprocess.run("pset dmfilth outfile=diffuse.fits", shell=True)    
    subprocess.run("pset dmfilth method=POISSON", shell=True)
    subprocess.run("pset dmfilth srclist=@exclude.src.reg", shell=True)
    subprocess.run("pset dmfilth bkglist=@exclude.bg.reg", shell=True)
    subprocess.run("pset dmfilth randseed=0", shell=True)
    subprocess.run("dmfilth infile=broad_flux.fits " +
                   "outfile=diffuse.fits method=POISSON " +
                   "srclist=@exclude.src.reg bkglist=@exclude.bg.reg",
                   shell=True) # remove regions and fill with Poisson
    # distribution of the background
    
    os.chdir("..") # move back up to the cluster directory
    
## STEP 7 - REPEAT STEPS 3-6 FOR bin=2 IMAGE ##
    
    os.chdir("bin_2")
    
    subprocess.run("punlearn dmmakereg", shell=True)
    subprocess.run("dmmakereg 'region(../sources_mod.reg)' sources_mod.fits " +
                   "wcsfile=broad_flux.fits", shell=True)
    
    subprocess.run("mkdir sources", shell=True)
    subprocess.run("punlearn roi", shell=True)
    subprocess.run("pset roi infile=sources_mod.fits", shell=True)
    subprocess.run("pset roi outsrcfile=sources/src%d.fits", shell=True)
    subprocess.run("pset roi bkgfactor=0.5", shell=True)
    subprocess.run("roi infile=sources_mod.fits fovregion='' " +
                   "streakregion='' outsrcfile=sources/src%d.fits "+
                   "radiusmode=mul bkgradius=3", shell=True)
    
    subprocess.run("splitroi 'sources/src*.fits' exclude", shell=True)
    
    subprocess.run("punlearn dmfilth", shell=True)
    subprocess.run("pset dmfilth infile=broad_flux.fits", shell=True)
    subprocess.run("pset dmfilth outfile=diffuse.fits", shell=True)    
    subprocess.run("pset dmfilth method=POISSON", shell=True)
    subprocess.run("pset dmfilth srclist=@exclude.src.reg", shell=True)
    subprocess.run("pset dmfilth bkglist=@exclude.bg.reg", shell=True)
    subprocess.run("pset dmfilth randseed=0", shell=True)
    subprocess.run("dmfilth infile=broad_flux.fits " +
                   "outfile=diffuse.fits method=POISSON " +
                   "srclist=@exclude.src.reg bkglist=@exclude.bg.reg",
                   shell=True)
    
    os.chdir("..")
    
## STEP 8 - CONSTRAIN DATA TO REGION OF INTEREST (Rout_Mpc) ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmcopy.html
    
    subprocess.run("mkdir ROI", shell=True) # trim the images to the ROI
    subprocess.run("mkdir ROI_2", shell=True)
    
    subprocess.run("punlearn dmcopy", shell=True) # restore system defaults
    subprocess.run("dmcopy 'bin/diffuse.fits[sky=region(ds9_fk5.reg)]' " +
                   "ROI/diffuse.fits", shell=True)
    subprocess.run("dmcopy 'bin/broad_flux_bkg.fits[sky=region(ds9_fk5.reg)]' "+
                   "ROI/background.fits", shell=True)
    
    subprocess.run("dmcopy 'bin_2/diffuse.fits[sky=region(ds9_fk5.reg)]' " +
                   "ROI_2/diffuse.fits", shell=True)
    subprocess.run("dmcopy 'bin_2/broad_flux_bkg.fits[sky=region(ds9_fk5.reg)]' "+
                   "ROI_2/background.fits", shell=True)
    
## STEP 9 - BACKGROUND SUBTRACTION ##
    
    subprocess.run("punlearn dmimgcalc", shell=True)
    subprocess.run("dmimgcalc ROI/diffuse.fits ROI/background.fits " +
                   "ROI/final.fits sub", shell=True) # subtract background of
    # region of interest from diffuse emission image, thus creating final
    # merged, exposure-corrected, background-subtracted cluster image
    
    subprocess.run("punlearn dmimgcalc", shell=True)
    subprocess.run("dmimgcalc ROI_2/diffuse.fits ROI_2/background.fits " +
                   "ROI_2/final.fits sub", shell=True)
    
## STEP 10 - COMPUTE CONCENTRATION PARAMETER ##
    
# could alternatively use ecf_calc to determine radii for 20% and 80% of counts
# http://cxc.harvard.edu/ciao/ahelp/ecf_calc.html
    
    os.chdir("ROI_2") # move into the bin=2 directory
    concen,concen_err = concen_calc.main('final.fits',RA,Dec,redshift,Rout_Mpc)
    
## STEP 11 - COMPUTE ASYMMETRY PARAMETER ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmregrid.html
# http://cxc.harvard.edu/ciao/ahelp/dmregrid2.html
    
    science = fits.open('final.fits') # open the final science image
    image = science[0].data # get the science data that will be used
    science.close()
    
    x_length = image.shape[1] # images might not be perfectly square
    y_length = image.shape[0]
    
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
    subprocess.run("csmooth final.fits outfile=smoothed.fits " +
                   "outsigfile=clumpy_sig.fits outsclfile=clumpy_scl.fits " +
                   "sclmode=compute conmeth=fft conkerneltype=gauss " +
                   "sclmin=" + str(scale) + " sclmax=" + str(scale) +
                   " sigmin=4 sigmax=5", shell=True)
    
#    subprocess.run("punlearn dmcopy", shell=True)
#    subprocess.run("dmcopy 'smoothed.fits[sky=region(../ds9_fk5.reg)]' " +
#                   "smoothed.fits") # retrim to get rid of edge effects
    
    clumpy, clumpy_err = clumpy_calc.main('final.fits', 'smoothed.fits')
    
## STEP 13 - CREATE UNSHARP MASK (UM) IMAGE ##
    
# http://cxc.harvard.edu/ciao/gallery/smooth.html
# http://cxc.harvard.edu/ciao/ahelp/aconvolve.html
# http://cxc.harvard.edu/ciao/ahelp/csmooth.html
# http://cxc.harvard.edu/ciao/ahelp/dmimgcalc.html
    
    subprocess.run("punlearn csmooth", shell=True)
    subprocess.run("csmooth final.fits outfile=smoothed_3.fits " +
                   "outsigfile=um3_sig.fits outsclfile=um3_scl.fits " +
                   "sclmode=compute conmeth=fft conkerneltype=gauss " +
                   "sclmin=3 sclmax=3 sigmin=4 sigmax=5", shell=True)
    subprocess.run("csmooth final.fits outfile=smoothed_30.fits " +
                   "outsigfile=um30_sig.fits outsclfile=um30_scl.fits " +
                   "sclmode=compute conmeth=fft conkerneltype=gauss " +
                   "sclmin=30 sclmax=30 sigmin=4 sigmax=5", shell=True)
    
    subprocess.run("punlearn dmimgcalc", shell=True)
    subprocess.run("dmimgcalc smoothed_3.fits smoothed_30.fits " +
                   "unsharp_mask.fits sub", shell=True)
    
    os.chdir("..")
    
## STEP 14 - CREATE GAUSSIAN GRADIENT MAGNITUDE (GGM) IMAGE ##
    
# http://cxc.harvard.edu/ciao/gallery/smooth.html
# https://github.com/jeremysanders/ggm
    
    os.chdir("ROI") # move into the bin=0.5 directory
    
    science = fits.open('final.fits') # open the final science image
    image = science[0].data # get the science data that will be used
    science.close()
    
    x_length = image.shape[1] # images might not be perfectly square
    y_length = image.shape[0]
    
    for sigma in [1,2,4,8,16,32] :
        outfilename = cluster + "_" + str(sigma) + ".fits"
        subprocess.run(['python',
                        '../../reduction/ggm/gaussian_gradient_magnitude.py',
                        'final.fits', outfilename, str(sigma)])
    
    file = open('input.yml','w') # open for writing
    file.write("image:\n")
    file.write("        centre: [" + str(x_length/2) + "," + str(y_length/2) + "]\n")
    file.write("        outfilename: " + cluster + "_ggm.fits\n")
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
    
    subprocess.run(['python','uninteractive.py','input.yml'])
    
    os.chdir("..")
    
## STEP 15 - WRITE CAS PARAMETER VALUES TO TEXT FILE ##
    
    with open('../CAS_parameters_v1.txt', 'a') as file :
        file.write(cluster + "," + str(concen) + "," + str(concen_err) +
                   "," + str(asymm) + "," + str(asymm_err) +
                   "," + str(clumpy) + "," + str(clumpy_err) + "\n" )
    
else:
    with open('../CAS_parameters_v1.txt', 'a') as file :
        file.write(cluster + ",,,,,,\n")

## STEP 16 - ADDITIONAL CLEANUP ##

cmd = "rm -rf bin" # delete unnecessary files
subprocess.run(cmd, shell=True) # pass the cleanup command to the system

os.chdir("..") # go back to the data/ directory


    # start here again, June 25, 2019
    
    
'''
    
# old code, adapt for above
    #BIN=2 ONLY Then create a background image using the region of extraction found before (resaved as bk.reg),
    #only necessary for bin=2 save as ciao&physical.
    
    subprocess.run("mv background_reg.fits bk.reg exclude.bg.fits exclude.bg.reg exclude.src.reg \sources_bk")
    
    #with the bin=2 and bin=0.5 images
    subprocess.run("dmcopy 'broad_thresh_bkg.fits[sky=region(../ds9_fk5.reg)]' background.fits")		#only for bin=2	 
    subprocess.run("dmcopy 'broad_thresh_nps.fits[sky=region(../ds9_fk5.reg)]' threshed_broad.fits")	#for bin=2 and bin=0.5
    os.chdir('../merged')
    subprocess.run("dmcopy 'broad_thresh_nps.fits[sky=region(../ds9_fk5.reg)]' threshed_broad.fits")
    
    #make a bin=2 directory
    os.chdir('..')
    subprocess.run("mkdir bin=2")
    os.chdir('bin=2')
    subprocess.run("mkdir concen")
    subprocess.run("mkdir asymm")
    subprocess.run("mkdir clumpy")
    subprocess.run("mkdir UM")	#make a UM directory in the bin=2 directory
    os.chdir('../merged_2')
    subprocess.run("mv background.fits ../bin=2") #mv background.fits to bin=2
    subprocess.run("mv threshed_broad.fits ../bin=2")
    
    os.chdir('../bin=2')
    subprocess.run("cp threshed_broad.fits UM")
    
    subprocess.run("cp threshed_broad.fits concen")
    subprocess.run("cp background.fits asymm")
    subprocess.run("cp threshed_broad.fits asymm")
    subprocess.run("cp background.fits clumpy")
    subprocess.run("cp threshed_broad.fits clumpy")
    
    os.chdir('../merged')
    
    subprocess.run("mv threshed_broad.fits ../ggm_combine")#move threshed in bin0.5 to ggm 
    os.chdir('..')
    subprocess.run("cp ../reduce/concen_calc.py bin=2/concen")
    subprocess.run("cp ../reduce/asymm_calc.py bin=2/asymm")
    subprocess.run("cp ../reduce/clumpy_calc.py bin=2/clumpy")
    #========================================================
    
    #================================== 6. APPLY GGM FILTER =
    #ONLY STEP NEEDS PYTHON-SEPARATE TERMINAL.
    #run through Gaussian_gradient_magnitude.py with bin=0.5 threshed_broad.img after point source removal,
    # using the bright pixel from above as center
    #run ggm_combine to merge all ggm filtered images
    #adjust scaling lengths to match with region of extraction in input.yml. ie set second to last radius to radius of region of extraction 
    #(in image coord pixels) and keep halfing until zero
    
    #after copying /ggm_combine to your current directory
    #will need to be done in a terminal not running ciao
#    subprocess.run("cp ../reduce/step6.py ggm_combine")
    
    # Use same pixel from asymmetry param rotation as center of rotation in image coords
    
    os.chdir('ggm_combine')
    
    f = open("threshed_broad.fits", "r")
    q = open("temp.txt","w+")
    q.write(f.read(1000))
    f.close()
    q.close()
    q = open("temp.txt","r")
    content = q.readline() #get threshed broad size data + more
    q.close()
    
    contents = content.split("NAXIS") 
    content = contents[2][4:]
    contents = content.split('/')
    content = contents[0].strip()
    
    val = int(content)
    val = val // 2
    subprocess.run("rm temp.txt")
    
#    subprocess.run("gnome-terminal -x python step6.py " + cluster + " " + str(val))
    
#    subprocess.run("dmcopy 'merged/broad_flux.img[sky=region(ds9_fk5.reg)]' " +
#                   "ROI/broad_flux_ROI.fits", shell=True)
#    subprocess.run("dmcopy 'merged/broad_thresh.img[sky=region(ds9_fk5.reg)]' " +
#                   "ROI/broad_thresh_ROI.fits", shell=True)
#    subprocess.run("dmcopy 'merged/broad_thresh.expmap[sky=region(ds9_fk5.reg)]' " +
#                   "ROI/broad_thresh_expmap_ROI.fits", shell=True)
#    subprocess.run("dmcopy 'merged/broad_thresh.psfmap[sky=region(ds9_fk5.reg)]' " +
#                   "ROI/broad_thresh_psfmap_ROI.fits", shell=True)
#	
#    subprocess.run("dmcopy 'merged_2/broad_flux.img[sky=region(ds9_fk5.reg)]' " +
#                   "ROI_2/broad_flux_ROI.fits", shell=True)
#    subprocess.run("dmcopy 'merged_2/broad_thresh.img[sky=region(ds9_fk5.reg)]' " +
#                   "ROI_2/broad_thresh_ROI.fits", shell=True)
#    subprocess.run("dmcopy 'merged_2/broad_thresh.expmap[sky=region(ds9_fk5.reg)]' " +
#                   "ROI_2/broad_thresh_expmap_ROI.fits", shell=True)
#    subprocess.run("dmcopy 'merged_2/broad_thresh.psfmap[sky=region(ds9_fk5.reg)]' " +
#                   "ROI_2/broad_thresh_psfmap_ROI.fits", shell=True)

'''
