# this script assumes Python 3.5 is in use

'''
For information regarding how this script is initialized, see the 'README.md'
file in reduction/README.md.

The calling code used in spa_process_all_data.py for this file, is of the form:
subprocess.run(['python','reduction/reduce4.py','1E_0657-56','0.296','4.34241507547309','11.64','4.89E+20','sufficient'])
                 argv[-]         argv[0]           argv[1]   argv[2]       argv[3]      argv[4]   argv[5]     argv[6]
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
    
## STEP 3-8 - COMPUTE SPA PARAMETERS FOR bin=2 IMAGE ##
    
    os.chdir("SPA_box") # move into the SPA_box directory
    
## STEP 3 - CALCULATE AND WRITE K-CORRECTION ##
    
    subprocess.run("python ~/soft/morph/K_nH_correction.py " +
                   "--kT " + str(kT) + " --nH " + str(nH) + " --Eobs 0.5-7.0" +
                   " --Ez 0.1-50.0 " + str(redshift) + " > K_correction.txt",
                   shell=True)
    
    with open('K_correction.txt', 'r') as file :
        K_corr = float( file.read() )
    
## STEP 4 - CALCULATE HUBBLE PARAMETER, SUFRACE BRIGHTNESS SCALING ##
    
# https://ui.adsabs.harvard.edu/abs/2008A%26A...483...35S/abstract
# https://ui.adsabs.harvard.edu/abs/2015MNRAS.449..199M/abstract
    
    E_z = np.sqrt(0.3*((1 + redshift)**3) + 0.7) # normalized Hubble parameter 
    
    norm = K_corr * kT * (E_z**3) / ((1 + redshift)**4) # 'f_s' in Mantz et al.
    
    with open('morph.log', 'w') as file :
        file.write("SB scaling factor = " + str(norm) + "\n")
    
## STEP 5 - RUN MORPHOLOGY EXECUTABLE ##
    
    cmd = ("~/soft/morph/morphology broad_nps_box.fits --obnoxious" +
           " --isoph-min-level " + str(2.0e-3*norm) +
           " --isoph-max-level " + str(0.05*norm) +
           " --num-isoph 5 --kpc " + str(kpc_per_pixel) +
           " --peaky-flux " + str(0.0475*norm) +
           " --bg-file background_box.fits 1 0 --expmap expmap_box.fits" +
           " >> morph.log")
    subprocess.run(cmd, shell=True) # run morphology executable once
    
    cmd = ("~/soft/morph/morphology broad_nps_box.fits --quiet" +
           " --isoph-min-level " + str(2.0e-3*norm) +
           " --isoph-max-level " + str(0.05*norm) +
           " --num-isoph 5 --kpc " + str(kpc_per_pixel) +
           " --peaky-flux " + str(0.0475*norm) +
           " --bg-file background_box.fits 1 0 --expmap expmap_box.fits" +
           " --boot 100 > morph_boot.dat")
    subprocess.run(cmd, shell=True) # bootstrap to estimate uncertainties
    
## STEP 6 - ANALYZE SPA OUTPUT ##
    
    subprocess.run("~/soft/morph/reduce2.R morph.log " + str(redshift) +
                   " morph_boot.dat > spa_params.txt", shell=True)
    
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
    
## STEP 7 - WRITE SPA PARAMETER VALUES TO TEXT FILE ##
    
    with open('../SPA_parameters_v2.txt', 'a') as file :
        file.write(cluster + "," + str(sym) + "," + str(sym_err) +
                   "," + str(peak) + "," + str(peak_err) +
                   "," + str(align) + "," + str(align_err) + "\n")
    
else:
    with open('../SPA_parameters_v2.txt', 'a') as file :
        file.write(cluster + ",,,,,,\n")

## STEP 8 - RETURN TO THE DATA DIRECTORY ##

os.chdir("..") # go back to the data/ directory
