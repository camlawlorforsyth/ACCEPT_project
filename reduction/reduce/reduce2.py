import sys
import os
from math import *

#sources_mod.reg ciao&physical bk.reg
#The following is adapted from the Chandra imaging diffuse emission thread
clusterName = sys.argv[1]
bad = sys.argv[2]

os.chdir(clusterName)

f = open("data.txt", "r")
f.readline()
stat = clusterName + "," + f.readline().split(' ')[-1].strip() + "," + f.readline().split(' ')[-1].strip() + ","

f.close()

if bad == "d":
    os.chdir('expcor_mosaic')




    for i in range(0,2):
	    os.system("punlearn dmmakereg")
	    os.system("dmmakereg \"region(sources_mod.reg)\" sources_mod.fits")
	    os.system("dmlist sources_mod.fits cols")				#convert region file to fits format
	    os.system("mkdir sources")
	    os.system("punlearn roi")								#combine nearby sources
	    os.system("pset roi infile=sources_mod.fits")
	    os.system("pset roi outsrcfile=sources/src%d.fits")
	    os.system("pset roi bkgfactor=0.5")
	    #os.system("roi") 										#press enter through all of the prompts 
	    os.system("roi infile=sources_mod.fits fovregion=\"\" streakregion=\"\" outsrcfile=sources/src%d.fits radiusmode=mul bkgradius=3")

	    os.system("pget roi num_srcs")							#number of sources after roi combines nearby sources
	    os.system("dmlist sources_mod.fits counts")				#original number of sources
     
	    os.system("splitroi \"sources/src*.fits\" exclude")		#split region into source and backgroun
	    os.system("dmmakereg \"region(exclude.bg.reg)\" exclude.bg.fits")

	    os.system("punlearn dmfilth")
	    os.system("pset dmfilth infile=broad_thresh.img")		#remove regions and fill with poission dist of background
	    os.system("pset dmfilth outfile=broad_thresh_nps.fits")
	    os.system("pset dmfilth method=POISSON")
	    os.system("pset dmfilth srclist=@exclude.src.reg")
	    os.system("pset dmfilth bkglist=@exclude.bg.reg")
	    os.system("pset dmfilth randseed=0")
    #	os.system("dmfilth")									#enter through
	    os.system("dmfilth infile=broad_thresh.img outfile=broad_thresh_nps.fits method=POISSON srclist=@exclude.src.reg bkglist=@exclude.bg.reg randseed=0")

	    os.system("mv exclude.bg.fits exclude.bg.reg exclude.src.reg \sources")

	    os.chdir('../expcor_mosaic_2')

    #BIN=2 ONLY Then create a background image using the region of extraction found before (resaved as bk.reg),
    #only necessary for bin=2 save as ciao&physical.

    os.system("punlearn dmmakereg")
    os.system("dmmakereg \"region(bk.reg)\" background_reg.fits")
    os.system("dmlist background_reg.fits cols")

    os.system("mkdir sources_bk")
    os.system("punlearn roi")		
    os.system("pset roi infile=background_reg.fits")
    os.system("pset roi outsrcfile=sources_bk/src%d.fits")
    os.system("pset roi bkgfactor=0.5")
    #os.system("roi")
    os.system("roi infile=background_reg.fits fovregion=\"\" streakregion=\"\" outsrcfile=sources_bk/src%d.fits radiusmode=mul bkgradius=3")
    os.system("pget roi num_srcs")
    os.system("dmlist background_reg.fits counts")
	     
    os.system("splitroi \"sources_bk/src*.fits\" exclude")
    os.system("dmmakereg \"region(exclude.bg.reg)\" exclude.bg.fits")

    os.system("punlearn dmfilth")
    os.system("pset dmfilth infile=broad_thresh_nps.fits")
    os.system("pset dmfilth outfile=broad_thresh_bkg.fits")			
    os.system("pset dmfilth method=POISSON")
    os.system("pset dmfilth srclist=@exclude.src.reg")
    os.system("pset dmfilth bkglist=@exclude.bg.reg")
    os.system("pset dmfilth randseed=0")
    #os.system("dmfilth")
    os.system("dmfilth infile=broad_thresh_nps.fits outfile=broad_thresh_bkg.fits method=POISSON srclist=@exclude.src.reg bkglist=@exclude.bg.reg randseed=0")

    os.system("mv background_reg.fits bk.reg exclude.bg.fits exclude.bg.reg exclude.src.reg \sources_bk")

    #with the bin=2 and bin=0.5 images
    os.system("dmcopy \"broad_thresh_bkg.fits[sky=region(../ds9_fk.reg)]\" background.fits")		#only for bin=2	 
    os.system("dmcopy \"broad_thresh_nps.fits[sky=region(../ds9_fk.reg)]\" threshed_broad.fits")	#for bin=2 and bin=0.5
    os.chdir('../expcor_mosaic')
    os.system("dmcopy \"broad_thresh_nps.fits[sky=region(../ds9_fk.reg)]\" threshed_broad.fits")

    #make a bin=2 directory
    os.chdir('..')
    os.system("mkdir bin=2")
    os.chdir('bin=2')
    os.system("mkdir asymm")
    os.system("mkdir clumpy")
    os.system("mkdir UM")	#make a UM directory in the bin=2 directory
    os.chdir('../expcor_mosaic_2')
    os.system("mv background.fits ../bin=2") #mv background.fits to bin=2
    os.system("mv threshed_broad.fits ../bin=2")

    os.chdir('../bin=2')
    os.system("cp threshed_broad.fits UM")

    os.system("cp background.fits asymm")
    os.system("cp threshed_broad.fits asymm")
    os.system("cp background.fits clumpy")
    os.system("cp threshed_broad.fits clumpy")

    os.chdir('../expcor_mosaic')

    os.system("mv threshed_broad.fits ../ggm_combine")#move threshed in bin0.5 to ggm 
    os.chdir('..')
    os.system("cp ../reduce/asymm_calc.py bin=2/asymm")
    os.system("cp ../reduce/clumpy_calc.py bin=2/clumpy")
    #===============================================================================================#

    #================================== 6. APPLY GGM FILTER ========================================#
    #ONLY STEP NEEDS PYTHON-SEPARATE TERMINAL.
    #run through Gaussian_gradient_magnitude.py with bin=0.5 threshed_broad.img after point source removal, using the bright pixel from above as center
    #run ggm_combine to merge all ggm filtered images
    #adjust scaling lengths to match with region of extraction in input.yml. ie set second to last radius to radius of region of extraction 
    #(in image coord pixels) and keep halfing until zero

    #after copying /ggm_combine to your current directory
    #will need to be done in a terminal not running ciao
#    os.system("cp ../reduce/step6.py ggm_combine")
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
    os.system("rm temp.txt")

#    os.system("gnome-terminal -x python step6.py " + clusterName + " " + str(val))
    #everything below will now use only the bin=2 images
    #EVERYTHING IN IMAGE COORDS
    #===============================================================================================#


    #=============================== 7. MAKE UNSHARP MASKED IMAGE ==================================#
    #with the bin=2 images...in bin=2/UM
    os.chdir('../bin=2/UM')
    os.system("csmooth threshed_broad.fits clobber=yes outfile=smoothed_1.fits sclmap=\"\" sclmin=1 sclmax=1 sclmode=compute outsigfile=. outsclfile=. conmeth=fft conkerneltype=gauss sigmin=4 sigmax=5")
    os.system("csmooth threshed_broad.fits clobber=yes outfile=smoothed_30.fits sclmap=\"\" sclmin=30 sclmax=30 sclmode=compute outsigfile=. outsclfile=. conmeth=fft conkerneltype=gauss sigmin=4 sigmax=5")
    os.system("dmimgcalc smoothed_1.fits smoothed_30.fits unsharp.fits SUB")
    #play with a few different scalings of the larger value to get best results
    #good for seeing cavities
    #play around with 30/20 for artifacts
    #===============================================================================================#

    #================================== 8. ASYMMETRY PARAMTER =====================================#
    #rotate broad_thresh counts image and subtract from original. Divide square of the residual by square of the original image
    #Use same pixel from ggm filtering as center of rotation in image coords


    #Must be done in a terminal running ciao
    os.chdir('../asymm')

    #Need to input your own center of rotation
    rxc = str(val/4)
    ryc = str(val/4)
    #When prompted for rotated image enter: rot.fits
    #When prompted for background image enter: background.fits
    os.system("dmregrid2 threshed_broad.fits rot.fits resolution=0 theta=180 rotxcenter=" + rxc + " rotycenter=" + ryc)
    #num pixels = val/2
    os.system("python asymm_calc.py " + str(val/2) + " rot.fits background.fits threshed_broad.fits >> ../../data.txt")#outputs A

    #sum pixels in residual image, subtract the sum of the square of pixels in the background and divide by
    #twice the sum in the squared original to get the asymmetry A=(Io-Ir)^2/2Io^2
    #===============================================================================================#



    #================================= 9. CLUMPINESS PARAMETER =====================================#
    #Smooth a copy of threshed_broad.fits and subtract from original image to isolate high freq structure


    os.chdir('../clumpy')
    os.system("csmooth threshed_broad.fits clobber=yes outfile=smoothed.fits sclmap=\"\" sclmin=20 sclmax=20 sclmode=compute outsigfile=. outsclfile=. conmeth=fft conkerneltype=gauss sigmin=4 sigmax=5")
    os.system("dmcopy \"smoothed.fits[sky=region(../../ds9_fk.reg)]\" smoothed.fits clobber=yes")			#retrim to get rid of edge effects
    os.system("python clumpy_calc.py " + str(val/2) + " smoothed.fits background.fits threshed_broad.fits >> ../../data.txt")#sets all negative pixels to zero & outputs S
    #===============================================================================================#

    os.chdir('../..')
    #Cluster_name,R_out,D_A,A,S,C
    f = open("data.txt", "r")
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    asym = f.readline().strip()
    clump = f.readline().strip()
    f.close()
    stat = stat + asym + "," + clump +",\n"

    #================================ 10. CONCENTRATION PARAMETER ===================================#
    #isolate region of extraction 
    #determine radii that contain 20% and 80% of the total counts within the image
    #alter radius of region until it encompasses 20% and 80% of the total emission in ds9

    #Clumpiness = 5*log(r_80/r_20)		#needs to be calculated manually with ds9 unfortunately
    #===============================================================================================#
else:
    stat = stat +",,\n"
    

st = open("../chandrastats.txt", "a")
st.write(stat)
st.close()
