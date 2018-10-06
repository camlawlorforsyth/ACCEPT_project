# Point Source Analysis README #

To begin point source extraction and statistical significance analysis, enter the data/ directory through the terminal. This analysis assumes that SAOImageDS9 is installed on the system, and is accessible from the terminal via `ds9`.

## Defining the Region of Extraction ##

Navigate to the directory of the cluster of interest. Open the "data.txt" file and the bin=2 "broad_thresh.img" by running:
```
gedit data.txt &
ds9 -log /expcor_mosaic_2/broad_thresh.img &
```

Once the image is open in DS9, enter the 'Edit' menu and select 'Region'. Click on the image and a green circular region should appear. Double click within the circle to edit it's properties. Enter the radius found in "data.txt" and the right ascension (RA) and declination (Dec) found on the [ACCEPT site](https://web.pa.msu.edu/astro/MC2/accept/) as the coordinates for the center. The region of extraction (ROI) has now been created.

In the properties window, enter the 'Analysis' menu and select 'Statistics'. This will open a new statistics window for the defined region. If the sum of counts (lower left of the window) are less than 20000*(1+z)^4, found in the "data.txt" file, then the cluster has insufficient data for statistically significant analysis. These clusters should be labelled as 'bad' with a `b` flag in all applicable files (namely [process_all_data.py](process_all_data.py), [verify_coords.py](../checks/verify_coords.py), and [ggm_all_data.py](ggm_all_data.py)).

If the cluster has sufficient counts, it should be labelled as 'done' with a `d` flag in the three files named above. Save the created ROI as `ds9_fk.reg` in the cluster's directory, using the 'ds9' format, with 'WCS - FK5' as the coordinate system.

Additionally, save the ROI as `bk.reg` into the "[cluster_name]/expcor_mosaic_2 directory", using the 'CIAO' format with 'Physical' as the coordinate system.

## Point Source Removal ##

Once the ROI has been successfully saved, the point source analysis can be started.

Create circular regions around every bright point source found within the ROI. Ensure that the point source regions are as small as possible while containing the entire point source, without encompassing any additional background. 

Once every point source has been enclosed within a circular region in the ROI, save these regions in the "[cluster_name]/expcor_mosaic_2" directory as `sources_mod.reg` using the 'CIAO' format with 'Physical' as the coordinate system. This is the same style as for the `bk.reg` file from earlier. It is important to ensure that the entire ROI itself **is not** included in the point source regions.

Save the point source regions once more in the "[cluster_name]/expcor_mosaic" directory, again as `sources_mod.reg` using the 'CIAO' format with 'Physical' as the coordinate system. Close DS9.

### Bin=0.5 Confirmation ###

Open the "broad_thresh.img" image within the "[cluster_name]/expcor_mosaic" directory by running `ds9 -log /expcor_mosaic/broad_thresh.img &`. This image has different binning than the image found in "expcor_mosaic_2/". Open "sources_mod.reg" inside DS9, and ensure that all point sources have a circular region enclosing them. As well, if any source regions appear to lack a point source, remove said region.

If the regions have changed, overwrite the previous "sources_mod.reg" in the "[cluster_name]/expcor_mosaic" directory, but **do not** overwrite the "sources_mod.reg" in the "[cluster_name]/expcor_mosaic_2" directory.

DS9 can once again be closed, and the next step (Step 2b) in the automated reduction process can be completed. Refer to the main reduction [README](../README.md) in [reduction/](..).
