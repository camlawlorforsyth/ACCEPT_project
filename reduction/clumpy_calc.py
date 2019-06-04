# this script assumes Python 3.5 is in use

# imports
import numpy as np
from astropy.io import fits

#..........................................................................main
def main(file, smooth) :
    
    science = fits.open(file) # open the background-subtracted science image
    image = science[0].data # get the science data that will be used
    science.close()
    
    smoothed = fits.open(smooth) # open the smoothed image
    smooth_image = smoothed[0].data # get the smoothed data that will be used
    smoothed.close()
    
    return clumpiness(image, smooth_image)

#....................................................................clumpiness
def clumpiness(image, smoothed) :
    
    num_total = 0
    denom_total = 0
    values = []
    
    dim = min(image.shape[0], image.shape[1]) # images might not be perfectly
                                              # square
    
    # pixel coordinates are of the form image[y,x]
    for x in range(0, dim) : # loop for every pixel in the image
        for y in range(0, dim) :
            num = ( image[x,y] - smoothed[x,y] )
            num_total += num
            denom = ( image[x,y] )
            denom_total += denom
            values.append( num / denom )
    
    return num_total/denom_total, num_total/denom_total*np.std(np.array(values), ddof=1)
#..............................................................end of functions
