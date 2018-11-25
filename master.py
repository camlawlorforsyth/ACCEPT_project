# -*- coding: utf-8 -*-
"""
    SUMMER RESEARCH 2016/2017/2018
    ASSIGNMENT: Plot correlations
    AUTHOR:     Cam Lawlor-Forsyth (lawlorfc@myumanitoba.ca)
    SUPERVISOR: Chris O'Dea
    VERSION:    2018-Nov-25
    
    PURPOSE: Plot various parameters from multiple data tables while calculating
             Spearman rank correlations and associated p-values using SciPy.
"""

# imports
import numpy as np

import matplotlib as mpl # for publication-quality plots
mpl.rcParams['font.serif'] = "Times New Roman"
mpl.rcParams['font.family'] = "serif"
mpl.rcParams['text.usetex'] = True

import matplotlib.pyplot as plt
import scipy.stats as sp
from scipy import linalg
from time import ctime
import warnings
warnings.filterwarnings("ignore", category = RuntimeWarning) # ignore warnings

# create numpy arrays from *.txt data tables
# all '*.txt' data tables have 241 total entries
(nameMain, RA, Dec, zz, zz_err, K0, K0_err, K100, K100_err, alpha, Tx, Tx_err,
     Lbol, Lbol_err, LbolUL, LHa, LHa_err, LHaUL, Lrad, Lrad_err) = np.genfromtxt(
    "accept_main.txt", delimiter = ',', unpack = True)

(name20kpc, Rin, Rout, eDen, eDen_err, PLent, flatent, ent_err, PLpress,
    flatpress, press_err, clusmass, clusmass_err, clustemp, clustemp_err, 
    LL, coolingtime52, ct52_err, coolingtime, ct_err) = np.genfromtxt(
    "accept_20kpc.txt", delimiter = ',', unpack = True)
    # values above are for an annulus with inner radius ~20 kpc

(nameSFR, UVSFR, UV_err, IRSFR, IR_err, seventySFR, seventy_err,
    twentyfourSFR, twentyfour_err, BCGmass, BCGmass_err) = np.genfromtxt(
    "accept_SFR.txt", delimiter = ',', unpack = True)

(nameCAS, ROIout, angsize, asymm, asymm_err, clump, clump_err,
    concen, concen_err) = np.genfromtxt(
    "accept_CAS.txt", delimiter = ',', unpack = True)

(nameSPA, sym, peak, align, raff, cavag, osul, hlava, cavpow) = np.genfromtxt(
    "accept_SPA_cavpow.txt", delimiter = ',', unpack = True)

(nameACCEPT, nameFraser, BCGalt, SFRalt) = np.genfromtxt(
    "accept_Fraser_BCG_SFR.txt", delimiter = ',', unpack = True)

(tcool) = np.genfromtxt("tcool.txt", unpack=True)

# axis label dictionary
DICT = {
        # parameters from main table for entire cluster
        'zz':'Redshift',
        'K0':'Central Entropy (keV$\cdot$cm$^2$)',
        'K100':'Entropy at 100 kpc (keV$\cdot$cm$^2$)',
        'Tx':'Average Cluster Temperature (keV)',
        'Lbol':'Cluster Bolometric Luminosity ($10^{44}$ ergs s$^{-1}$)',
        'LHa':r'Cluster H$\alpha$ Luminosity ($10^{40}$ ergs s$^{-1}$)',
        'Lrad':'Cluster Radio Luminosity ($10^{40}$ ergs s$^{-1}$)',
        
        # parameters for annulus with inner radius ~20 kpc
        'eDen':'Electron Density (cm$^{-3}$) at ~20 kpc',
        'PLent':'Entropy using a Power Law (keV$\cdot$cm$^2$) at ~20 kpc',
        'flatent':'Entropy using a Flat Relation (keV$\cdot$cm$^2$) at ~20 kpc',
        'PLpress':'Pressure (dyne cm$^{-2}$)', #'Pressure using a Power Law (dyne cm$^{-2}$)',
        'flatpress':'Pressure (dyne cm$^{-2}$)', #'Pressure using a Flat Relation (dyne cm$^{-2}$)',
        'clusmass':'Cluster Mass ($M_\odot$) at ~20 kpc',
        'clustemp':'Cluster X-ray Temperature (keV) at ~20 kpc',
        'coolingtime52':'Cooling Time using the 5/2 Model (Gyr) at ~20 kpc', # note: 5*0.6 = 3
        'coolingtime':'Cooling Time (Gyr) at ~20 kpc', # uses the 3/2 model
        
        # star-formation parameters for Brightest Cluster Galaxy (BCG)
        'UVSFR':'UV SFR ($M_\odot$ yr$^{-1}$)',
        'IRSFR':'IR SFR ($M_\odot$ yr$^{-1}$)',
        'seventySFR':'70 $\mu$m SFR ($M_\odot$ yr$^{-1}$)',
        'twentyfourSFR':'24 $\mu$m SFR ($M_\odot$ yr$^{-1}$)',
        'BCGmass':'BCG Stellar Mass ($10^{10} \/ M_\odot$)',
        
        # CAS parameters and extras for entire cluster
        'asymm':'Asymmetry',
        'clump':'Clumpiness',
        'concen':'Concentration',
#        'ROIout':'Outer Radius of Region of Interest (Mpc)',
#        'angsize':'Angular Size Distance (Mpc)',
        
        # SPA parameters and cavity power for entire cluster
        'sym':'Symmetry',
        'peak':'Peakiness',
        'align':'Alignment',
        'cavpow':'Cavity Power ($10^{42}$ ergs s$^{-1}$)',
        
        # BCG and SFR parameters coming from Fraser-McKelvie et al. (2014)
        'BCGalt':'BCG Stellar Mass ($10^{10} \/ M_\odot$)\nfrom Fraser-McKelvie et al. (2014)',
        'SFRalt':'SFR ($M_\odot$ yr$^{-1}$)\nfrom Fraser-McKelvie et al. (2014)',
        
        # general axes titles and legend entries for mutli-plots
        'pressure':'Pressure (dyne cm$^{-2}$)',
        'PL':'Power Law Model',
        'flat':'Flat Relation Model'
        }

# dictionary to access associated errors

UNCERTS = {
           'zz':zz_err,
           'K0':K0_err,
           'K100':K100_err,
           'Tx':Tx_err, # error for Tx taken as standard dev. of individual temps
           'Lbol':Lbol_err,
           'LHa':LHa_err,
           'Lrad':Lrad_err,
          
           'eDen':eDen_err,
           'PLent':ent_err,
           'flatent':ent_err,
           'PLpress':press_err,
           'flatpress':press_err,
           'clusmass':clusmass_err,
           'clustemp':clustemp_err,
           'coolingtime52':ct52_err,
           'coolingtime':ct_err,
          
           'UVSFR':UV_err,
           'IRSFR':IR_err, # no error for IRSFR, therefore equal to 0
           'seventySFR':seventy_err,
           'twentyfourSFR':twentyfour_err,
           'BCGmass':BCGmass_err, # no error for BCGmass, therefore equal to 0
          
           'asymm':asymm_err, # no errors for asymm yet
           'clump':clump_err, # no errors for clump yet
           'concen':concen_err # no errors for concen yet
          
#           'sym':sym_err,
#           'peak':peak_err,
#           'align':align_err,
#           'cavpow':cavpow_err, # there is both an upper and lower error
          
#           'BCGalt':BCGalt_err, # there is both an upper and lower error
#           'SFRalt':SFRalt_err # there is both an upper and lower error
          }

# constants
currentFig = 1 # first figure will be numbered as 'Figure 1'

#...........................................................................main
def main(xvals, xlab, yvals, ylab, xmin=None, xmax=None, ymin=None,
         ymax=None, logx=False, logy=False, linear=False, errors=True,
         showplot=True) :
    """
    This function plots one parameter against the other, while labelling
    the respective axes correctly.
    """
    
    global currentFig
    spear = sp.spearmanr(xvals, yvals, nan_policy='omit') # find Spearman rank
                                                          # of the correlation
    print("Figure %2.1d   %13s vs %-13s   Spearman: %8.3g   pvalue: %8.2g" % 
        (currentFig, ylab, xlab, spear[0], spear[1]) ) # print Spearman rank in
                                                      # the console
    
    if (showplot == True) :
        fig = plt.figure(currentFig)  # the current figure
        currentFig += 1
        plt.clf() # clear the figure before each run
        
        ax = fig.add_subplot(111) # set axes, figure location
        
        if (errors == False) :
            if (logx == True) and (logy == False) and (linear == False) :
                ax.semilogx(xvals, yvals, 'ko') # use semilogx for peakiness
            elif (logx == False) and (logy == True) and (linear == False) :
                ax.semilogy(xvals, yvals, 'ko')
            elif (logx == False) and (logy == False) and (linear == True) :
                ax.plot(xvals, yvals, 'ko')
#                slope, intercept, xx = fit(xvals, yvals, lin=True)
#                ax.plot(xx, slope*xx + intercept, 'k-')
            elif (logx == True) and (logy == True) and (linear == False) :
                ax.loglog(xvals, yvals, 'ko') # use loglog to look for power laws
            else :
                ax.loglog(xvals, yvals, 'ko')
#                slope, intercept, xx = fit(xvals, yvals, lin=False)
#                ys = (xx**(slope))*(10**(intercept))
#                ax.loglog(xx, ys, 'k-')
        else :
            if (logx == True) and (logy == False) and (linear == False) :
                ax.set_xscale('log')
                ax.set_yscale('linear')
                ax.errorbar(xvals, yvals, xerr=UNCERTS[xlab], yerr=UNCERTS[ylab],
                            fmt='ko', elinewidth=0.3, capsize=1.5, errorevery=1)
            elif (logx == False) and (logy == True) and (linear == False) :
                ax.set_xscale('linear')
                ax.set_yscale('log')
                ax.errorbar(xvals, yvals, xerr=UNCERTS[xlab], yerr=UNCERTS[ylab],
                            fmt='ko', elinewidth=0.3, capsize=1.5, errorevery=1)
            elif (logx == False) and (logy == False) and (linear == True) :
                ax.set_xscale('linear')
                ax.set_yscale('linear')
                ax.errorbar(xvals, yvals, xerr=UNCERTS[xlab], yerr=UNCERTS[ylab],
                            fmt='ko', elinewidth=0.3, capsize=1.5, errorevery=1)
            elif (logx == True) and (logy == True) and (linear == False) :
                ax.set_xscale('log')
                ax.set_yscale('log')
                ax.errorbar(xvals, yvals, xerr=UNCERTS[xlab], yerr=UNCERTS[ylab],
                            fmt='ko', elinewidth=0.3, capsize=1.5, errorevery=1)
            else :
                ax.set_xscale('log')
                ax.set_yscale('log')
                ax.errorbar(xvals, yvals, xerr=UNCERTS[xlab], yerr=UNCERTS[ylab],
                            fmt='ko', elinewidth=0.3, capsize=1.5, errorevery=1)
        
        ax.set_xlabel("%s" % DICT[xlab], fontsize = 15 )
        ax.set_ylabel("%s" % DICT[ylab], fontsize = 15 )
        
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        
    #    ax.plot([0.01,1000],[0.01,1000],linewidth=1,color='black',ls='--') # plot
            # a dotted line increasing from bottom left to top right
            
#        ax.annotate('Spearman: %.3g, pval: %.2g' % (spear[0], spear[1]), 
#                    xy=(0.98, 0.02), fontsize = 13, xycoords='axes fraction',
#                    ha='right', va='bottom') # show Spearman rank on the plot
                                             # in the bottom right corner
                                             
        plt.show() # show the figure
#        showTermination() # confirm the process completed as expected
        return
    else :
#        showTermination() # confirm the process completed as expected
        return

#......................................................................all_corrs
def all_corrs(param, label, plots=True) :
    # the complete set of all correlations, besides "Rout" and "angsize"
    
    main(param, label, zz, 'zz', showplot=plots)
    main(param, label, K0, 'K0', showplot=plots)
    main(param, label, K100, 'K100', showplot=plots)
    main(param, label, Tx, 'Tx', showplot=plots)
    main(param, label, Lbol, 'Lbol', showplot=plots)
    main(param, label, LHa, 'LHa', showplot=plots)
    main(param, label, Lrad, 'Lrad', showplot=plots)
    
    main(param, label, eDen, 'eDen', showplot=plots)
    main(param, label, PLent, 'PLent', showplot=plots)
    main(param, label, flatent, 'flatent', showplot=plots)
    main(param, label, PLpress, 'PLpress', showplot=plots)
    main(param, label, flatpress, 'flatpress', showplot=plots)
    main(param, label, clusmass, 'clusmass', showplot=plots)
    main(param, label, clustemp, 'clustemp', showplot=plots)
    main(param, label, coolingtime52, 'coolingtime52', showplot=plots)
    main(param, label, coolingtime, 'coolingtime', showplot=plots)
    
    main(param, label, UVSFR, 'UVSFR', showplot=plots)
    main(param, label, IRSFR, 'IRSFR', showplot=plots)
    main(param, label, seventySFR, 'seventySFR', showplot=plots)
    main(param, label, twentyfourSFR, 'twentyfourSFR', showplot=plots)
    main(param, label, BCGmass, 'BCGmass', showplot=plots)
    
    main(param, label, asymm, 'asymm', logx=True, showplot=plots)
    main(param, label, clump, 'clump', logx=True, showplot=plots)
    main(param, label, concen, 'concen', logx=True, showplot=plots)
    
    main(param, label, sym, 'sym', logx=True, showplot=plots)
    main(param, label, peak, 'peak', logx=True, showplot=plots)
    main(param, label, align, 'align', logx=True, showplot=plots)
#    main(param, label, raff, 'cavpow') # individual cavity powers may have
#    main(param, label, cavag, 'cavpow') # insufficient entries for
#    main(param, label, osul, 'cavpow') # statistically significant analysis
#    main(param, label, hlava, ' cavpow')
    main(param, label, cavpow, 'cavpow', showplot=plots)
    
    return

#.........................................................................cavPow
def cavPow(yvals, ylab, ymin=None, ymax=None, linear=False,
           location='upper left') :
    # plots a parameter against the individual cavity powers, but all together
    
    global currentFig
    
    fig = plt.figure(currentFig)
    currentFig += 1
    plt.clf()
    
    ax = fig.add_subplot(111)
    
    ax.set_ylim(ymin, ymax)
    
    if linear == True :
        ax.semilogx(raff, yvals, 'ro', label = 'Rafferty et al. (2006)')
        ax.semilogx(cavag, yvals, 'go', label = 'Cavagnolo et al. (2010)')
        ax.semilogx(osul, yvals, 'bo', label = 'O’Sullivan et al. (2011)')
        ax.semilogx(hlava, yvals, 'ko', label='Hlavacek-Larrondo et al. (2012)')
    else :
        ax.loglog(raff, yvals, 'ro', label = 'Rafferty et al. (2006)')
        ax.loglog(cavag, yvals, 'go', label = 'Cavagnolo et al. (2010)')
        ax.loglog(osul, yvals, 'bo', label = 'O’Sullivan et al. (2011)')
        ax.loglog(hlava, yvals, 'ko', label = 'Hlavacek-Larrondo et al. (2012)')
    
    ax.set_xlabel('Cavity Power ($10^{42}$ ergs s$^{-1}$)', fontsize = 15)
    ax.set_ylabel('%s' % DICT[ylab], fontsize = 15)
    
    plt.legend(loc = location)
    plt.show()
    
    return

#....................................................................checkcommon
def checkcommon(param1, param2, noprint=False) :
    
    count = 0
    for i in range(241) :
        if (~np.isnan(param1[i])) and (~np.isnan(param2[i])) :
            count += 1
            print("%6g   %6g" % (param1[i], param2[i]) )
    
    if noprint==False :
        print("\nNumber in common is %g." % count)
    else :
        return count
    
    return

#....................................................................checknonnan
def checknonnan(param, noprint=False) :
    
    num = np.count_nonzero(~np.isnan(param)) # '~' inverts the bool matrix
    
    if noprint==False :
        print("\nNumber of non-nan elements is %g." % num)
    else :
        return num
    
    return

#...................................................................checkunique1
def checkunique1(param1, param2) :
    
    count = 0
    for i in range(241) :
        if (~np.isnan(param1[i])) or (~np.isnan(param2[i])) :
            count += 1
#            print("%6g   %6g" % (param1[i], param2[i]) )
#    print("\nNumber of unique elements is %g." % count)
    
    return count

#...................................................................checkunique2
def checkunique2(param1, param2) :
    
    count = 0
    count += checknonnan(param1, noprint=True)
    count += checknonnan(param2, noprint=True)
    count -= checkcommon(param1, param2, noprint=True)
    
#    print("\nNumber of unique elements is %g." % count)
    
    return count

#....................................................................checkunique
def checkunique(param1, param2) :
    
    num1 = checkunique1(param1, param2)
    num2 = checkunique2(param1, param2)
    
    if (num1 == num2) :
        print("\nNumber of unique elements is %g." % num1)
    else :
        print("\nError! The two checks did not return the same number of " +
              "unique elements.")
    
    return

#.....................................................................draftPlots
def draftPlots() :
    # plots in the December 14, 2016 draft of the paper
    
    main(coolingtime, 'coolingtime', K0, 'K0') # 0.531 7.8e-19
    main(coolingtime, 'coolingtime', IRSFR, 'IRSFR') # -0.000698 1
    main(coolingtime, 'coolingtime', UVSFR, 'UVSFR') # -0.24 0.011
    main(coolingtime, 'coolingtime', LHa, 'LHa') # -0.295 0.0016
    main(IRSFR, 'IRSFR', LHa, 'LHa') # 0.705 7.8e-07
    main(cavpow, 'cavpow', Lrad, 'Lrad') # 0.457 0.0018
    multi(Lrad, PLpress, Lrad, flatpress, 'Lrad', 'pressure', 'PL', 'flat')
#         0.524 3.5e-18 on average
    main(cavpow, 'cavpow', coolingtime, 'coolingtime') # -0.4 0.0072
    main(cavpow, 'cavpow', LHa, 'LHa') # 0.575 0.0017
    main(cavpow, 'cavpow', IRSFR, 'IRSFR') # 0.74 6.9e-06
    main(cavpow, 'cavpow', K0, 'K0') # 0.612 1e-05
    main(cavpow, 'cavpow', BCGmass, 'BCGmass') # 0.711 2.2e-05
    main(BCGmass,'BCGmass', zz,'zz') # 0.674 4.1e-10
    main(cavpow, 'cavpow', zz, 'zz') # 0.696 1.6e-07
    main(BCGmass, 'BCGmass', coolingtime, 'coolingtime') # 0.0978 0.43
    main(BCGmass, 'BCGmass',K0,'K0') # 0.524 5.4e-06
    main(zz, 'zz', K0, 'K0') # 0.355 1.5e-08
    main(BCGmass, 'BCGmass', IRSFR, 'IRSFR') # 0.503 1.4e-05
    main(concen, 'concen', peak, 'peak', linear=True) # 0.774 7.4e-09
    main(align, 'align', asymm, 'asymm', linear=True) # -0.544 0.00034
    main(sym, 'sym', asymm, 'asymm', linear=True) # -0.54 0.00038
    main(coolingtime, 'coolingtime', asymm, 'asymm', logx=True) # 0.37 8.1e-05
    main(K0, 'K0', asymm, 'asymm', logx=True) # 0.526 4.8e-09
    main(cavpow, 'cavpow', asymm, 'asymm', logx=True)
    
    # old versions of cavity power plots
#    cavPow(Lrad, 'Lrad')
#    cavPow(coolingtime, 'coolingtime')
#    cavPow(LHa, 'LHa')
#    cavPow(IRSFR, 'IRSFR')
#    cavPow(K0, 'K0')
#    cavPow(BCGmass, 'BCGmass')
#    cavPow(zz, 'zz')
#    cavPow(asymm, 'asymm', location='lower left')
    
    return

#............................................................................fit
def fit(param1, param2, lin=False) :
    
    from scipy.optimize import curve_fit
    
    x, y = getcommon(param1, param2) # get the common values that aren't nans
    xs = np.linspace(min(x), max(x), 1000)
    if (lin == True) :
        popt, pcov = curve_fit(linear, x, y)
    else :
        logparam1, logparam2 = np.log10(x), np.log10(y) # this will break for
                                                        # any values of 0
        popt, pcov = curve_fit(linear, logparam1, logparam2)
#    perr = np.sqrt( np.diag(pcov) )

#    badfit1 = linear(popt[0]+perr[0], xs, popt[1]-perr[1])
#    badfit2 = linear(popt[0]-perr[0], xs, popt[1]+perr[1])
    
    return popt[0], popt[1], xs

#......................................................................getcommon
def getcommon(param1, param2) :
    
    newList1 = []
    newList2 = []
    for i in range(241) :
        if (~np.isnan(param1[i])) and (~np.isnan(param2[i])) :
            newList1.append(param1[i])
            newList2.append(param2[i])
    
    return newList1, newList2

#.........................................................................linear
def linear(m, x, b) : # helper function for fit function
        return m*x + b

#...........................................................................misc
def misc() :
    # miscellaneous functions that are sometimes helpful
    
    print(np.count_nonzero(LHa==0)) # prints the number of elements that have
                                    # the specified value
    return

#..........................................................................multi
def multi(xvals1, yvals1, xvals2, yvals2, xaxislabel, yaxislabel, 
          legend1, legend2, xmin=None, xmax=None, ymin=None,
          ymax=None, location='upper right') :
    
    global currentFig
    spear1 = sp.spearmanr(xvals1, yvals1, nan_policy='omit')
    spear2 = sp.spearmanr(xvals2, yvals2, nan_policy='omit')
    print("Figure %2.1d   Spearman: %6.3g   pvalue: %8.2g" % 
        (currentFig, spear1[0], spear1[1]) )
    print("Figure %2.1d   Spearman: %6.3g   pvalue: %8.2g" % 
        (currentFig, spear2[0], spear2[1]) )
        
    fig = plt.figure(currentFig)  # the current figure
    currentFig += 1
    plt.clf()
    
    ax = fig.add_subplot(111)
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    
    ax.loglog(xvals1, yvals1, 'bo', label = "%s" % DICT[legend1] )
    ax.loglog(xvals2, yvals2, 'ro', label = "%s" % DICT[legend2] )
    
    ax.set_xlabel("%s" % DICT[xaxislabel], fontsize = 15 )
    ax.set_ylabel("%s" % DICT[yaxislabel], fontsize = 15 )
    
    plt.legend(loc = location)
    
    ax.annotate('Power Law Spearman: %.3g, pval: %.2g' % (spear1[0], spear1[1]), 
                xy=(0.98, 0.05), fontsize = 13, xycoords='axes fraction',
                ha='right', va='bottom')
    ax.annotate('Flat Spearman: %.3g, pval: %.2g' % (spear2[0], spear2[1]), 
                xy=(0.98, 0.02), fontsize = 13, xycoords='axes fraction',
                ha='right', va='bottom')
    
    plt.show()
    
    return

#...................................................................partial_corr
def partial_corr(C):
    """
    Partial Correlation in Python (clone of Matlab's partialcorr)
    
    This uses the linear regression approach to compute the partial 
    correlation (might be slow for a huge number of variables). The 
    algorithm is detailed here:
    
        http://en.wikipedia.org/wiki/Partial_correlation#Using_linear_regression
    
    Taking X and Y two variables of interest and Z the matrix with all
    the variable minus {X, Y}, the algorithm can be summarized as
    
        1) perform a normal linear least-squares regression with X as the target
           and Z as the predictor
        2) calculate the residuals in Step #1
        3) perform a normal linear least-squares regression with Y as the target
           and Z as the predictor
        4) calculate the residuals in Step #3
        5) calculate the correlation coefficient between the residuals from
           Steps #2 and #4; 
    
        The result is the partial correlation between X and Y while controlling
        for the effect of Z.
    
    Date: Nov 2014
    Author: Fabian Pedregosa-Izquierdo, f@bianp.net
    Testing: Valentina Borghesani, valentinaborghesani@gmail.com
    """
    """
    Returns the sample linear partial correlation coefficients between pairs of
    variables in C, controlling for the remaining variables in C.
    
    Parameters
    ----------
    C : array-like, shape (n, p)
        Array with the different variables. Each column of C is taken as a
        variable
    
    Returns
    -------
    P : array-like, shape (p, p)
        P[i, j] contains the partial correlation of C[:, i] and C[:, j]
        controlling for the remaining variables in C.
    """
    
    C = np.asarray(C)
    p = C.shape[1]
    P_corr = np.zeros((p, p), dtype=np.float)
    for i in range(p):
        P_corr[i, i] = 1
        for j in range(i+1, p):
            idx = np.ones(p, dtype=np.bool)
            idx[i] = False
            idx[j] = False
            beta_i = linalg.lstsq(C[:, idx], C[:, j])[0]
            beta_j = linalg.lstsq(C[:, idx], C[:, i])[0]
            
            res_j = C[:, j] - C[:, idx].dot(beta_i)
            res_i = C[:, i] - C[:, idx].dot(beta_j)
            
#            corr = sp.pearsonr(res_i, res_j)[0]
            corr = sp.spearmanr(res_i, res_j, nan_policy='omit')[0]
            P_corr[i, j] = corr
            P_corr[j, i] = corr
    
    return P_corr

#.........................................................................p_corr
def p_corr(param1, param2) :
    """
    Create a master mask based on the two input arrays, then mask those two
    arrays and then remove the masked entries. Finally create a 2D array of the
    two input arrays, where they are columns, and then calculate the partial
    correlation as seen in partial_corr.
    """
    
    newmask = (~np.isnan(param1)) & (~np.isnan(param2))
    
    new_param1 = np.ma.array(param1, mask=~newmask)
    new_param2 = np.ma.array(param2, mask=~newmask)
    
    onlydata1 = np.ma.compressed(new_param1)
    onlydata2 = np.ma.compressed(new_param2)
    
    matrix = np.column_stack( (onlydata1,onlydata2) )
    #print(matrix)
    
    partial = partial_corr(matrix)
    print(partial)
    
    return

#................................................................showTermination
def showTermination() :
    """
    This function prints a final message identifying the programmer,
    giving the date, and saying the program has finished.
    """
    print("\nProgrammed by Cam Lawlor-Forsyth")
    print( "Date: " + ctime() )
    print("End of processing")
    return
#...............................................................end of functions

# print a table of the CAS and SPA parameters
#count = 0
#for i in range(241) :
#    if (np.isnan(clump[i])==False) and (np.isnan(sym[i])==False) :
#        count += 1
#        print("%6g   %9g   %9g   %5g    %4g   %5g" % (concen[i], asymm[i],
#                                                      clump[i], sym[i],
#                                                      align[i], peak[i]) )
#print(count)

# test the partial correlation function
#p_corr(Lrad, PLpress)
#main(PLpress, "PLpress", Lrad, "Lrad", errors=False)

