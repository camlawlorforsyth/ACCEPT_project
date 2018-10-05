To determine the concentration (C) parameter for a given cluster,
first open the 'threshed_broad.fits' image (located in bin=2/) in ds9
and load the 'ds9_fk.reg' region file onto the image. Next, open the
statistics for the region to find the total number of counts enclosed.
Multiply this value by 0.8 to find 80% of the total counts. Following
this, shrink the region in ds9 until the total number of counts shown
in the statistics pane matches the previously found 80% value. Record
this radius. Complete the same process for 20% of the total counts,
again recording the radius. The concentration (C) is then:

C = 5 * log10(80%_radius / 20%_radius)
