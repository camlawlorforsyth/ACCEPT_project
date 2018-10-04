from pycrates import read_file
import numpy as np
import math
import sys

if len(sys.argv) == 5:
	A = int(sys.argv[1])
	H = sys.argv[2]
	B = sys.argv[3]
	T = sys.argv[4]
else:
	print "input number of pixels"
	A = input('')
	print "input path to smoothed image"
	H = raw_input('')
	print "input path to background image"
	print "If there is no background enter 'no'"
	B = raw_input('')
	print "input path to original image"
	T = raw_input('')


img_t = read_file(T)
img_h = read_file(H)
orig_pix_vals_h = img_h.get_image().values
orig_pix_vals_t = img_t.get_image().values
for x in range(0,A):						#adjust upper limit to the image pixel size of the image
	for y in range(0,A):
		a = (img_t.get_image().values[x,y] - img_h.get_image().values[x,y])
		if a < 0:
			img_h.get_image().values[x,y] = 0 
		else:
			img_h.get_image().values[x,y] = a
	
h=0
b=0
t=0

if B == 'no':
	for x in range(0,A):						
		for y in range(0,A):
			h += img_h.get_image().values[x,y] 
			t += img_t.get_image().values[x,y]

else:
	img_b = read_file(B)
	orig_pix_vals_b = img_b.get_image().values

	for x in range(0,A):						
		for y in range(0,A):
			h += img_h.get_image().values[x,y]
			b += img_b.get_image().values[x,y] 
			t += img_t.get_image().values[x,y]

print (h-b)/t

