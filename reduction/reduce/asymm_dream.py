# this script assumes Python 2.7 is in use

from pycrates import read_file # allows reading, writing, and changing FITS files. Based on Crates, provided with CIAO
                               # Can alternatively use 'from astropy.io import fits' and then 'fits.open(...)', but further
                               # modifications to the code would then be necessary
import numpy as np
import math
import sys

'''
The calling code used in reduce2.py for this file, is of the form:
python asymm_dream.py dimension rot.fits background.fits threshed_broad.fits
argv[-]    argv[0]     argv[1]   argv[2]     argv[3]          argv[4]
'''

if len(sys.argv) == 5 :
	A = int(sys.argv[1]) # the one size dimension of the image, where the image is assumed to be square
	R = sys.argv[2] # the rotated image
	B = sys.argv[3] # the background image
	T = sys.argv[4] # the original science image
else : # this should only be necessary if not using the automated reduction scripts
	print "Input the number of pixels (ie. one dimension of the square image):"
	A = input('')
	print "Input the path to the rotated image:"
	R = raw_input('')
	print "Input the path to the background image (if there is no background image, enter 'no'):"
	B = raw_input('')
	print "Input the path to the original science image:"
	T = raw_input('')

img_r = read_file(R) # read the rotated image
img_t = read_file(T) # read the science image
orig_pix_vals_r = img_r.get_image().values # get the pixel values from the rotated image
orig_pix_vals_t = img_t.get_image().values # get the pixel values from the original science image

'''
# Michael's original code, suspected to be incorrect

r, b, t = 0, 0, 0 # inital values

if B == 'no' : # if there is no background image
	for x in range(0, A) : # loop for every pixel in the square image
		for y in range(0, A) :
			r += ( orig_pix_vals_t[x,y] - orig_pix_vals_r[x,y] )**2
			t += 2*( ( orig_pix_vals_t[x,y] )**2 )
else :
	img_b = read_file(B)
	orig_pix_vals_b = img_b.get_image().values
	for x in range(0, A) :
		for y in range(0, A) :
			r += ( orig_pix_vals_t[x,y] - orig_pix_vals_r[x,y] )**2
			b += ( orig_pix_vals_b[x,y] )**2
			t += 2*( ( orig_pix_vals_t[x,y] )**2 )

print (r-b)/t
'''

num = 0
denom = 0

for x in range(0, A) : # loop for every pixel in the square image
    for y in range(0, A) :
        if B == 'no' : # if there is no background image
            num += ( orig_pix_vals_t[x,y] - orig_pix_vals_r[x,y] )**2
            denom += 2*( ( orig_pix_vals_t[x,y] )**2 )
        else:
            img_b = read_file(B) # read the background image
            orig_pix_vals_b = img_b.get_image().values # get the pixel values from the background image
            num += ( orig_pix_vals_t[x,y] - orig_pix_vals_b[x,y] - orig_pix_vals_r[x,y] )**2
            denom += 2*( ( orig_pix_vals_t[x,y] - orig_pix_vals_b[x,y] )**2 )

print num/denom
