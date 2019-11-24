# this script assumes Python 3.5 is in use

# imports
import numpy as np
from astropy.io import fits

#..........................................................................main
def main(file) :
    
    science = fits.open(file) # open the background-subtracted science image
    header = science[0].header # define the header, to get the exposure time
    image = science[0].data # get the science data that will be used
    science.close()
    
    exposure = header['EXPOSURE'] # total exposure time, to enable an easier
    image = image*exposure        # sigma calculation
    image = np.ma.masked_where(image < 0, image)
    np.ma.set_fill_value(image, 0)
    image = image.filled()
    sigma = np.sqrt(image)
    
    size = image.shape
    height, width = size[:2]
    center = [int(width/2), int(height/2)]
    max_radius = min(center[0], center[1], width-center[0], height-center[1])
    
    concen = concentration(image, max_radius, height, width, center)
    
    # monte-carlo
    concens = []
    for i in range(1000) :
        iteration = np.random.normal(image, sigma, size)
        concen_resample = concentration(iteration, max_radius,
                                        height, width, center)
        concens.append(concen_resample)
    
    concens = np.array(concens)
    std_dev = np.std(concens)
    
    return concen, std_dev

#.................................................................circular_mask
def circular_mask(height, width, center, radius) :        
    
    YY, XX = np.ogrid[:height, :width]
    dist_squared = ((XX - center[0])**2 + (YY - center[1])**2)
    
    return (dist_squared <= radius**2)

#.................................................................concentration
def concentration(image, max_radius, height, width, center) :
    
    total = np.sum(image)
    
    # find radius that encompasses 20% of the emission, then the same for 80%
    r_20_lo_rough, r_20_hi_rough = first_search(image, 0.2*total, max_radius,
                                                height, width, center)
    r_20_lo, r_20_hi = search(image, 0.2*total, r_20_lo_rough, r_20_hi_rough,
                              0.01, height, width, center)
    
    r_80_lo_rough, r_80_hi_rough = first_search(image, 0.8*total, max_radius,
                                                height, width, center)
    r_80_lo, r_80_hi = search(image, 0.8*total, r_80_lo_rough, r_80_hi_rough,
                              0.01, height, width, center)
    
    return 5*np.log10( np.mean([r_80_lo,r_80_hi])/np.mean([r_20_lo,r_20_hi]) )

#..................................................................first_search
def first_search(image, desired_total, max_radius, height, width, center) :
    
    twenty_five_radius = int(0.25*max_radius)
    twenty_five_mask = circular_mask(height, width, center, twenty_five_radius)
    twenty_five_masked_image = image.copy()
    twenty_five_masked_image[~twenty_five_mask] = 0
    twenty_five_radius_total = np.sum(twenty_five_masked_image)
    
    fifty_radius = int(0.5*max_radius)
    fifty_mask = circular_mask(height, width, center, fifty_radius)
    fifty_masked_image = image.copy()
    fifty_masked_image[~fifty_mask] = 0
    fifty_radius_total = np.sum(fifty_masked_image)
    
    seventy_five_radius = int(0.75*max_radius)
    seventy_five_mask = circular_mask(height, width, center, seventy_five_radius)
    seventy_five_masked_image = image.copy()
    seventy_five_masked_image[~seventy_five_mask] = 0
    seventy_five_radius_total = np.sum(seventy_five_masked_image)
    
    if desired_total > seventy_five_radius_total :
        initial_radius = seventy_five_radius_total
    elif desired_total > fifty_radius_total :
        initial_radius = fifty_radius
    elif desired_total > twenty_five_radius_total :
        initial_radius = twenty_five_radius
    else :
        initial_radius = 0
    
    return search(image, desired_total, initial_radius, max_radius, 1, height,
                  width, center)

#........................................................................search
def search(image, desired_total, initial_radius, max_radius, step, height,
           width, center) :
    
    radius = initial_radius
    while radius < max_radius : 
        mask = circular_mask(height, width, center, radius)
        masked_image = image.copy()
        masked_image[~mask] = 0
        total = np.sum(masked_image)
        diff = desired_total - total
        
        if diff < 0 :
            return radius-step, radius
        else :
            radius += step
#..............................................................end of functions
