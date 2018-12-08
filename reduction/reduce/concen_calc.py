# this script assumes Python 3.7 is in use

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
warnings.filterwarnings("ignore")

import sys

'''
The calling code used in reduce2.py for this file, is of the form:
python concen_calc.py science_image.fits integer
argv[-]    argv[0]         argv[1]       argv[2]
'''

#if len(sys.argv) == 3 :
    

(nameMain, RA, Dec, zz, zz_err, K0, K0_err, K100, K100_err,
     alpha, Tx, Tx_err, Lbol, Lbol_err, LbolUL, LHa, LHa_err,
     LHaUL, Lrad, Lrad_err) = np.genfromtxt(
    "../../accept_main.txt", delimiter = ',', unpack = True)

(nameCAS, ROIout, angsize, asymm, asymm_err, clump, clump_err,
    concen, concen_err) = np.genfromtxt(
    "../../accept_CAS.txt", delimiter = ',', unpack = True)

(RAs, Decs) = np.genfromtxt("../../accept_coordinates.txt",
                            unpack = True, dtype=str)

# constants
cosmo = FlatLambdaCDM(H0 = 70, Om0 = 0.3) # specify the cosmology being used

#science = fits.open('threshed_broad_0.fits') # open the science image, 1E 0567-56
science = fits.open('threshed_broad_1.fits') # open the science image, 2A 0335+96
#science.info()
header = science[0].header # define the header, in order to get the WCS
image = science[0].data # create the image that will be used
science.close()

world_cs = WCS(header)

# the following are values that must get populated prior to running the script
i = 1

RA = Angle(RAs[i], u.hour)
Dec = Angle(Decs[i], u.deg)
redshift = zz[i]
R_out = ROIout[i]*u.Mpc

D_A = cosmo.angular_diameter_distance(redshift)
R_max = (R_out/D_A)*(180/np.pi)*u.deg # to get maximum radius in degrees

position = SkyCoord(ra=RA, dec=Dec, distance=D_A)
aperture = SkyCircularAperture(position, r=R_max)
phot_table = aperture_photometry(image, aperture, wcs=world_cs)
max_total = phot_table['aperture_sum'][0]

#........................................................................search
def search(desired_total) :
    
    eps = 1e-3
    radius = 1e-10*u.deg
    
    while radius <= R_max :
        aperture = SkyCircularAperture(position, r=radius)
        phot_table = aperture_photometry(image, aperture, wcs=world_cs)
        total = phot_table['aperture_sum'][0] # the value with no units
        
        if abs(desired_total-total) <= eps*max(abs(desired_total),abs(total)) :
            return radius
        else :
            radius += R_max/10000

#.................................................................concentration
def concentration() :
    
    r_20 = search(0.2*max_total) # find the radius that encompasses 20% of the
    r_80 = search(0.8*max_total) # emission, and then the same for 80%
    
    uncertainty = 5/np.log(10) * ( (R_max/10000)/r_20 + (R_max/10000)/r_80 )
    
    return 5*np.log10(r_80 / r_20), uncertainty

CC, CC_err = concentration()
print(CC)
print(CC_err)

