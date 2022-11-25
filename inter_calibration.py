import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyROA.PyROA import InterCalibrate
import os


class InterCalibrator(object):

    """Intercalibrator for the light curves"""

    def __init__(self, datacsv, objName, datadir='tmp/'):
        """Initializes the intercalibrator

        :datacsv: csv with the lightcurves
        :objName: The object name
        :scopes: List of telescope names
        :datadir: Data where the temporary files will be located

        """
        self._datacsv = datacsv
        self._datadir = datadir
        self._objName = objName
        self._results = {}

        # Prepare the temporary files
        self._data = pd.read_csv(datacsv)
        self._bands = np.unique(self._data['Filter'])
        self._scopes = np.unique(self._data['Tel'])

        # make sure the folder exists
        if not os.path.isdir(self._datadir):
            os.mkdir(self._datadir)
        for band in self._bands:
            band_data = self._data[self._data['Filter'] == band]
            for scope in self._scopes:
                scope_data = self._data[self._data['Tel'] == band_data]
                filename = os.path.join(
                    self._datadir, f'{self._objName}_{band}_{scope}.dat')
                scope_data = scope_data[['MJD', 'Flux', 'Error']]
                scope_data.to_csv(filename, index=False, header=False, sep=' ')

    def calibrate(self, filt, **kwargs):
        """Does the intercalibration for a given band and priors. Passes kwargs to PyROA
        InterCalibrate

        :filter: filter to do the intercalibration in

        """
        fit = InterCalibrate(
            self._datadir, self._objName, filt, self._scopes, **kwargs)
        self._results[filt]=fit

    def plot_results(self, f, save_dir='figures'):
        """ Plots the uncalibrated lightcurves along with the calibrated joined curve

        :f: Filter to plot
        """
        plt.rcParams.update({
            "font.family": "Sans",
            "font.serif": ["DejaVu"],
            "figure.figsize": [20, 10],
            "font.size": 20})

        # Read in original lightcurves
        data=[]
        for i in range(len(self._scopes)):
            file=self._datadir + \
                str(self._objName) + "_" + str(f) + \
                "_" + str(self._scopes[i]) + ".dat"
            data.append(np.loadtxt(file))

        plt.title(str(f))
        # Plot data for filter
        for i in range(len(data)):
            mjd=data[i][:, 0]
            flux=data[i][:, 1]
            err=data[i][:, 2]
            plt.errorbar(mjd, flux, yerr=err, ls='none',
                         marker=".", label=str(self._scopes[i]), alpha=0.5)

        fit=self._results[f]
        plt.errorbar(fit.mjd, fit.flux, yerr=fit.err, ls='none',
                     marker=".", color="black", label="Calibrated")

        plt.xlabel("mjd")
        plt.ylabel("Flux")
        plt.legend()
        plt.savefig(os.path.join(save_dir),
                    f'intercalibration_{self._objName}_{f}.png')
        plt.show()
