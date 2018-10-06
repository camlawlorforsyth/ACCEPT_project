# checks/ README #

To perform these checks, copy this checks/ folder into your data directory.
After that, move the two verify_*.py files into the data directory from this now copied directiory. 
run: python verify_*.py  
with * replaced with the end of the file name, for both tests

After each test a file called "good.txt" should appear with any error's listed that the 
tests found.

Verify reproj: Occasionally, the download and reprojection will skip over some necessary files
this test ensures no files are missing (if the are, image counts and point sources will be off)
and tells you if any files are missing. If the are you will have to delete, and redownload the 
cluster with the error.

Verify coords: This file goes through all the region files before reduce2, and ensures they are 
saved in the proper coordinates. If not you will have to resave them