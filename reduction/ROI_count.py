# this script assumes Python 3.5 is in use

# imports
import subprocess

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
    R_max = Angle(Rout/D_A*u.rad) # maximum radius in radians
    
    position = SkyCoord(ra=RA, dec=Dec, distance=D_A)
    aperture = SkyCircularAperture(position, r=R_max)
    phot_table = aperture_photometry(image, aperture, wcs=world_cs)
    total_counts_per_second = phot_table['aperture_sum'][0]
    
    exposure_time = header['EXPOSURE'] # exposure time in seconds
    
    minimum_necessary_counts = 20000
    
    if (total_counts_per_second*exposure_time) < minimum_necessary_counts :
        
        with open('insufficient.txt', 'w') as file :
            file.write("Actual counts: " +
                       str(total_counts_per_second*exposure_time))
        
        return "skip"
    else :
        roi_sky = ('# Region file format: DS9 version 4.1\n' +
                   'global width=1\n' + 'fk5\n')
        
        roi_sky += ("circle(" + RA.to_string(unit=u.hour, sep=':') +
                    "," + Dec.to_string(unit=u.degree, sep=':') +
                    "," + str(R_max.to(u.arcsec).value) + '")\n')
        
        box_sky = ('# Region file format: DS9 version 4.1\n' +
                   'global width=1\n' + 'fk5\n')
        
        box_sky += ("box(" + RA.to_string(unit=u.hour, sep=':') +
                    "," + Dec.to_string(unit=u.degree, sep=':') +
                    "," + str(4*R_max.to(u.arcsec).value) + '"' +
                    "," + str(4*R_max.to(u.arcsec).value) + '",360)\n')
        
        with open('roi_sky.reg', 'w') as file :
            file.write(roi_sky) # create the roi_sky.reg file for further use
        
        with open('box_sky.reg', 'w') as file :
            file.write(box_sky) # save square region with l=w=2*R_max
        
        # http://cxc.harvard.edu/ciao/ahelp/dmmakereg.html    
        
        subprocess.run("punlearn dmmakereg", shell=True)
        subprocess.run("dmmakereg 'region(roi_sky.reg)' roi_phys.reg " +
                       "kernel=ascii wcsfile=merged_2/broad_flux.img",
                       shell=True) # take the roi_sky.reg file and create a
                                   # CIAO physical roi_phys.reg file
        
        subprocess.run("dmmakereg 'region(box_sky.reg)' box_phys.reg "+
                       "kernel=ascii wcsfile=merged_2/broad_flux.img",
                       shell=True) # take the box_sky.reg file and create a
                                   # CIAO physical box_phys.reg file
        
        return "sufficient"
#..............................................................end of functions
