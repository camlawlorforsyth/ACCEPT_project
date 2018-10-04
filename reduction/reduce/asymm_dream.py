from pycrates import read_file
import numpy as np
import math
import sys

if len(sys.argv) == 5:
	A = int(sys.argv[1])
	R = sys.argv[2]
	B = sys.argv[3]
	T = sys.argv[4]
else:
	print "input number of pixels"
	A = input('')
	print "input path to rotated image"
	R = raw_input('')
	print "input path to background image"
	print "If there is no background enter 'no'"
	B = raw_input('')
	print "input path to original image"
	T = raw_input('')

img_r = read_file(R)
img_t = read_file(T)
orig_pix_vals_r = img_r.get_image().values
orig_pix_vals_t = img_t.get_image().values

r=0
b=0
t=0

if B == 'no':
	for x in range(0,A):						
		for y in range(0,A):
			r += (img_t.get_image().values[x,y] - img_r.get_image().values[x,y])**2	
			t += 2*(img_t.get_image().values[x,y])**2

else:
	img_b = read_file(B)
	orig_pix_vals_b = img_b.get_image().values

	for x in range(0,A):						
		for y in range(0,A):
			r += (img_t.get_image().values[x,y] - img_r.get_image().values[x,y])**2	
			b += (img_b.get_image().values[x,y])**2 
			t += 2*((img_t.get_image().values[x,y])**2)

print (r-b)/t
