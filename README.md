# ACCEPT_project #

Relevant scripts used in the analysis and preparation of a paper regarding cooling cores and the dynamical state of galaxy clusters within the [ACCEPT](https://web.pa.msu.edu/astro/MC2/accept/) sample. See [*"Intracluster Medium Entropy Profiles for a Chandra Archival Sample of Galaxy Clusters"*, Cavagnolo et al. 2009, *ApJS*, 182, 12](http://adsabs.harvard.edu/abs/2009ApJS..182...12C) for further information and background regarding the ACCEPT sample.

## Data ##

### Sample Size ###

[accept_main.txt](accept_main.txt), [accept_20kpc.txt](accept_20kpc.txt), [accept_SFR.txt](accept_SFR.txt), [accept_CAS.txt](accept_CAS.txt), [accept_SPA_cavpow.txt](accept_SPA_cavpow.txt), and [accept_Fraser_BCG_SFR.txt](accept_Fraser_BCG_SFR.txt) all have 241 entries and are the complete ACCEPT sample.

### Data Files ###

[accept_main.txt](accept_main.txt) is adapted from the [accept_main.tab](https://web.pa.msu.edu/astro/MC2/accept/accept_main.tab) file found at http://www.pa.msu.edu/astro/MC2/accept/ under the **Useful Data and Figures** header. This file is comma delimited to accomodate the zero (0) value entries for bolometric, Halpha, and radio luminosity.

[accept_20kpc.txt](accept_20kpc.txt) is an adaptation of sorts of the [all_profiles.dat](https://web.pa.msu.edu/astro/MC2/accept/data/all_profiles.dat) file from http://www.pa.msu.edu/astro/MC2/accept/, under the **Useful Data and Figures** header. As each cluster has many annulii, the values presented in this file reflect the various parameters for an annulus with an inner radius of ~20 kpc from the centre of the cluster. This file is comma delimited.

[accept_SFR.txt](accept_SFR.txt) is adapted from the [**Table 7**](http://iopscience.iop.org/0067-0049/199/1/23/suppdata/apjs420668t7_mrt.txt) data file found at http://iopscience.iop.org/article/10.1088/0067-0049/199/1/23, from [Hoffer et al. (2012)](http://adsabs.harvard.edu/abs/2012ApJS..199...23H). This file is comma delimited.

[accept_CAS.txt](accept_CAS.txt) was produced by determining the CAS parameters for the clusters that have sufficient counts for statistically significant analysis and represents the culmination of six months of work for C. Lawlor-Forsyth, as well as likely longer for M. Radica. Additionally, C. McRae, Y. Bharani, and B. Blaikie were all instrumental in completing the CAS analysis for the full ACCEPT sample and this work could not have been completed without them. This file is comma delimited.

[accept_SPA_cavpow.txt](accept_SPA_cavpow.txt) contains the SPA parameters determined by [Mantz et al. (2015)](http://adsabs.harvard.edu/abs/2015MNRAS.449..199M), as well as the cavity powers for the various clusters. Cavity powers were selected from from [Rafferty et al. (2006)](http://adsabs.harvard.edu/abs/2006ApJ...652..216R), [Cavagnolo et al. (2010)](http://adsabs.harvard.edu/abs/2010ApJ...720.1066C), [O'Sullivan et al. (2011)](http://adsabs.harvard.edu/abs/2011ApJ...735...11O), and [Hlavacek-Larrondo et al. (2012)](http://adsabs.harvard.edu/abs/2012MNRAS.421.1360H). Data was downloaded via Vizier. This file is comma delimited.

[accept_Fraser_BCG_SFR.txt](accept_Fraser_BCG_SFR.txt) contains the BCG stellar mass and BCG SFR data for 72 clusters present in the ACCEPT sample, coming from [Fraser-McKelvie et al. (2014)](http://adsabs.harvard.edu/abs/2014MNRAS.444L..63F), recommended by Y. Gordon. Data was downloaded via Vizier. This file is comma delimited.

## Programs ##

[master.py](master.py) is the master program responsible for creating the most current plots, and determining Spearman rank coefficients as well as p-values.

[correlations.xlsx](correlations.xlsx) is the master table of correlations found when plotting all parameters against one-another. Sheet 1 contains the Spearman rank coefficients, while Sheet 2 contains the associated two-tailed p-values.

## Automated Reduction Process ##

Scripts and files relevant to the automated reduction process, including explanatory READMEs and instructions, can be found in [reduction/](reduction).
