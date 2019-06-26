# this script assumes Python 3.5 is in use

'''
For information regarding how this script is initialized, see the 'README.md'
file in reduction/README.md.

The calling code used in ggm_all_data.py for this file, is of the form:
subprocess.run(['python','reduction/reduce3.py','1E_0657-56','sufficient'])
                 argv[-]         argv[0]           argv[1]      argv[2]
'''

# imports
import os
import sys
import subprocess

# constants
cluster = sys.argv[1] # the cluster name, as indicated
quality = sys.argv[2] # quality flag

#================================== 6. APPLY GGM FILTER ========================================#
#ONLY STEP NEEDS PYTHON-SEPARATE TERMINAL.
#run through Gaussian_gradient_magnitude.py with bin=0.5 threshed_broad.img after point source removal, using the bright pixel from above as center
#run ggm_combine to merge all ggm filtered images
#adjust scaling lengths to match with region of extraction in input.yml. ie set second to last radius to radius of region of extraction 
#(in image coord pixels) and keep halfing until zero

#after copying /ggm_combine to your current directory
#will need to be done in a terminal not running ciao

if quality == "sufficient" :
    
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

