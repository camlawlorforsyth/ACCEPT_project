# checks/ README #

To perform these checks, copy this checks/ folder into the main data/ directory.

After that, copy the two verify\_\*.py files into the data/ directory from this (now copied) directory.
```
cp /checks/verify_*.py .
```

Following this, run `python verify_reproj.py`. This assumes `python get_all_data.py` has already been completed.

Next, run `python verify_coords.py` once all ROIs and point source region files have been created. See the [POINT_README](../reduce/POINT_README.md) in [reduce/](../reduce) for additional information, as well as the main reduction [README](../README.md) in [reduction/](..).

Once each verification process has completed, a "issues.txt" file will be created in the data/ directory, listing any errors that the tests may have discovered.

## Main files ##

1. [verify_reproj.py](verify_reproj.py) - Occasionally, the download and reprojection will skip over some necessary files. This test ensures no files are missing and states if there are any issues. If files are missing, image counts and point sources will be off, and the data for that particular cluster must be first deleted, and then re-downloaded.
   - [expcor_count.py](expcor_count.py) is called by verify_reproj.py

2. [verify_coords.py](verify_coords.py) - This file goes through all the region files before [process_all_data.py](../reduce/process_all_data.py) is called (which calls [reduce2.py](../reduce/reduce2.py)), and ensures the region files are saved in the proper coordinates. If there are any issues, the region files will have to be re-saved before proceeding.
   - [check_coords.py](check_coords.py) is called by verify_coords.py
