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
from photutils import SkyCircularAperture, CircularAperture
import warnings
warnings.filterwarnings("ignore") # ignore warnings about WCS unit changes

# constants
cosmo = FlatLambdaCDM(H0 = 70, Om0 = 0.3) # specify the cosmology being used
eps = 1e-3

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
    R_max = Angle(Rout/D_A*u.rad) # maximum radius in radians
    
    position = SkyCoord(ra=RA, dec=Dec, distance=D_A)
    aperture = SkyCircularAperture(position, r=R_max).to_pixel(world_cs)
    phot_table = aperture_photometry(image, aperture)
    max_total = phot_table['aperture_sum'][0]
    radius_pix = aperture.r # maximum radius in pixels
    centre = aperture.positions # centre in pixels
    
    return concentration(max_total, radius_pix, centre, image)

#.................................................................concentration
def concentration(max_total, radius_pix, centre, image) :
    
    # find radius that encompasses 20% of the emission, then the same for 80%
    r_20, r_20_rel_err = search(0.2*max_total, radius_pix, centre, image, 10000)
    r_80, r_80_rel_err = search(0.8*max_total, radius_pix, centre, image, 10000)
    
    uncertainty = 5/np.log(10) * ( r_20_rel_err + r_80_rel_err )
    
    return 5*np.log10(r_80 / r_20), uncertainty

#........................................................................search
def search(desired_total, radius_pix, centre, image, num_steps) :
    
    aperture = CircularAperture(centre, r=0.1*radius_pix)
    phot_table = aperture_photometry(image, aperture)
    ten_radius_pix_total = phot_table['aperture_sum'][0]
    
    aperture = CircularAperture(centre, r=0.2*radius_pix)
    phot_table = aperture_photometry(image, aperture)
    twenty_radius_pix_total = phot_table['aperture_sum'][0]
    
    aperture = CircularAperture(centre, r=0.3*radius_pix)
    phot_table = aperture_photometry(image, aperture)
    thirty_radius_pix_total = phot_table['aperture_sum'][0]
    
    aperture = CircularAperture(centre, r=0.4*radius_pix)
    phot_table = aperture_photometry(image, aperture)
    forty_radius_pix_total = phot_table['aperture_sum'][0]
    
    aperture = CircularAperture(centre, r=0.5*radius_pix)
    phot_table = aperture_photometry(image, aperture)
    fifty_radius_pix_total = phot_table['aperture_sum'][0]
    
    aperture = CircularAperture(centre, r=0.6*radius_pix)
    phot_table = aperture_photometry(image, aperture)
    sixty_radius_pix_total = phot_table['aperture_sum'][0]
    
    aperture = CircularAperture(centre, r=0.7*radius_pix)
    phot_table = aperture_photometry(image, aperture)
    seventy_radius_pix_total = phot_table['aperture_sum'][0]
    
    aperture = CircularAperture(centre, r=0.8*radius_pix)
    phot_table = aperture_photometry(image, aperture)
    eighty_radius_pix_total = phot_table['aperture_sum'][0]
    
    aperture = CircularAperture(centre, r=0.9*radius_pix)
    phot_table = aperture_photometry(image, aperture)
    ninety_radius_pix_total = phot_table['aperture_sum'][0]
    
    if desired_total > ninety_radius_pix_total :
        radius = 0.9*radius_pix
    elif desired_total > eighty_radius_pix_total :
        radius = 0.8*radius_pix
    elif desired_total > seventy_radius_pix_total :
        radius = 0.7*radius_pix
    elif desired_total > sixty_radius_pix_total :
        radius = 0.6*radius_pix
    elif desired_total > fifty_radius_pix_total :
        radius = 0.5*radius_pix
    elif desired_total > forty_radius_pix_total :
        radius = 0.4*radius_pix
    elif desired_total > thirty_radius_pix_total :
        radius = 0.3*radius_pix
    elif desired_total > twenty_radius_pix_total :
        radius = 0.2*radius_pix
    elif desired_total > ten_radius_pix_total :
        radius = 0.1*radius_pix
    else :
        radius = 1e-10*radius_pix
    
    while radius <= radius_pix :
        aperture = CircularAperture(centre, r=radius)
        phot_table = aperture_photometry(image, aperture)
        total = phot_table['aperture_sum'][0] # the value with no units
        
        if (desired_total-total) > 0 :
            if (desired_total-total) <= eps*max(abs(desired_total),abs(total)) :
                return radius, (radius_pix/num_steps)/radius
            else :
                radius += radius_pix/num_steps
        else : # if (desired_total-total) < 0, we've gone too far
               # so we try again with finer steps
            search(desired_total, radius_pix, centre, image, 10*num_steps)
#..............................................................end of functions
