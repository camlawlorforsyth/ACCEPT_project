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

import os

# constants
cosmo = FlatLambdaCDM(H0 = 70, Om0 = 0.3) # specify the cosmology being used

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
    total_counts_per_second = phot_table['aperture_sum'][0]
    
    exposure_time = header['EXPOSURE'] # exposure time in seconds
    
    minimum_necessary_counts = 20000*(1 + redshift)**4
    
    if (total_counts_per_second*exposure_time) < minimum_necessary_counts :
        return "skip"
    else :
        ds9_fk5 = ('# Region file format: DS9 version 4.1\n' +
                   'global width=1\n' + 'fk5\n')
        
        ds9_fk5 += ("circle(" + RA.to_string(unit=u.hour, sep=':') + "," +
                    Dec.to_string(unit=u.degree, sep=':') + "," +
                    str(R_max/u.deg*3600) + '")\n')
        
        with open('ds9_fk5.reg', 'a') as file :
            file.write(ds9_fk5) # create the ds9_fk5.reg file for further use
        
        # http://cxc.harvard.edu/ciao/ahelp/dmmakereg.html    
        
        os.system('dmmakereg "region(ds9_fk5.reg)" bk.reg kernel=ascii ' + 
                  'wcsfile=merged_2/broad_flux.img') # take the ds9_fk5.reg
                              # file and create a CIAO physical bk.reg file
        
        return "sufficient"
