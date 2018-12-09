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

import sys

'''
The calling code used in reduce2.py for this file, is of the form:
python concen_calc.py science_image.fits redshift
argv[-]    argv[0]         argv[1]       argv[2]
'''

if len(sys.argv) == 2 :
    file = sys.argv[1]
    redshift = sys.argv[2]
else : # this should only be necessary if not using the automated scripts
    print('Input the path to the original science image:')
    file = input('')
    print('Input the redshift to use:')
    redshift = float(input(''))
    print('Input confirmed. Continuing with script.')

(nameMain, zz, zz_err, K0, K0_err, K100, K100_err,
     alpha, Tx, Tx_err, Lbol, Lbol_err, LbolUL, LHa, LHa_err,
     LHaUL, Lrad, Lrad_err) = np.genfromtxt(
    "../../accept_main.txt", delimiter = ',', unpack = True)

(RAs, Decs) = np.genfromtxt("../../accept_coordinates.txt",
                            unpack = True, dtype=str)

(nameCAS, ROIout, angsize, asymm, asymm_err, clump, clump_err,
    concen, concen_err) = np.genfromtxt(
    "../../accept_CAS.txt", delimiter = ',', unpack = True)

# constants
cosmo = FlatLambdaCDM(H0 = 70, Om0 = 0.3) # specify the cosmology being used

science = fits.open(file) # open the science image
#science.info()
header = science[0].header # define the header, in order to get the WCS
image = science[0].data # create the image that will be used
science.close()

world_cs = WCS(header)

i = int(np.where(zz==redshift)[0]) # requires redshifts in 'zz' to be unique
RA = Angle(RAs[i], u.hour) # get the RA, Dec, ROIout for this cluster
Dec = Angle(Decs[i], u.deg)
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
    
    aperture = SkyCircularAperture(position, r=0.25*R_max)
    phot_table = aperture_photometry(image, aperture, wcs=world_cs)
    twentyfive_R_max_total = phot_table['aperture_sum'][0]
    
    aperture = SkyCircularAperture(position, r=0.5*R_max)
    phot_table = aperture_photometry(image, aperture, wcs=world_cs)
    fifty_R_max_total = phot_table['aperture_sum'][0]
    
    aperture = SkyCircularAperture(position, r=0.75*R_max)
    phot_table = aperture_photometry(image, aperture, wcs=world_cs)
    seventyfive_R_max_total = phot_table['aperture_sum'][0]
    
    if desired_total > seventyfive_R_max_total :
        radius = 0.75*R_max
    elif desired_total > fifty_R_max_total :
        radius = 0.5*R_max
    elif desired_total > twentyfive_R_max_total :
        radius = 0.25*R_max
    else :
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

print('C: {0:g}, C_err: {1:g}'.format(CC, CC_err))
