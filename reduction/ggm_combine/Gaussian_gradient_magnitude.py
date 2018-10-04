########################################################################
#gaussian_gradient_magnitude.py

#The main program is gaussian_gradient_magnitude.py. This utility applies the gaussian gradient magnitude filter to an input fits image, using a particular scale, sigma, in pixels.
#Requirements: - Python 2.7, pyfits, numpy, scipy
#To run, type ./gaussian_gradient_magnitude.py in.fits out.fits sigma Where sigma is a floating point value >0
########################################################################

#!/usr/bin/env python
import sys
import os
import argparse
import pyfits
import scipy.ndimage
import numpy as N

def run(infile, outfile, scale):
	f = pyfits.open(infile)
	img = f[0].data

	# convert to float if required
	if issubclass(img.dtype.type, N.integer):
		img = img.astype(N.float32)

	proc = scipy.ndimage.gaussian_gradient_magnitude(img, scale)

	f[0].data = proc

	try:
		os.unlink(outfile)
	except OSError:
		pass

	f.writeto(outfile)

def main():
	parser = argparse.ArgumentParser(
		description="Gaussian gradient magnitude")
	parser.add_argument('inimage', help='input image')
	parser.add_argument('outimage', help='output image')
	parser.add_argument('scale', type=float, help='gaussian sigma (pixels)')
	args = parser.parse_args()

	run(args.inimage, args.outimage, args.scale)
if __name__ == '__main__':
	main()

