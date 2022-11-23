import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_lightcurves(csv, filename, filters=['u', 'B', 'g', 'V', 'r', 'i', 'z']):
    data = pd.read_csv(csv)

    fig, axs = plt.subplots(7, figsize=(12, 16))
    color_array = ['blue', 'c', 'teal', 'green',
                   'orange', 'red', 'firebrick', 'black']
    fig.suptitle('Curvas de luz sin calibrar')
    for i, band in enumerate(filters):
        band_data = data[data['Filter'] == band]
        axs[i].errorbar(band_data.MJD, band_data.Flux, band_data.Error, fmt='.',
                        ecolor='gray', ms=5, elinewidth=0.4, c=color_array[i])
    fig.savefig(filename)
