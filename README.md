# ACCEPT_project #

Relevant scripts used in the analysis and preparation of a paper regarding cooling cores and the dynamical state of galaxy clusters within the ACCEPT sample.

## Data ##

### Sample Size ###

'accept_main.txt', 'accept_20kpc.txt', 'accept_SFR.txt', 'accept_CAS.txt', 'accept_SPA_cavpow.txt', and 'accept_Fraser_BCG_SFR.txt' all have 241 entries
 and are the complete ACCEPT sample.

### Data Files ###

'accept_main.txt' is adapted from the 'accept_main.tab' file found at http://www.pa.msu.edu/astro/MC2/accept/ under the 'Useful Data and Figures' header. This file is comma delimited to accomodate the zero (0) value entries for bolometric, Halpha, and radio luminosity.

'accept_20kpc.txt' was copied from the /data/udata/ACCEPT_data folder on Chris's machine. Note that the file was originally named 'ACCEPT_data_impr.txt' but was renamed for convenience. This file is an adaptation of sorts of the 'all_profiles.dat' file from http://www.pa.msu.edu/astro/MC2/accept/, under the 'Useful Data and Figures' header. As each cluster has many annulii, the values presented in this file reflect the various parameters for an annulus with an inner radius of 20 kpc from the centre of the cluster. This file is comma delimited.

'accept_SFR.txt' is adapted from the Table 7 data file found at http://iopscience.iop.org/article/10.1088/0067-0049/199/1/23, from the Hoffer et al. paper. This file is comma delimited.

'accept_CAS.txt' was produced by determining the CAS parameters for the clusters that have sufficient counts for statistically significant analysis and represents the culmination of nearly six months of work for Cam Lawlor-Forsyth, as well as likely longer for Michael Radica, Criag McRae, Yashashvi Bharani, Brynne Blaikie were all instrumental in completing the CAS analysis for the full ACCEPT sample and this work could not have been completed without them. This file is comma delimited.

'accept_SPA_cavpow.txt' contains the SPA parameters determined by Mantz et al. (2015), as well as the cavity powers [coming from Rafferty et al. (2006), Cavagnolo et al. (2010), O'Sullivan et al. (2011), Hlavacek-Larrondo et al. (2012)] for the various clusters. Data was downloaded via Vizier. This file is comma delimited.

'accept_Fraser_BCG_SFR.txt' contains the BCG stellar mass and BCG SFR data for 72 clusters present in the ACCEPT sample, coming from the Fraser-McKelvie et al. (2014) paper, recommended by Yjan. Data was downloaded via Vizier. This file is comma delimited.

## Programs ##

'master.py' is the master program responsible for creating the most current plots, and determining Spearman rank coefficients as well as p-values.

'correlations.xlsx' is the master table of correlations found when plotting all parameters against one-another. Sheet 1 contains the Spearman rank coefficients, while Sheet 2 contains the associated two-tailed p-values.

## Automated Reduction Process ##

Scripts and files relevant to the automated reduction process, including explanatory READMEs and instructions, can be found in [reduction/](reduction).
