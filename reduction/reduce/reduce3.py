import os
import sys

#================================== 6. APPLY GGM FILTER ========================================#
#ONLY STEP NEEDS PYTHON-SEPARATE TERMINAL.
#run through Gaussian_gradient_magnitude.py with bin=0.5 threshed_broad.img after point source removal, using the bright pixel from above as center
#run ggm_combine to merge all ggm filtered images
#adjust scaling lengths to match with region of extraction in input.yml. ie set second to last radius to radius of region of extraction 
#(in image coord pixels) and keep halfing until zero

#after copying /ggm_combine to your current directory
#will need to be done in a terminal not running ciao

clusterName = sys.argv[1]
bad = sys.argv[2]

if bad == "d":
    
    os.chdir(clusterName + "/ggm_combine")
 
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
	    os.system("python Gaussian_gradient_magnitude.py threshed_broad.fits " + clusterName + "_" + str(2**i) + ".fits " + str(2**i))
    #os.system("ds9 -log threshed_broad.fits &")

    #Extract data for, and write, the input.yml file

    f = open("input.yml","w+")
    f.write("image:\n")
    f.write("        centre: [" + str(val) + "," + str(val) + "]\n")
    f.write("        outfilename: " + clusterName + "_ggmfiltered.fits\n")


    over2 = "[0,"
    for i in range(0, 6):
        over2 += str(int(val // 2**(5-i))) + ","
    over2 += str(int(val // 1)) + "]\n"
    line = "weightrad: " + over2

    f.write("data:\n")

    f.write("        - filename: " + clusterName + "_" + str(2**0) + ".fits\n")
    f.write("          " + line)
    f.write("          weightvals: [1,1,0,0,0,0,0,0]\n")

    f.write("        - filename: " + clusterName + "_" + str(2**1) + ".fits\n")
    f.write("          " + line)
    f.write("          weightvals: [2,2,2,0,0,0,0,0]\n")

    f.write("        - filename: " + clusterName + "_" + str(2**2) + ".fits\n")
    f.write("          " + line)
    f.write("          weightvals: [0,4,4,4,0,0,0,0]\n")

    f.write("        - filename: " + clusterName + "_" + str(2**3) + ".fits\n")
    f.write("          " + line)
    f.write("          weightvals: [0,0,8,8,8,0,0,0]\n")

    f.write("        - filename: " + clusterName + "_" + str(2**4) + ".fits\n")
    f.write("          " + line)
    f.write("          weightvals: [0,0,0,10,10,10,0,0]\n")

    f.write("        - filename: " + clusterName + "_" + str(2**5) + ".fits\n")
    f.write("          " + line)
    f.write("          weightvals: [0,0,0,0,10,10,10,10]\n")
    f.close()

    os.system("python uninteractive.py input.yml")
