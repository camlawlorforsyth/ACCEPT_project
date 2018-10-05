To begin point source extraction and statistical significance analysis, 
enter you data directory in your terminal.

for each cluster you'll want to open the data.txt file [gedit data.txt &]
and the broad_thresh.img in clusterName/expcor_mosaic_2 [ds9 -log broad_thresh.img &]

Once open, click on the image and a green circle should appear. Double click within
the circle to edit it's properties. Enter the radius found in data.txt and the RA and Dec
found on the ACCEPT site as center cordinates. You have now created the Region of Extraction (ROI)

In the circle window, open analysis. If the sum counts are less than what is found
in the data.txt file (20000*(1+z)^4), than the cluster data is statistically insignificant
and should be labelled bad with a "b" flag in all files where applicable. 

If it's good (not bad) you can move on to point source extraction. Save the ROI you have
created in the cluster directory. Save it with the name "ds9_fk.reg" with coordinates of ds9 & fk5.

Save it once again, this time in clusterName/expcor_mosaic_2 with the name "bk.reg"
Use the coodinates ciao & physical this time. 

Now create circles around every bright source found in the ROI. See reduction/example for a sample
of this. Ensure that the point source regions you make are as tight as possible. 

Once you have surrounded every point source in the ROI tightly with a circular region, save it in 
clusterName/expcor_mosaic_2 as "sources_mod.reg" with coordinates ciao & physical, just like bk.reg
ENSURE THE CIRCLE FOR THE ROI ITSELF IS NOT INCLUDED IN THE POINT SOURCE REGION FILES

Save it once more in clusterName/expcor_mosaic with the same name "sources_mod.reg" and same coordinates
ciao & physical

close ds9, and now from clusterName/expcor_mosaic, open broad_thresh.img in ds9
this is a more fine grained version of the previous image you had open.
Open sources_mod.reg and ensure that you are not missing any point sources, and
that you dont have any regions that are not around point sources.

If the regions have changed, overwrite the previous "sources_mod.reg" in expcor_mosaic
do NOT overwrite the "sources_mod.reg" in expcor_mosaic_2

Now you are ready to move on to the next step, found in Reduction/README
