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
    
    numer = image - smoothed
    numer = np.ma.masked_where(numer < 0, numer)
    np.ma.set_fill_value(numer, 0)
    numer = numer.filled()
    denom = image
    clumpy = np.sum(numer)/np.sum(denom)
    
    numer_flat = numer.flatten()
    denom_flat = denom.flatten()
    numer_len = len(numer_flat)
    denom_len = len(denom_flat)
    
    # bootstrap
    clumpys = []
    for i in range(10000) :
        numer_resample = np.random.choice(numer_flat,size=numer_len,replace=True)
        denom_resample = np.random.choice(denom_flat,size=denom_len,replace=True)
        clumpy_resample = np.sum(numer_resample)/np.sum(denom_resample)
        clumpys.append(clumpy_resample)
    
    clumpys = np.array(clumpys)
    std_dev = np.std(clumpys)
    
    return clumpy, std_dev
#..............................................................end of functions
