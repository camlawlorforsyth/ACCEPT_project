# this script assumes Python 3.5 is in use

# imports
import numpy as np
from astropy.io import fits

#..........................................................................main
def main(file, rot) :
    
    science = fits.open(file) # open the background-subtracted science image
    image = science[0].data # get the science data that will be used
    science.close()
    
    rotated = fits.open(rot) # open the rotated image
    rot_image = rotated[0].data # get the rotated data that will be used
    rotated.close()
    
    return asymmetry(image, rot_image)

#.....................................................................asymmetry
def asymmetry(image, rotated) :
    
    num_total = 0
    denom_total = 0
    values = []
    
    # pixel coordinates are of the form image[y,x]
    for x in range(0, image.shape[0]) : # loop for every pixel in the image
        for y in range(0, image.shape[1]) :
            num = ( image[x,y] - rotated[x,y] )**2
            num_total += num
            denom = 2*( ( image[x,y] )**2 )
            denom_total += denom
            values.append( num / denom )
    
    return num_total/denom_total, num_total/denom_total*np.std(np.array(values), ddof=1)
#..............................................................end of functions
