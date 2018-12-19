# this script assumes Python 2.7 is in use

from pycrates import read_file # allows reading, writing, and changing FITS files. Based on Crates, provided with CIAO
                               # Can alternatively use 'from astropy.io import fits' and then 'fits.open(...)', but further
                               # modifications to the code would then be necessary
import numpy as np
import math
import sys

'''
The calling code used in reduce2.py for this file, is of the form:
python asymm_calc.py threshed_broad.fits smoothed.fits
argv[-]    argv[0]         argv[1]        argv[2]
'''

if len(sys.argv) == 5 :
	A = int(sys.argv[1]) # the one size dimension of the image, where the image is assumed to be square
	S = sys.argv[2] # the smoothed image
	B = sys.argv[3] # the background image
	T = sys.argv[4] # the original science image
else : # this should only be necessary if not using the automated reduction scripts
	print "Input the number of pixels (ie. one dimension of the square image):"
	A = input('')
	print "Input the path to the smoothed image:"
	S = raw_input('')
	print "Input the path to the background image (if there is no background image, enter 'no'):"
	B = raw_input('')
	print "Input the path to the original science image:"
	T = raw_input('')

img_s = read_file(S) # read the smoothed image
img_t = read_file(T) # read the science image
orig_pix_vals_s = img_s.get_image().values # get the pixel values from the smoothed image
orig_pix_vals_t = img_t.get_image().values # get the pixel values from the original science image

'''
# Michael's original code, suspected to be incorrect

for x in range(0, A) : # adjust upper limit to the image pixel size of the image
	for y in range(0, A) :
		a = (orig_pix_vals_t[x,y] - orig_pix_vals_s[x,y])
		if a < 0 :
			orig_pix_vals_s[x,y] = 0 
		else :
			orig_pix_vals_s[x,y] = a

s, b, t = 0, 0, 0 # initial values

if B == 'no' :
	for x in range(0, A) :						
		for y in range(0, A) :
			s += orig_pix_vals_s[x,y] 
			t += orig_pix_vals_t[x,y]
else :
	img_b = read_file(B)
	orig_pix_vals_b = img_b.get_image().values
	for x in range(0, A) :						
		for y in range(0, A) :
			s += orig_pix_vals_s[x,y]
			b += orig_pix_vals_b[x,y] 
			t += orig_pix_vals_t[x,y]

print (s-b)/t
'''

num = 0
denom = 0

for x in range(0, A) : # loop for every pixel in the square image
    for y in range(0, A) :
        if B == 'no' : # if there is no background image
            diff = orig_pix_vals_t[x,y] - orig_pix_vals_s[x,y]
            if diff < 0 :
                num += 0
            else :
                num += diff
            denom += orig_pix_vals_t[x,y]
        else :
            img_b = read_file(B) # read the background image
            orig_pix_vals_b = img_b.get_image().values # get the pixel values from the background image
            diff = (orig_pix_vals_t[x,y] - orig_pix_vals_b[x,y]) - orig_pix_vals_s[x,y]
            if diff < 0 :
                num += 0
            else :
                num += diff
            denom += orig_pix_vals_t[x,y] - orig_pix_vals_b[x,y]

print num/denom
