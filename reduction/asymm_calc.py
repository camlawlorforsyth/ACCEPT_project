# this script assumes Python 3.5 is in use

# imports
import numpy as np
from astropy.io import fits

#..........................................................................main
def main(file) :
    
    science = fits.open(file) # open the background-subtracted science image
    image = science[0].data # get the science data that will be used
    science.close()
    
    rot_image = np.rot90(image, 2) # rotate the original image by 180 degrees
    
    return asymmetry(image, rot_image)

#.....................................................................asymmetry
def asymmetry(image, rotated) :
    
    numer = (image - rotated)**2
    denom = image**2
    asymm = 0.5*np.sum(numer)/np.sum(denom)
    
    numer_flat = numer.flatten()
    denom_flat = denom.flatten()
    numer_len = len(numer_flat)
    denom_len = len(denom_flat)
    
    # bootstrap
    asymms = []
    for i in range(1000) :
        numer_resample = np.random.choice(numer_flat,size=numer_len,replace=True)
        denom_resample = np.random.choice(denom_flat,size=denom_len,replace=True)
        asymm_resample = 0.5*np.sum(numer_resample)/np.sum(denom_resample)
        asymms.append(asymm_resample)
    
    asymms = np.array(asymms)
    std_dev = np.std(asymms)
    
    return asymm, std_dev
#..............................................................end of functions
