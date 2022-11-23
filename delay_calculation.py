import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import PyROA
import os


class DelayCalculator(object):

    """Calculates the delay for a given object"""

    def __init__(self, data_dir, objName):
        """Initializes the class

        :data_dir: folder containing the calibrated data

        """
        self._data_dir = data_dir
        self._objName = objName
        self.delays = None

    def find_delays(self, filters, **kwargs
                    ):
        """Finds the delay for the given filters

        :filters: list of filters
        :priors: priors for the mcmc

        """
        pass
        fit = PyROA.Fit(self._data_dir, self._objName, filters, **kwargs)

        self.delays = fit

        return self.delays
