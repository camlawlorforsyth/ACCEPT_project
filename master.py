# -*- coding: utf-8 -*-
"""
    SUMMER RESEARCH 2016/2017/2018
    ASSIGNMENT: Plot correlations
    AUTHOR:     Cam Lawlor-Forsyth (lawlorfc@myumanitoba.ca)
    SUPERVISOR: Chris O'Dea
    VERSION:    2019-Mar-25
    
    PURPOSE: Plot various parameters from multiple data tables while
             calculating Spearman rank correlations and associated p-values
             using SciPy.
"""

# imports
import numpy as np

from astropy.io import ascii
#import linmix
#import matplotlib as mpl # for publication-quality plots
#mpl.rcParams['font.serif'] = "Times New Roman"
#mpl.rcParams['font.family'] = "serif"
#mpl.rcParams['text.usetex'] = False # have to install LaTeX and then set to True
import matplotlib.pyplot as plt
import scipy.stats as sp
from scipy import linalg
from time import ctime
import warnings
warnings.filterwarnings("ignore", category = RuntimeWarning) # ignore warnings

# read in data from sample catalog
dat = ascii.read('accept_catalog.csv') # requires columns to have unique names

zz, K0, K100, Tx = dat['z'], dat['K0'], dat['K100'], dat['Tx']
Lbol, LHa, Lrad = dat['Lbol'], dat['LHa'], dat['Lrad']

# these values are for an annulus with inner radius ~20 kpc
Rin, Rout, eDen, PLent = dat['Rin'], dat['Rout'], dat['nelec'], dat['Kitpl']
flatent, PLpress, flatpress = dat['Kflat'], dat['Pitpl'], dat['Pflat']
clusmass, clustemp = dat['Mgrav'], dat['clustemp']
coolingtime52, coolingtime = dat['tcool5/2'], dat['tcool3/2']

UVSFR, IRSFR, seventySFR = dat['UVSFR'], dat['IRSFR'], dat['70SFR']
twentyfourSFR, BCGmass = dat['24SFR'], dat['BCGmass']

ROIout, ansize = dat['ROIout'], dat['D_A']
asymm, clump, concen = dat['asymm_v0'], dat['clumpy_v0'], dat['concen_v0']

sym, peak, align = dat['Symmetry'], dat['Peakiness'], dat['Alignment']
cavpow = dat['completeCavPow']

BCGalt, SFRalt = dat['BCG_Stellar_Mass'], dat['BCG_SFR']

tcool = dat['alt_tcool']

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
        'eDen':'Electron Density (cm$^{-3}$)',
        'PLent':'Entropy using a Power Law (keV$\cdot$cm$^2$)',
        'flatent':'Entropy using a Flat Relation (keV$\cdot$cm$^2$)',
        'PLpress':'Pressure (dyne cm$^{-2}$)', #'Pressure (Power Law)',
        'flatpress':'Pressure (dyne cm$^{-2}$)', #'Pressure (Flat Relation)',
        'clusmass':'Cluster Mass ($M_\odot$)',
        'clustemp':'Cluster X-ray Temperature (keV)',
        'coolingtime52':'Cooling Time using the 5/2 Model (Gyr)', # 5*0.6 = 3
        'coolingtime':'Cooling Time (Gyr)', # uses the 3/2 model
        
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
        'BCGalt':'BCG Stellar Mass ($10^{10} \/ M_\odot$)\nfrom F-M+ (2014)',
        'SFRalt':'SFR ($M_\odot$ yr$^{-1}$)\nfrom F-M+ (2014)',
        
        # general axes titles and legend entries for mutli-plots
        'pressure':'Pressure (dyne cm$^{-2}$)',
        'PL':'Power Law Model',
        'flat':'Flat Relation Model'
        }

# dictionary to access associated errors
UNCERTS = {
           'zz':dat['z_err'], # zz_err, # NEED TO FINISH GETTING
           'K0':dat['K0_err'], # NEED TO FINISH GETTING
           'K100':dat['K100_err'], # NEED TO FINISH GETTING
           'Tx':dat['Tx_err'], # error for Tx: standard dev. of individual temps # FINISH GETTING
           'Lbol':dat['Lbol_err'],
           'LHa':dat['LHa_err'],
           'Lrad':dat['Lrad_err'],
           
           'eDen':dat['nelec_err'],
           'PLent':dat['K_err'],
           'flatent':dat['K_err'],
           'PLpress':dat['Perr'],
           'flatpress':dat['Perr'],
           'clusmass':dat['Mgrav_err'],
           'clustemp':dat['clustemp_err'],
           'coolingtime52':dat['t52err'],
           'coolingtime':dat['t32err'],
           
           'UVSFR':dat['UVerr'],
           'IRSFR':dat['IR_err'], # no error for IRSFR, therefore equal to 0
           'seventySFR':dat['70err'],
           'twentyfourSFR':dat['24err'],
           'BCGmass':dat['BCGmass_err'], # no error for BCGmass, therefore equal to 0
           
           'asymm':dat['asymm_v0_err'], # no errors for asymm yet
           'clump':dat['clump_v0_err'], # no errors for clump yet
           'concen':dat['concen_v0_err'], # no errors for concen yet
           
           'sym':dat['Symm_err'],
           'peak':dat['Peak_err'],
           'align':dat['Align_err'],
           'cavpow':[dat['complete_err_low'],dat['complete_err_high']],
           
           'BCGalt':[dat['mass_low'],dat['mass_high']],
           'SFRalt':[dat['SFR_low'],dat['SFR_high']]
          }

# constants
currentFig = 1 # first figure will be numbered as 'Figure 1'

#..........................................................................main
def main(xvals, xlab, yvals, ylab, xmin=None, xmax=None, ymin=None,
         ymax=None, logx=False, logy=False, linear=False, errors=True,
         showplot=True, printfit=False) :
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
#                slope, intercept, xx = fit(xvals, yvals, lin=True,
#                                           show_mb=printfit)
#                ax.plot(xx, slope*xx + intercept, 'r-')
            elif (logx == True) and (logy == True) and (linear == False) :
                ax.loglog(xvals, yvals, 'ko') # use loglog for power laws
            else :
                ax.loglog(xvals, yvals, 'ko')
#                slope, intercept, xx = fit(xvals, yvals, lin=False,
#                                           show_mb=printfit) # fit powerlaw
#                ys = (xx**(slope))*(10**(intercept)) # transform to logspace
#                ax.loglog(xx, ys, 'k-') # plot the powerlaw
#                theoreticals = (xx**(2/3))*(10**(intercept)) # for tcool vs K0
#                ax.loglog(xx, theoreticals, 'r-')
        else :
            if (logx == True) and (logy == False) and (linear == False) :
                ax.set_xscale('log')
                ax.set_yscale('linear')
                ax.errorbar(xvals, yvals, xerr=UNCERTS[xlab],
                            yerr=UNCERTS[ylab], fmt='ko', elinewidth=0.3,
                            capsize=1.5, errorevery=1)
            elif (logx == False) and (logy == True) and (linear == False) :
                ax.set_xscale('linear')
                ax.set_yscale('log')
                ax.errorbar(xvals, yvals, xerr=UNCERTS[xlab],
                            yerr=UNCERTS[ylab], fmt='ko', elinewidth=0.3,
                            capsize=1.5, errorevery=1)
            elif (logx == False) and (logy == False) and (linear == True) :
                ax.set_xscale('linear')
                ax.set_yscale('linear')
                ax.errorbar(xvals, yvals, xerr=UNCERTS[xlab],
                            yerr=UNCERTS[ylab], fmt='ko', elinewidth=0.3,
                            capsize=1.5, errorevery=1)
            elif (logx == True) and (logy == True) and (linear == False) :
                ax.set_xscale('log')
                ax.set_yscale('log')
                ax.errorbar(xvals, yvals, xerr=UNCERTS[xlab],
                            yerr=UNCERTS[ylab], fmt='ko', elinewidth=0.3,
                            capsize=1.5, errorevery=1)
            else :
                ax.set_xscale('log')
                ax.set_yscale('log')
                ax.errorbar(xvals, yvals, xerr=UNCERTS[xlab],
                            yerr=UNCERTS[ylab], fmt='ko', elinewidth=0.3,
                            capsize=1.5, errorevery=1)
        
        ax.set_xlabel("%s" % DICT[xlab], fontsize = 15 )
        ax.set_ylabel("%s" % DICT[ylab], fontsize = 15 )
        
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        
    #    ax.plot([0.01,1000],[0.01,1000],linewidth=1,color='black',ls='--')
            # plot a dotted line increasing from bottom left to top right
            
#        ax.annotate('Spearman: %.3g, pval: %.2g' % (spear[0], spear[1]), 
#                    xy=(0.98, 0.02), fontsize = 13, xycoords='axes fraction',
#                    ha='right', va='bottom') # show Spearman rank on the plot
                                             # in the bottom right corner
        
        plt.tight_layout()
        plt.show() # show the figure
#        showTermination() # confirm the process completed as expected
        return
    else :
#        showTermination() # confirm the process completed as expected
        return

#.....................................................................all_corrs
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

#........................................................................cavPow
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
        ax.semilogx(hlava, yvals, 'ko',
                    label='Hlavacek-Larrondo et al. (2012)')
    else :
        ax.loglog(raff, yvals, 'ro', label = 'Rafferty et al. (2006)')
        ax.loglog(cavag, yvals, 'go', label = 'Cavagnolo et al. (2010)')
        ax.loglog(osul, yvals, 'bo', label = 'O’Sullivan et al. (2011)')
        ax.loglog(hlava, yvals, 'ko',
                  label = 'Hlavacek-Larrondo et al. (2012)')
    
    ax.set_xlabel('Cavity Power ($10^{42}$ ergs s$^{-1}$)', fontsize = 15)
    ax.set_ylabel('%s' % DICT[ylab], fontsize = 15)
    
    plt.legend(loc = location)
    
    plt.tight_layout()
    plt.show()
    
    return

#...................................................................checkcommon
def checkcommon(param1, param2, noprint=False) :
    
    count = 0
    for i in range(len(param1)) :
        if (~np.isnan(param1[i])) and (~np.isnan(param2[i])) :
            count += 1
            print("%6g   %6g" % (param1[i], param2[i]) )
    
    if noprint==False :
        print("\nNumber in common is %g." % count)
    else :
        return count
    
    return

#...................................................................checknonnan
def checknonnan(param, noprint=False) :
    
    num = np.count_nonzero(~np.isnan(param)) # '~' inverts the bool matrix
    
    if noprint==False :
        print("\nNumber of non-nan elements is %g." % num)
    else :
        return num
    
    return

#..................................................................checkunique1
def checkunique1(param1, param2) :
    
    count = 0
    for i in range(len(param1)) :
        if (~np.isnan(param1[i])) or (~np.isnan(param2[i])) :
            count += 1
#            print("%6g   %6g" % (param1[i], param2[i]) )
#    print("\nNumber of unique elements is %g." % count)
    
    return count

#..................................................................checkunique2
def checkunique2(param1, param2) :
    
    count = 0
    count += checknonnan(param1, noprint=True)
    count += checknonnan(param2, noprint=True)
    count -= checkcommon(param1, param2, noprint=True)
    
#    print("\nNumber of unique elements is %g." % count)
    
    return count

#...................................................................checkunique
def checkunique(param1, param2) :
    
    num1 = checkunique1(param1, param2)
    num2 = checkunique2(param1, param2)
    
    if (num1 == num2) :
        print("\nNumber of unique elements is %g." % num1)
    else :
        print("\nError! The two checks did not return the same number of " +
              "unique elements.")
    
    return

#....................................................................delete_val
def delete_val(param1, param2, param_of_interest, value) :
    
    badIndex = np.where(param_of_interest == value)
    
    newparam1 = np.delete(param1, badIndex)
    newparam2 = np.delete(param2, badIndex)
    
    return newparam1, newparam2

#....................................................................draftPlots
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

#...........................................................................fit
def fit(param1, param2, lin=False, show_mb=False) :
    
    from scipy.optimize import curve_fit
    
    x, y = getcommon(param1, param2) # get the common values that aren't nans
    xs = np.linspace(min(x), max(x), 1000)
    if (lin == True) :
        popt, pcov = curve_fit(linear, x, y)
    else :
        logparam1, logparam2 = np.log10(x), np.log10(y) # this will break for
                                                        # any values of 0
        popt, pcov = curve_fit(linear, logparam1, logparam2)
    perr = np.sqrt( np.diag(pcov) )
    
    if show_mb == True :
        print('\nSlope: %.3g +/- %.1g' % (popt[0], perr[0]) )
        print('Intercept: %.3g +/- %.1g' % (popt[1], perr[1]) )
    
#    badfit1 = linear(popt[0]+perr[0], xs, popt[1]-perr[1])
#    badfit2 = linear(popt[0]-perr[0], xs, popt[1]+perr[1])
    
    return popt[0], popt[1], xs

#.....................................................................getcommon
def getcommon(param1, param2) :
    
    newList1 = []
    newList2 = []
    for i in range(len(param1)) :
        if (~np.isnan(param1[i])) and (~np.isnan(param2[i])) :
            newList1.append(param1[i])
            newList2.append(param2[i])
    
    return newList1, newList2

#.........................................................................histo
def histo(param, label, num_bins) :
    
    global currentFig
    fig = plt.figure(currentFig)
    currentFig += 1
    plt.clf()
    
    vals, dummy_vals = getcommon(param, param)
    
    ax = fig.add_subplot(111)
    ax.hist(vals, bins=num_bins, density=True, color='k')
    plt.xlabel("%s" % DICT[label], fontsize = 15)
    
    plt.tight_layout()
    plt.show()
    
    return

#........................................................................linear
def linear(m, x, b) : # helper function for fit function
        return m*x + b

#...................................................................linmix_test
def linmix_test() :
    
#    main(K0, 'K0', coolingtime, 'coolingtime') # for comparison
    
    newK0_err, newct_err = delete_val(K0_err, ct_err, K0, 0)
    newK0, newcoolingtime = delete_val(K0, coolingtime, K0, 0)
    
    logK0 = np.log10(newK0)
    logK0_err = np.log10(newK0_err)
    logct = np.log10(newcoolingtime)
    logct_err = np.log10(newct_err)
    
    lm = linmix.LinMix(logK0, logct, logK0_err, logct_err)
    lm.run_mcmc(silent=True)
    
    global currentFig    
    fig = plt.figure(currentFig)
    currentFig += 1
    plt.clf()
    ax = fig.add_subplot(111)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.errorbar(newK0, newcoolingtime, xerr=newK0_err, yerr=newct_err,
                fmt='ko', elinewidth=0.3, capsize=1.5, errorevery=1)
    
#    slope = lm.chain['alpha']
#    intercept = lm.chain['beta']
    
#    xs = np.linspace(min(newK0), max(newK0), 1000)
#    ys = (xs**(slope))*(10**(intercept)) # transform to logspace
#    ax.loglog(xs, ys, 'r-') # plot the powerlaw
#    theoreticals = (xs**(2/3))*(10**(intercept)) # for tcool vs K0
#    ax.loglog(xs, theoreticals, 'r-')
    
    ax.set_xlabel("%s" % DICT['K0'], fontsize = 15 )
    ax.set_ylabel("%s" % DICT['coolingtime'], fontsize = 15 )
    
    plt.tight_layout()
    plt.show()
    
    return

#..........................................................................misc
def misc() :
    # miscellaneous functions that are sometimes helpful
    
    print(np.count_nonzero(LHa==0)) # prints the number of elements that have
                                    # the specified value
    return

#.........................................................................multi
def multi(xvals, xlab, yvals1, ylab1, yvals2, ylab2, #legend1, legend2,
          xmin=None, xmax=None, ymin=None,
          ymax=None, location='upper right') :
    
    global currentFig
    spear1 = sp.spearmanr(xvals, yvals1, nan_policy='omit')
    spear2 = sp.spearmanr(xvals, yvals2, nan_policy='omit')
    print("Figure %2.1d   Spearman: %6.3g   pvalue: %8.2g" % 
        (currentFig, spear1[0], spear1[1]) )
    print("Figure %2.1d   Spearman: %6.3g   pvalue: %8.2g" % 
        (currentFig, spear2[0], spear2[1]) )
        
    fig = plt.figure(currentFig)  # the current figure
    currentFig += 1
    plt.clf()
    
    ax = fig.add_subplot(111)
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.errorbar(xvals, yvals1, xerr=UNCERTS[xlab],
                yerr=UNCERTS[ylab1], fmt='ko', elinewidth=0.3,
                capsize=1.5, errorevery=1, label = "%s" % DICT[ylab1])
    ax.errorbar(xvals, yvals2, xerr=UNCERTS[xlab],
                yerr=UNCERTS[ylab2], fmt='ro', elinewidth=0.3,
                capsize=1.5, errorevery=1, label = "%s" % DICT[ylab2])
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    
    ax.set_xlabel("%s" % DICT[xlab], fontsize = 15 )
    ax.set_ylabel("%s" % DICT[ylab1], fontsize = 15 )
    
    plt.legend(loc = location)
    
#    ax.annotate('Power Law Spearman: %.3g, pval: %.2g' %(spear1[0], spear1[1]), 
#                xy=(0.98, 0.05), fontsize = 13, xycoords='axes fraction',
#                ha='right', va='bottom')
#    ax.annotate('Flat Spearman: %.3g, pval: %.2g' % (spear2[0], spear2[1]), 
#                xy=(0.98, 0.02), fontsize = 13, xycoords='axes fraction',
#                ha='right', va='bottom')
    
    plt.tight_layout()
    plt.show()
    
    return

#..................................................................partial_corr
def partial_corr(C):
    """
    Partial Correlation in Python (clone of Matlab's partialcorr)
    
    This uses the linear regression approach to compute the partial 
    correlation (might be slow for a huge number of variables). The 
    algorithm is detailed here:
    
    http://en.wikipedia.org/wiki/Partial_correlation#Using_linear_regression
    
    Taking X and Y two variables of interest and Z the matrix with all
    the variable minus {X, Y}, the algorithm can be summarized as
    
        1) perform a normal linear least-squares regression with X as the
           target and Z as the predictor
        2) calculate the residuals in Step #1
        3) perform a normal linear least-squares regression with Y as the
           target and Z as the predictor
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

#........................................................................p_corr
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

#...............................................................showTermination
def showTermination() :
    """
    This function prints a final message identifying the programmer,
    giving the date, and saying the program has finished.
    """
    print("\nProgrammed by Cam Lawlor-Forsyth")
    print( "Date: " + ctime() )
    print("End of processing")
    return
#..............................................................end of functions

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
