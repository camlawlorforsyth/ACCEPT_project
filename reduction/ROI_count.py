# this script assumes Python 3.5 is in use

'''
The calling code used in reduce1.py for this file, is of the form:
python ../reduce/ROI_count.py 1E_0657-56 image.img redshift Rout_Mpc
argv[-]       argv[0]         argv[1]     argv[2]  argv[3]  argv[4]
'''

# imports
import numpy as np

from astropy.coordinates import Angle
from astropy.coordinates import SkyCoord
from astropy.cosmology import FlatLambdaCDM
from astropy.io import ascii
from astropy.io import fits
import astropy.units as u
from astropy.wcs import WCS
from photutils import aperture_photometry
from photutils import SkyCircularAperture
import warnings
warnings.filterwarnings("ignore") # ignore warnings about WCS unit changes

import os
import sys

# read in the complete catalog
dat = ascii.read('../accept_catalog.csv') # requires columns to have unique
                                             # names
dat.add_index('z') # index the catalog by redshift so that row queries are
                  # possible

# constants
cosmo = FlatLambdaCDM(H0 = 70, Om0 = 0.3) # specify the cosmology being used

#..........................................................................main
def main() :
    
    if len(sys.argv) == 4 :
        cluster = sys.argv[1]
        file = sys.argv[2]
        redshift = float(sys.argv[3])
        Rout_Mpc = float(sys.argv[4])
    else : # this should only be necessary if not using the automated scripts
        cluster = get_cluster()
        file = get_image()
        redshift = get_redshift()
        Rout_Mpc = get_Rout_Mpc()
        print('\nInput confirmed. Continuing with script.\n')
    
    science = fits.open(file) # open the science image
    #science.info()
    header = science[0].header # define the header, in order to get the WCS
    image = science[0].data # create the image that will be used
    science.close()
    
    world_cs = WCS(header)
    
    index = dat.loc_indices[redshift] # requires redshift in dat['z'] be unique
    RA = Angle(dat['RA'][index], u.deg) # get the RA, Dec for this cluster
    Dec = Angle(dat['Dec'][index], u.deg)
    Rout = Rout_Mpc*u.Mpc # the Rout_Mpc for this cluster
    
    D_A = cosmo.angular_diameter_distance(redshift)
    R_max = (Rout/D_A)*(180/np.pi)*u.deg # maximum radius in degrees
    
    position = SkyCoord(ra=RA, dec=Dec, distance=D_A)
    aperture = SkyCircularAperture(position, r=R_max)
    phot_table = aperture_photometry(image, aperture, wcs=world_cs)
    total_counts = phot_table['aperture_sum'][0]
    
    minimum_necessary_counts = 20000*(1 + redshift)**4
    
    cmd = 'os.system("'
    cmd += ("python reduce/reduce2.py " + cluster + " " + str(redshift) + " " +
            str(Rout_Mpc) )
    
    if total_counts < minimum_necessary_counts :
        cmd += ' skip")' # append the quality flag for further analysis
        print(cmd)
    else :
        cmd += ' complete")'
        print(cmd)
        
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
    
    return

#...................................................................get_cluster
def get_cluster() :
    
    prompt = ('Input the cluster to use for analysis: ')
    warning = '\b'
    while warning : # drop out if empty
        userIn = input(warning + prompt)
        warning = ''
        try :
            val = str( userIn )
            if val == None :
                warning = ("You clearly have some data. Please try again.\n\n")
            else :
                pass
        except ValueError :
            warning = ("Error. Please try again.\n\n") 
    
    return val

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

#..................................................................get_Rout_Mpc
def get_Rout_Mpc() :
    
    prompt = ('Input the Rout_Mpc to use for analysis: ')
    warning = '\b'
    while warning : # drop out if empty
        userIn = input(warning + prompt)
        warning = ''
        try :
            val = float( userIn )
            if val == None :
                warning = ("You must have an outer radius. Please try again.\n\n")
            elif val < 0 :
                warning = ("Radii aren't negative. Please try again.\n\n")
            else :
                pass
        except ValueError :
            warning = ("Error. Please try again.\n\n") 
    
    return val
#..............................................................end of functions

main()
