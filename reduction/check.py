# this script assumes Python 3.5 is in use

'''
For information regarding how this script is initialized, see the 'README.md'
file in reduction/README.md.

The calling code used in check_all_data.py for this file, is of the form:
subprocess.run(['python','reduction/check.py','1E_0657-56','sufficient'])
                 argv[-]       argv[0]           argv[1]      argv[2]
'''

# imports
import os
import sys

# constants
cluster = sys.argv[1]
quality = sys.argv[2]
num_files = sum(len(files) for root, dirs, files in os.walk(cluster))

## STEP 1 - MOVE INTO CLUSTER DIRECTORY ##

os.chdir(cluster)

## STEP 2 - PERFORM NEXT STEP IF DATA IS OF SUFFICIENT QUALITY ##

if quality == "sufficient" :
    
## STEP 3 - CHECK IF 'SOURCES.REG' EXISTS AND COUNT POINT SOURCE REGIONS ##
    
    exists = os.path.isfile('sources.reg')
    
    if exists == True :
        with open('sources.reg', 'r') as file :
            num_lines = sum(1 for line in file)
        
        with open('../checks.txt', 'a') as file :
            file.write(cluster + "," + str(num_files) + "," + str(num_lines) + ",0,\n")
    
    else :
        with open('../checks.txt', 'a') as file :
            file.write(cluster + "," + str(num_files) + ",-1,MISSING,\n")

## STEP 4 - CHECK THE NUMBER OF COUNTS IF DATA IS INSUFFICIENT ##

else :
    
    with open('insufficient.txt', 'r') as file :
        counts = file.read().split(' ')[2]
    
    with open('../checks.txt', 'a') as file :
        file.write(cluster + "," + str(num_files) + ",,," + str(counts) + "\n")

## STEP 5 - RETURN TO THE DATA DIRECTORY ##

os.chdir("..") # go back to the data/ directory
