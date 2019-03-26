# this script assumes Python 3.7 is in use

# imports
from astropy.io import fits

import sys

'''
The calling code used in reduce2.py for this file, is of the form:
python asymm_calc.py threshed_broad.fits smoothed.fits
argv[-]    argv[0]         argv[1]        argv[2]
'''

#..........................................................................main
def main() :
    
    if len(sys.argv) == 3 :
        file = sys.argv[1]
        smooth = sys.argv[2]
#        bg = sys.argv[3]
    else : # this should only be necessary if not using the automated scripts
        file = get_image('Input the path to the original science image: ')
        smooth = get_image('Input the path to the smoothed image: ')
#        bg = get_image('Input the path to the background image: ')
        print('\nInput confirmed. Continuing with script.\n')
    
    science = fits.open(file) # open the background-subtracted science image
    #science.info()
    image = science[0].data # get the science data that will be used
    science.close()
    
    smoothed = fits.open(smooth) # open the smoothed image
    #rotated.info()
    smooth_image = smoothed[0].data # get the smoothed data that will be used
    smoothed.close()
    '''
    background = fits.open(bg) # open the background image
#    background.info()
    bg_image = background[0].data # create the background image to use
    background.close()
    '''
    SS, SS_err = clumpiness(image, smooth_image) #, bg_image)
    
    print('{0:g},{1:g} # clump, clump_err'.format(SS, SS_err))

#.....................................................................get_image
def get_image(prompt_string) :
    
    prompt = (prompt_string)
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

#....................................................................clumpiness
def clumpiness(image, smoothed) :#, background) :
    
    num = 0
    denom = 0
    
    # pixel coordinates are of the form image[y,x]
    for x in range(0, image.shape[1]) : # loop for every pixel in the image
        for y in range(0, image.shape[0]) :
            num += ( image[x,y] - smoothed[x,y] )
            denom += ( image[x,y] )
    
    return num/denom, -1
#..............................................................end of functions

main()