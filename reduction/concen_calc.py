# this script assumes Python 3.5 is in use

# imports
import numpy as np

from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
from astropy.cosmology import FlatLambdaCDM
from astropy.io import fits
import astropy.units as u
from astropy.wcs import WCS
from photutils import aperture_photometry
from photutils import SkyCircularAperture
import warnings
warnings.filterwarnings("ignore") # ignore warnings about WCS unit changes

# constants
cosmo = FlatLambdaCDM(H0 = 70, Om0 = 0.3) # specify the cosmology being used

#..........................................................................main
def main(file, right_ascension, declination, redshift, Rout_Mpc) :
    
    science = fits.open(file) # open the science image
    header = science[0].header # define the header, in order to get the WCS
    image = science[0].data # create the image that will be used
    science.close()
    
    world_cs = WCS(header)
    
    RA = Angle(right_ascension, u.deg) # the RA, Dec for this cluster
    Dec = Angle(declination, u.deg)
    Rout = Rout_Mpc*u.Mpc # the Rout_Mpc for this cluster
    
    D_A = cosmo.angular_diameter_distance(redshift)
    R_max = (Rout/D_A)*(180/np.pi)*u.deg # maximum radius in degrees
    
    position = SkyCoord(ra=RA, dec=Dec, distance=D_A)
    aperture = SkyCircularAperture(position, r=R_max)
    phot_table = aperture_photometry(image, aperture, wcs=world_cs)
    max_total = phot_table['aperture_sum'][0]
    
    return concentration(max_total, R_max, position, image, world_cs)

#........................................................................search
def search(desired_total, R_max, position, image, wcs, num_steps) :
    
    eps = 1e-3
    
    aperture = SkyCircularAperture(position, r=0.1*R_max)
    phot_table = aperture_photometry(image, aperture, wcs=wcs)
    ten_R_max_total = phot_table['aperture_sum'][0]
    
    aperture = SkyCircularAperture(position, r=0.2*R_max)
    phot_table = aperture_photometry(image, aperture, wcs=wcs)
    twenty_R_max_total = phot_table['aperture_sum'][0]
    
    aperture = SkyCircularAperture(position, r=0.3*R_max)
    phot_table = aperture_photometry(image, aperture, wcs=wcs)
    thirty_R_max_total = phot_table['aperture_sum'][0]
    
    aperture = SkyCircularAperture(position, r=0.4*R_max)
    phot_table = aperture_photometry(image, aperture, wcs=wcs)
    forty_R_max_total = phot_table['aperture_sum'][0]
    
    aperture = SkyCircularAperture(position, r=0.5*R_max)
    phot_table = aperture_photometry(image, aperture, wcs=wcs)
    fifty_R_max_total = phot_table['aperture_sum'][0]
    
    aperture = SkyCircularAperture(position, r=0.6*R_max)
    phot_table = aperture_photometry(image, aperture, wcs=wcs)
    sixty_R_max_total = phot_table['aperture_sum'][0]
    
    aperture = SkyCircularAperture(position, r=0.7*R_max)
    phot_table = aperture_photometry(image, aperture, wcs=wcs)
    seventy_R_max_total = phot_table['aperture_sum'][0]
    
    aperture = SkyCircularAperture(position, r=0.8*R_max)
    phot_table = aperture_photometry(image, aperture, wcs=wcs)
    eighty_R_max_total = phot_table['aperture_sum'][0]
    
    aperture = SkyCircularAperture(position, r=0.9*R_max)
    phot_table = aperture_photometry(image, aperture, wcs=wcs)
    ninety_R_max_total = phot_table['aperture_sum'][0]

    if desired_total > ninety_R_max_total :
        radius = 0.9*R_max
    elif desired_total > eighty_R_max_total :
        radius = 0.8*R_max
    elif desired_total > seventy_R_max_total :
        radius = 0.7*R_max
    elif desired_total > sixty_R_max_total :
        radius = 0.6*R_max
    elif desired_total > fifty_R_max_total :
        radius = 0.5*R_max
    elif desired_total > forty_R_max_total :
        radius = 0.4*R_max
    elif desired_total > thirty_R_max_total :
        radius = 0.3*R_max
    elif desired_total > twenty_R_max_total :
        radius = 0.2*R_max
    elif desired_total > ten_R_max_total :
        radius = 0.1*R_max
    else :
        radius = 1e-10*u.deg
    
    while radius <= R_max :
        aperture = SkyCircularAperture(position, r=radius)
        phot_table = aperture_photometry(image, aperture, wcs=wcs)
        total = phot_table['aperture_sum'][0] # the value with no units
        
        if (desired_total-total) > 0 :
            if (desired_total-total) <= eps*max(abs(desired_total),abs(total)) :
                return radius, (R_max/num_steps)/radius
            else :
                radius += R_max/num_steps
        else : # if (desired_total-total) < 0, we've gone too far
               # so we try again with finer steps
            search(desired_total, R_max, position, image, wcs, 10*num_steps)

#.................................................................concentration
def concentration(max_total, R_max, position, image, wcs) :
    
    # find radius that encompasses 20% of the emission, then the same for 80%
    r_20, r_20_rel_err = search(0.2*max_total, R_max, position, image, wcs, 10000)
    r_80, r_80_rel_err = search(0.8*max_total, R_max, position, image, wcs, 10000)
    
    uncertainty = 5/np.log(10) * ( r_20_rel_err + r_80_rel_err )
    
    return 5*np.log10(r_80 / r_20), uncertainty
#..............................................................end of functions
