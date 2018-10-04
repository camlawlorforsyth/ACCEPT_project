# assumes Python 2.7 is installed

import sys
import os
from math import *

#to run this file from within your data folder, type in the terminal with ciao running:
 
#python reduce1.py [cluster_name] obsid1 obsid2 ... obsidN z R_out

#Assumes you run this from within your data folder, and that your data folder contains asymm_dream.py, clumpy_dream.py, ggm_combine

#this file will direct you through the reduction steps and process to obtain the CAS parameters
#for each cluster

#Record useful information in chandra_stats.txt

#================================== 1. GET DATA FROM ARCHIVE ==================================#
#You need to start CIAO first (after having installed it, of course). On the command line, type "ciao"

length = len(sys.argv)
z = float(sys.argv[length-2])
Rout = float(sys.argv[length-1])
clusterName = sys.argv[1]

os.system("mkdir " + clusterName) # create a new directory for the cluster
os.system("cp -r ggm_combine/ " + clusterName) # copy the ggm_combine/ directory to the new cluster directory
os.chdir(clusterName) # change directory to the cluster directory

cmd = "download_chandra_obsid " # download Chandra data as per http://cxc.harvard.edu/ciao/threads/archivedownload/
for i in range(2, length - 3):
	cmd += str(sys.argv[i]) + "," # creates a comma-separated list of the passed ObsIds from sys.arv(...)
cmd += str(sys.argv[length-3])
os.system("echo " + cmd)
os.system(cmd)
cmd = ""

#Gets the ObsIDs needed: multiple observations as chandra observs in ~50ks chunks. The location of the
#files have changed in May 2017 and old database is not able to download than use: --mirror 
#ftp://cda.cfa.harvard.edu/pub along with this command line to download the files from new location.
#===============================================================================================#
	
#================================ 2. REDUCE DATA TO LVL=2 ======================================#

for i in range(2, length-2):
	os.system("echo chandra_repro indir=" + sys.argv[i] + " outdir=" + sys.argv[i] + "/repro cleanup=no") 
	os.system("chandra_repro indir=" + sys.argv[i] + " outdir=" + sys.argv[i] + "/repro cleanup=no") 
	#the data to lvl2, stores in repro subdirectory

#Cleanup=no does not remove intermdeiate files
#More info about processing pipeline at 
#http://cxc.harvard.edu/ciao/threads/intro_data/index.html#processingversion
#===============================================================================================#

#============================ 3. CHANGE WCS AND MOSAIC IMAGES ==================================#
#Default bands parameter is broad: 0.5-7keV (or something)

os.system("punlearn reproject_obs flux_obs")

cmd = "reproject_obs "
for i in range(2, length-2):
	zero = ""
	num0 = 5-len(sys.argv[i])
	for n in range (0, num0):
		zero += "0"
	cmd += (sys.argv[i] + "/repro/acisf" + zero + sys.argv[i] + "_repro_evt2.fits,")
cmd = cmd[:-1]
cmd += " reproj/"
os.system(cmd)
os.system("echo " + cmd)
cmd=""

os.system("flux_obs reproj/ expcor_mosaic/ bin=0.5")		#for ggm filtering
os.system("flux_obs reproj/ expcor_mosaic_2/ bin=2") 		#to be used in CAS and unsharp masking
#===============================================================================================#

#============================= 4. DEFINE REGION OF EXTRACTION ==================================#
os.system("python ../reduce/calculator.py " + str(z) + " 70 0.3 0.7 " + str(Rout) + " > data.txt")

os.chdir('expcor_mosaic_2')
#os.system("ds9 -log broad_thresh.img &")
#open broad_thesh.img in ds9 and find central pixel defined by ACCEPT on maintable: find nearest brighest pixel to use as center

#(from ACCEPT datatable) to calculate angular radius of circular region of extraction

#create region of extraction and save (in fk5 coordinates) : radius of region typically ~15-20% of cluster Rvir

#name ds9_fk.reg in cluster directory
#===============================================================================================#

#================================= 5. REMOVE POINT SOURCES =====================================#
#Only sources very near to xray bright emission are really necessary to remove: only those in region of extraction
#Make region around point sources in bin=2 broad_thresh.img and save regions in ciao format with physical coords: 
#make sure region of extraction is not included

