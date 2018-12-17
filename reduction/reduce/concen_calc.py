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
warnings.filterwarnings("ignore") # ignore warnings about WCS unit changes

import sys

'''
The calling code used in reduce2.py for this file, is of the form:
python concen_calc.py science_image.fits redshift
argv[-]    argv[0]         argv[1]       argv[2]
'''

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

#..........................................................................main
def main() :
    
    if len(sys.argv) == 3 :
        file = sys.argv[1]
        redshift = float(sys.argv[2])
    else : # this should only be necessary if not using the automated scripts
        file = get_image()
        redshift = get_redshift()
        print('\nInput confirmed. Continuing with script.\n')
    
    science = fits.open(file) # open the science image
    #science.info()
    header = science[0].header # define the header, in order to get the WCS
    image = science[0].data # create the image that will be used
    science.close()
    
    world_cs = WCS(header)
    
    i = int(np.where(zz==redshift)[0]) # requires redshifts in 'zz' be unique
    RA = Angle(RAs[i], u.hour) # get the RA, Dec, ROIout for this cluster
    Dec = Angle(Decs[i], u.deg)
    R_out = ROIout[i]*u.Mpc
    
    D_A = cosmo.angular_diameter_distance(redshift)
    R_max = (R_out/D_A)*(180/np.pi)*u.deg # to get maximum radius in degrees
    
    position = SkyCoord(ra=RA, dec=Dec, distance=D_A)
    aperture = SkyCircularAperture(position, r=R_max)
    phot_table = aperture_photometry(image, aperture, wcs=world_cs)
    max_total = phot_table['aperture_sum'][0]
    
    CC, CC_err = concentration(max_total, R_max, position, image, world_cs)
    
    print('{0:g},{1:g} # concen, concen_err'.format(CC, CC_err))

#.....................................................................get_image
def get_image() :
    
    prompt = ('Input the path to the original science image: ')
    warning = '\b'
    while warning : # drop out if empty
        userIn = input(warning + prompt)
        warning = ''
        try :
            val = ( userIn )
            if val == None :
                warning = ("You must have some image. Please try again.\n\n")
            else :
                pass
        except ValueError :
            warning = ("Error. Please try again.\n\n")   
    
    return val

#..................................................................get_redshift
def get_redshift() :
    
    prompt = ('Input the unique redshift to use for analysis: ')
    warning = '\b'
    while warning : # drop out if empty
        userIn = input(warning + prompt)
        warning = ''
        try :
            val = float( userIn )
            if val == None :
                warning = ("You must have the redshift. Please try again.\n\n")
            elif val < 0 :
                warning = ("Redshifts aren't negative. Please try again.\n\n")
            else :
                pass
        except ValueError :
            warning = ("Error. Please try again.\n\n") 
    
    return val

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
                return radius
            else :
                radius += R_max/num_steps
        else : # if (desired_total-total) < 0, we've gone too far
            return (-1) # so we return (-1) and try again with finer steps

#.................................................................concentration
def concentration(max_total, R_max, position, image, wcs) :
    
    # find radius that encompasses 20% of the emission, then the same for 80%
    r_20 = search(0.2*max_total, R_max, position, image, wcs, 10000)
    r_80 = search(0.8*max_total, R_max, position, image, wcs, 10000)
    
    if r_20 == (-1) :
        r_20 = search(0.2*max_total, R_max, position, image, wcs, 100000)
        r_20_relative_error = (R_max/100000)/r_20
    else :
        r_20_relative_error = (R_max/10000)/r_20
    
    if r_80 == (-1) :
        r_80 = search(0.8*max_total, R_max, position, image, wcs, 100000)
        r_80_relative_error = (R_max/100000)/r_80
    else :
        r_80_relative_error = (R_max/10000)/r_80
    
    uncertainty = 5/np.log(10) * ( r_20_relative_error + r_80_relative_error )
    
    return 5*np.log10(r_80 / r_20), uncertainty
#..............................................................end of functions

main()
