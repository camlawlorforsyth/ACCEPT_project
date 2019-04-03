# this script assumes Python 3.5 is in use

'''
The calling code used in reduce2.py for this file, is of the form:
python asymm_calc.py threshed_broad.fits rot.fits
argv[-]    argv[0]         argv[1]        argv[2]
'''

# imports
import numpy as np

from astropy.io import fits
import sys

#..........................................................................main
def main() :
    
    if len(sys.argv) == 3 :
        file = sys.argv[1]
        rot = sys.argv[2]
#        bg = sys.argv[3]
    else : # this should only be necessary if not using the automated scripts
        file = get_image('Input the path to the original science image: ')
        rot = get_image('Input the path to the rotated image: ')
#        bg = get_image('Input the path to the background image: ')
        print('\nInput confirmed. Continuing with script.\n')
    
    science = fits.open(file) # open the background-subtracted science image
    #science.info()
    image = science[0].data # get the science data that will be used
    science.close()
    
    rotated = fits.open(rot) # open the rotated image
    #rotated.info()
    rot_image = rotated[0].data # get the rotated data that will be used
    rotated.close()
    '''
    background = fits.open(bg) # open the background image
#    background.info()
    bg_image = background[0].data # create the background image to use
    background.close()
    '''
    AA, AA_err = asymmetry(image, rot_image) #, bg_image)
    
    print('{0:g},{1:g} # asymm, asymm_err'.format(AA, AA_err))

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

#.....................................................................asymmetry
def asymmetry(image, rotated) :#, background) :
    
    num = 0
    denom = 0
    values = []
    
    dim = min(image.shape[0], image.shape[1]) # images might not be perfectly
                                              # square
    
    # pixel coordinates are of the form image[y,x]
    for x in range(0, dim) : # loop for every pixel in the image
        for y in range(0, dim) :
            num += ( image[x,y] - rotated[x,y] )**2
            denom += 2*( ( image[x,y] )**2 )
            values.append( 0.5*(image[x,y]-rotated[x,y])**2 / (image[x,y])**2 )
    
    return num/denom, num/denom*np.std(np.array(values), ddof=1)
#..............................................................end of functions

main()
