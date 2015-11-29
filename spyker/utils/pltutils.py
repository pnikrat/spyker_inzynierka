import numpy as np

import scipy.io.wavfile
import matplotlib.pyplot as plt

from spyker.model.charts import stft
from spyker.utils.constants import RECS_DIR


def plot_function(fig, data, time=None, **labels):
    fig.clear()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel(labels.get('xlabel'))
    ax.set_ylabel(labels.get('ylabel'))

    if len(labels) == 2:
        ax.plot(time, data)
    elif len(labels) == 3:
        pax = ax.pcolormesh(data)
        cbar = fig.colorbar(pax)
        cbar.ax.set_ylabel(labels.get('zlabel'))
        ax.autoscale(enable=True, axis='both', tight=True)

