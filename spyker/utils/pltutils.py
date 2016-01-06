from matplotlib import cm
# noinspection PyUnresolvedReferences
from mpl_toolkits.mplot3d import Axes3D
from spyker.model.draggableplots import DraggableLine
import matplotlib.pyplot as plt
import numpy as np


def plot_function(fig, data, clear=True):
    if clear:
        fig.clear()

    x_vector = data['x_vector']
    y_vector = data['y_vector']

    ax = fig.add_subplot(1, 1, 1)

    labels = data['labels']

    ax.set_xlabel(labels['xlabel'])
    ax.set_ylabel(labels['ylabel'])

    if 'cursors' in data:
        for x in data['cursors']:
            ly = ax.axvline(color='r')
            ly.set_xdata(x)

    if len(labels) == 2:
        ax.plot(x_vector, y_vector, label=data['legend'])
        ax.legend()
    elif len(labels) == 3:
        pax = ax.pcolormesh(y_vector)
        cbar = fig.colorbar(pax)
        cbar.ax.set_ylabel(labels['zlabel'])
        ax.autoscale(enable=True, axis='both', tight=True)
        
    if 'yticks' in data:
        yticks = data['yticks']
        ylocs = yticks['locs']
        ylabels = yticks['labels']
        plt.yticks(ylocs, ylabels)

    if 'xticks' in data:
        xticks = data['xticks']
        xlocs = xticks['locs']
        xlabels = xticks['labels']
        plt.xticks(xlocs, xlabels, rotation='vertical')

    fig.savefig('samplefigure', bbox_inches='tight')


def plt_single(fig, data, nr, xory):
    fig.clear()
    ax = fig.add_subplot(1, 1, 1)

    labels = data['labels']
    ax.set_ylabel(labels.get('zlabel'))

    if xory == 'x':
        ax.set_xlabel(labels.get('ylabel'))
        y_vector = data['y_vector'][:, nr]
        ax.plot(y_vector)

    elif xory == 'y':
        ax.set_xlabel(labels.get('xlabel'))
        y_vector = data['y_vector'][nr]
        ax.plot(y_vector)
    fig.savefig('samplefigure', bbox_inches='tight')


def plot_3d(fig, data):
    fig.clear()

    x_vector = data['x_vector']
    ax = fig.gca(projection='3d')
    z_vector = data['y_vector']  # podmiana wektorow (przekazuje spectrum w y_vector aby zgadzalo sie z plt_single)
    y_vector = data['z_vector']

    labels = data['labels']

    ax.set_xlabel(labels.get('xlabel'))
    ax.set_ylabel(labels.get('ylabel'))

    ax.autoscale(enable=True, axis='both', tight=True)
    surf = ax.plot_surface(y_vector, x_vector, z_vector, rstride=2, cstride=2, cmap=cm.coolwarm, linewidth=0)
    fig.colorbar(surf)
    fig.savefig('samplefigure', bbox_inches='tight')


def plot_trimmable(fig, data):
    fig.clear()

    x_vector = data['x_vector']
    y_vector = data['y_vector']

    ax = fig.add_subplot(1, 1, 1)

    labels = data['labels']

    ax.set_xlabel(labels.get('xlabel'))
    ax.set_ylabel(labels.get('ylabel'))

    ax.plot(x_vector, y_vector)
    slider1XPos, slider2XPos, interval = data['sliders']
    leftline = ax.axvline(x=slider1XPos, color='r', linewidth=4)
    rightline = ax.axvline(x=slider2XPos, color='r', linewidth=4)

    h = DraggableLine(leftline, rightline, interval)
    h.connect()
    fig.tight_layout()
    return h  # need to return handlers, otherwise they are garbage collected and user cant move sliders
