# ACCEPT_project #

Relevant scripts used in the analysis and preparation of a paper regarding cooling cores and the dynamical state of galaxy clusters within the [ACCEPT](https://web.pa.msu.edu/astro/MC2/accept/) sample. See [*"Intracluster Medium Entropy Profiles for a Chandra Archival Sample of Galaxy Clusters"*, Cavagnolo et al. 2009, *ApJS*, 182, 12](http://adsabs.harvard.edu/abs/2009ApJS..182...12C) for further information and background regarding the ACCEPT sample.

## Data ##

### Sample Size ###

[accept_main.txt](accept_main.txt), [accept_coordinates.txt](accept_coordinates.txt), [accept_20kpc.txt](accept_20kpc.txt), [accept_SFR.txt](accept_SFR.txt), [accept_CAS.txt](accept_CAS.txt), [accept_SPA_cavpow.txt](accept_SPA_cavpow.txt), and [accept_Fraser_BCG_SFR.txt](accept_Fraser_BCG_SFR.txt) all have 241 entries and are the complete ACCEPT sample.

### Data Files ###

Columns 0-17 of [accept_catalog.csv](accept_catalog.csv) are adapted from the [accept_main.tab](https://web.pa.msu.edu/astro/MC2/accept/accept_main.tab) file found at http://www.pa.msu.edu/astro/MC2/accept/ under the **Useful Data and Figures** header. The upper limit columns for the bolometric and Halpha luminosities have been removed, as well as the zero (0) value entries for bolometric, Halpha, and radio luminosity.

Columns 18-36 of [accept_catalog.csv](accept_catalog.csv) are an adaptation of sorts of the [all_profiles.dat](https://web.pa.msu.edu/astro/MC2/accept/data/all_profiles.dat) file from http://www.pa.msu.edu/astro/MC2/accept/, under the **Useful Data and Figures** header. As each cluster has many annulii, the values presented in thse columns reflect the various parameters for an annulus with an inner radius of ~20 kpc from the centre of the cluster.

Columns 37-46 of [accept_catalog.csv](accept_catalog.csv) are adapted from the [**Table 7**](http://iopscience.iop.org/0067-0049/199/1/23/suppdata/apjs420668t7_mrt.txt) data file found at http://iopscience.iop.org/article/10.1088/0067-0049/199/1/23, from [Hoffer et al. (2012)](http://adsabs.harvard.edu/abs/2012ApJS..199...23H).

Columns 47-54 of [accept_catalog.csv](accept_catalog.csv) were produced by determining the CAS parameters for the clusters that have sufficient counts for statistically significant analysis. M. Radica, C. McRae, Y. Bharani, and B. Blaikie were all instrumental in completing the CAS analysis for the full ACCEPT sample and this work could not have been completed without them.

Columns 55-74 of [accept_catalog.csv](accept_catalog.csv) contain the SPA parameters determined by [Mantz et al. (2015)](http://adsabs.harvard.edu/abs/2015MNRAS.449..199M), as well as the cavity powers for the various clusters. Cavity powers were selected from from [Rafferty et al. (2006)](http://adsabs.harvard.edu/abs/2006ApJ...652..216R), [Cavagnolo et al. (2010)](http://adsabs.harvard.edu/abs/2010ApJ...720.1066C), [O'Sullivan et al. (2011)](http://adsabs.harvard.edu/abs/2011ApJ...735...11O), and [Hlavacek-Larrondo et al. (2012)](http://adsabs.harvard.edu/abs/2012MNRAS.421.1360H). Data was downloaded via Vizier.

Columns 75-81 of [accept_catalog.csv](accept_catalog.csv) contain the BCG stellar mass and BCG SFR data for 72 clusters present in the ACCEPT sample, coming from [Fraser-McKelvie et al. (2014)](http://adsabs.harvard.edu/abs/2014MNRAS.444L..63F), recommended by Y. Gordon. Data was downloaded via Vizier.

[accept_column_densities.txt](accept_column_densities.txt) were determined using the online tool 'Calculate Galactic NH,' available here: http://www.swift.ac.uk/analysis/nhtot/, with accompanying documentation here: http://www.swift.ac.uk/analysis/nhtot/docs.php.

## Programs ##

[master.py](master.py) is the master program responsible for creating the most current plots, and determining Spearman rank coefficients as well as p-values.

[correlations.xlsx](correlations.xlsx) is the master table of correlations found when plotting all parameters against one-another. Sheet 1 contains the Spearman rank coefficients, while Sheet 2 contains the associated two-tailed p-values.

[observations.xlsx](observations.xlsx) is the master table of all observations used in the preliminary analysis, and encompasses some 977 observations, totaling more than 28.8 Ms of clean observation time.

## Automated Reduction Process ##

Scripts and files relevant to the automated reduction process, including explanatory READMEs and instructions, can be found in [reduction/](reduction).

[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)
