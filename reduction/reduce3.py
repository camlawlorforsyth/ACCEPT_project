# this script assumes Python 3.5 is in use

'''
For information regarding how this script is initialized, see the 'README.md'
file in reduction/README.md.

The calling code used in spa_process_all_data.py for this file, is of the form:
subprocess.run(['python','reduction/reduce3.py','1E_0657-56','0.296','4.413023451','11.64','4.89E+20','sufficient'])
                 argv[-]         argv[0]           argv[1]   argv[2]    argv[3]    argv[4]   argv[5]     argv[6]
'''

# imports
import os
import sys
import subprocess

import numpy as np

# constants
cluster = sys.argv[1] # the cluster name, as indicated
redshift = float(sys.argv[2]) # the given redshift
kpc_per_pixel = float(sys.argv[3]) # pixel size in kpc
kT = float(sys.argv[4]) # the cluster temperature in keV, from Cavagnolo+
nH = float(sys.argv[5]) # galactic column density in cm^(-2)
quality = sys.argv[6] # quality flag

## STEP 1 - MOVE INTO CLUSTER DIRECTORY ##

os.chdir(cluster)

## STEP 2 - PERFORM NEXT STEPS IF DATA IS OF SUFFICIENT QUALITY ##

if quality == "sufficient" :
    
## STEP 3-9 - COMPUTE SPA PARAMETERS FOR bin=2 IMAGE ##
    
    os.chdir("bin_2")
    
## STEP 3 - BACKGROUND SUBTRACTION USING STANDARD DEVIATION OF CAS REGION ##
    
# http://cxc.harvard.edu/ciao/ahelp/dmimgcalc.html    
    
    with open('bkg_sigma.txt', 'r') as file :
        bkg_sigma = float( file.read() )
    
    subprocess.run("punlearn dmimgcalc", shell=True) # restore system defaults
    subprocess.run("dmimgcalc infile=diffuse.fits op='imgout=img1-" +
                   str(bkg_sigma) + "' out='final_SPA.fits' mode=h",shell=True)
    
## STEP 4 - START HEASOFT TOOLS, CALCULATE K-CORRECTION ##
    
    subprocess.run("heainit", shell=True)
    subprocess.run("python ../../../soft/morph/K_nH_correction.py " +
                   "--kT " + str(kT) + " --nH " + str(nH) + " --Eobs 0.5-7.0" +
                   " --Ez 0.1-50.0 " + str(redshift) + " > K_correction.txt",
                   shell=True)
    
    with open('K_correction.txt', 'r') as file :
        K_corr = float( file.read() )
    
## STEP 5 - CALCULATE HUBBLE PARAMETER, SUFRACE BRIGHTNESS SCALING ##
    
    E_z = np.sqrt(0.3*((1 + redshift)**3) + 0.7) # normalized Hubble parameter,
    # see https://ui.adsabs.harvard.edu/abs/2008A%26A...483...35S/abstract
    
    norm = K_corr * kT * (E_z**3) / ((1 + redshift)**4)
    
## STEP 6 - EXPORT SHARED LIBRARIES ##
    
    subprocess.run("LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib" +
                   ":/home/cam/soft/heasoft-6.26/x86_64-pc-linux-gnu-libc2.12/lib",
                   shell=True)
    subprocess.run("export LD_LIBRARY_PATH", shell=True)
    
## STEP 7 - RUN MORPHOLOGY EXECUTABLE ##
    
    subprocess.run("../../../soft/morph/morphology" +
                   " --isoph-min-level " + str(2.0e-3*norm) +
                   " --isoph-max-level " + str(0.05*norm) +
                   " --num-isoph 5 --kpc " + str(kpc_per_pixel) +
                   " --peaky-flux " + str(0.0475*norm) +
                   " final_SPA.fits > morph.log", shell=True)
    
## STEP 8 - ANALYZE SPA OUTPUT ##
    
    # something to do with 'reduce2.R' script/use python to interpret results
    
    subprocess.run("../../../soft/morph/reduce2.R morph.log " +
                   str(redshift) + " > spa_params.txt", shell=True)
    
    with open('spa_params.txt', 'r') as file :
        relaxed = float( file.readline() ) # read 'relaxed' quality
        sym, peak, align = [float(val) for val in
                            file.readline().strip('\n').split(' ')]        
        covariance_matrix = file.readlines()
    
    sigmas = np.sqrt( np.diag(
                        [ [float(val) for val in line.strip('\n').split(' ')]
                         for line in covariance_matrix] ) )
    sym_err, peak_err, align_err = sigmas[0], sigmas[1], sigmas[2]
    
    os.chdir("..")
    
## STEP 9 - WRITE SPA PARAMETER VALUES TO TEXT FILE ##
    
    with open('../SPA_parameters_v1.txt', 'a') as file :
        file.write(cluster + "," + str(sym) + "," + str(sym_err) +
                   "," + str(peak) + "," + str(peak_err) +
                   "," + str(align) + "," + str(align_err) + "\n")
    
else:
    with open('../SPA_parameters_v1.txt', 'a') as file :
        file.write(cluster + ",,,,,,\n")

os.chdir("..") # go back to the data/ directory

## STEP 10 - FINAL CLEANUP ##

cmd = "rm -rf bin_2" # delete unnecessary files
subprocess.run(cmd, shell=True) # pass the cleanup command to the system

os.chdir("..") # go back to the data/ directory





'''

#================================== 6. APPLY GGM FILTER ========================================#
#ONLY STEP NEEDS PYTHON-SEPARATE TERMINAL.
#run through Gaussian_gradient_magnitude.py with bin=0.5 threshed_broad.img after point source removal, using the bright pixel from above as center
#run ggm_combine to merge all ggm filtered images
#adjust scaling lengths to match with region of extraction in input.yml. ie set second to last radius to radius of region of extraction 
#(in image coord pixels) and keep halfing until zero

#after copying /ggm_combine to your current directory
#will need to be done in a terminal not running ciao
    
    ## STEP 1 - CREATE INPUT FILE FOR GGM FILTERING ##
    
    os.chdir(cluster + "/ggm_combine")
    
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
    os.system("rm temp.txt")
    
    for i in range (0, 6):
	    os.system("python Gaussian_gradient_magnitude.py threshed_broad.fits " + cluster + "_" + str(2**i) + ".fits " + str(2**i))
    #os.system("ds9 -log threshed_broad.fits &")
    
    #Extract data for, and write, the input.yml file
    
    f = open("input.yml","w+")
    f.write("image:\n")
    f.write("        centre: [" + str(val) + "," + str(val) + "]\n")
    f.write("        outfilename: " + cluster + "_ggmfiltered.fits\n")
    
    f.write("data:\n")
    
    radii = "[0,"
    for i in range(0, 6):
        radii += str(int(val // 2**(5-i))) + ","
    radii += str(int(val // 1)) + "]\n"
    line = "weightrad: " + radii
    
    f.write("        - filename: " + cluster + "_" + str(2**0) + ".fits\n")
    f.write("          " + line)
    f.write("          weightvals: [1,1,0,0,0,0,0,0]\n")
    
    f.write("        - filename: " + cluster + "_" + str(2**1) + ".fits\n")
    f.write("          " + line)
    f.write("          weightvals: [2,2,2,0,0,0,0,0]\n")
    
    f.write("        - filename: " + cluster + "_" + str(2**2) + ".fits\n")
    f.write("          " + line)
    f.write("          weightvals: [0,4,4,4,0,0,0,0]\n")
    
    f.write("        - filename: " + cluster + "_" + str(2**3) + ".fits\n")
    f.write("          " + line)
    f.write("          weightvals: [0,0,8,8,8,0,0,0]\n")
    
    f.write("        - filename: " + cluster + "_" + str(2**4) + ".fits\n")
    f.write("          " + line)
    f.write("          weightvals: [0,0,0,10,10,10,0,0]\n")
    
    f.write("        - filename: " + cluster + "_" + str(2**5) + ".fits\n")
    f.write("          " + line)
    f.write("          weightvals: [0,0,0,0,10,10,10,10]\n")
    f.close()
    
    os.system("python uninteractive.py input.yml")
'''
