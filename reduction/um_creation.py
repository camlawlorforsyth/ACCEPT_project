# this script assumes Python 3.5 is in use

# imports
from scipy import ndimage
from astropy.io import fits

#..........................................................................main
def main(file, scale) :
    
    science = fits.open(file) # open the background-subtracted science image
    image = science[0].data # get the science data that will be used
    science.close()
    
    smoothed_small = ndimage.gaussian_filter(image, scale)
    # smooth the original image using a Gaussian with a 3 pixel sigma
    
    smoothed_large = ndimage.gaussian_filter(image, 10*scale)
    # smooth the original image using a Gaussian with a 30 pixel sigma
    
    um_image = smoothed_small - smoothed_large
    
    hdul = fits.HDUList([fits.PrimaryHDU(um_image)])
    hdul.writeto('unsharp_mask.fits')
    
    return
#..............................................................end of functions
