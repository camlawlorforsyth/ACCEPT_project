# Concentration README #

To determine the concentration (C) parameter for a given cluster, first open the "threshed_broad.fits" image (located in /bin=2/) in DS9:
```
ds9 -log /bin=2/threshed_broad.fits &
```

Load the "ds9_fk.reg" region file into the image, by entering the 'Region' menu, and selecting 'Load Regions...'. Next, enter the 'Edit' menu and select 'Region', and then double-click on the region itself. In the newly opened properties window, enter the 'Analysis' menu and select 'Statistics'. This will open a new statistics window for the defined region.

Near the lower left of this window, the total number of counts enclosed by the region are displayed. Multiply this value by 0.8 to find 80% of the total counts. Following this, shrink the region in DS9 until the total number of counts shown in the statistics window matches the previously found 80% value. Record this radius as R80 by opening a new terminal and starting Python:
```
python
>>> import math as m
>>> R80 = found_radius_for_80%
```

Follow the same procedure as above for 80%, but this time for 20% of the total counts. Record this radius as R20 in Python: ```>>> R20 = found_radius_for_20%```. The concentration is defined to be:

C = 5 * log10( 80%\_radius / 20%\_radius ), so enter the following in Python:

```
>>> C = 5*m.log10( R80 / R20 )
```
