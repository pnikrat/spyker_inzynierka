from matplotlib import cm
# noinspection PyUnresolvedReferences
from mpl_toolkits.mplot3d import Axes3D
from spyker.model.draggableplots import DraggableLine
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
        ax.set_yticks(ylocs)
        ax.set_yticklabels(ylabels)

    if 'xticks' in data:
        xticks = data['xticks']
        xlocs = xticks['locs']
        xlabels = xticks['labels']
        ax.set_xticks(xlocs)
        ax.set_xticklabels(xlabels)

    if 'logarithmic' in data:
        ax.set_yscale('log')

    fig.tight_layout()
    # fig.savefig('samplefigure', bbox_inches='tight')


def plt_single_line(fig, data, nr, x_or_y, main_plot_fig, is_3d):
    fig.clear()
    ax = fig.add_subplot(1, 1, 1)

    labels = data['labels']
    ax.set_ylabel(labels.get('zlabel'))

    if x_or_y == 'x':
        if is_3d:  # dla stft 3D
            ax.set_xlabel(labels.get('xlabel'))
            y_vector = data['y_vector'][:, nr]
            x_vector = data['z_vector']
            ax.plot(x_vector, y_vector)
        else:  # dla stft i mffc
            ax.set_xlabel(labels.get('ylabel'))
            y_vector = data['y_vector'][:, nr]
            ax.plot(y_vector)

    elif x_or_y == 'y':
        if is_3d:
            ax.set_xlabel(labels.get('ylabel'))
            y_vector = data['y_vector'][nr]
            x_vector = data['x_vector'][0]
            ax.plot(x_vector, y_vector)
        else:
            ax.set_xlabel(labels.get('xlabel'))
            y_vector = data['y_vector'][nr]
            ax.plot(y_vector)
    fig.tight_layout()
        # fig.savefig('samplefigure', bbox_inches='tight')


def plot_cursor(main_plot_fig, data, nr, x_or_y, is_3d):
    ax = main_plot_fig.axes[0]
    if (is_3d):
        plot_3d_cursor(ax, data, nr, x_or_y)
    else:
        plot_2d_cursor(ax, data, nr, x_or_y)


def plot_3d_cursor(ax, data, nr, x_or_y):
    if ax.lines:
        ax.lines.pop(0)  # remove previous line

    if x_or_y == 'x':  # kroje w czasie i mam czestotliwosc na poziomej
        x = np.linspace(0, data['z_vector'][-1], len(data['z_vector']))
        element = data['x_vector'][:, nr][0]
        y = [element] * len(x)

    else:  # kroje w czestotliwosci i mam czas na poziomej
        y = data['x_vector'][0]
        element = data['z_vector'][nr, :][0]
        x = [element] * len(y)

    ax.plot(x, y, 1, 'r-')


def plot_2d_cursor(ax, data, nr, x_or_y):
    if ax.lines:
        ax.lines.pop(0)  # remove previous line
    if x_or_y == 'x':
        x = [nr, nr]
        y = [0, len(data['y_vector'])]
    else:
        x = [0, len(data['y_vector'][nr])]
        y = [nr, nr]

    ax.plot(x, y, 'r-')


def plot_3d(fig, data):
    fig.clear()

    x_vector = data['x_vector']
    ax = fig.gca(projection='3d')
    z_vector = data['y_vector']  # podmiana wektorow (przekazuje spectrum w y_vector aby zgadzalo sie z plt_single)
    y_vector = data['z_vector']
    labels = data['labels']

    ax.set_xlabel(labels.get('xlabel'))
    ax.set_ylabel(labels.get('ylabel'))
    ax.set_zlabel(labels.get('zlabel'))

    ax.autoscale(enable=True, axis='both', tight=True)
    surf = ax.plot_surface(y_vector, x_vector, z_vector, rstride=2, cstride=2, cmap=cm.coolwarm, linewidth=0)

    fig.colorbar(surf)
    fig.tight_layout()
    # fig.savefig('samplefigure', bbox_inches='tight')


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
    leftline = ax.axvline(x=slider1XPos, color='r', linewidth=1)
    rightline = ax.axvline(x=slider2XPos, color='r', linewidth=1)

    h = DraggableLine(leftline, rightline, interval)
    h.connect()
    fig.tight_layout()
    return h  # need to return handlers, otherwise they are garbage collected and user cant move sliders
