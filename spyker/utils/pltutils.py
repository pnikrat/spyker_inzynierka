from spyker.model.draggableplots import DraggableLine
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def plot_function(fig, data):
    fig.clear()
    y_vector = data['y_vector']
    x_vector = data['x_vector']
    if 'z_vector' in data:
        ax = fig.gca(projection='3d')
        z_vector = data['z_vector']
    else:
        ax = fig.add_subplot(1, 1, 1)

    labels = data['labels']

    ax.set_xlabel(labels.get('xlabel'))
    ax.set_ylabel(labels.get('ylabel'))

    if 'cursors' in data:
        cursors = data['cursors']
        for x in cursors:
            ly = ax.axvline(color='r')
            ly.set_xdata(x)
    if 'z_vector' not in data:
        if len(labels) == 2:
            ax.plot(x_vector, y_vector)
            if 'sliders' in data:
                slider1XPos, slider2XPos = data['sliders']
                leftline = ax.axvline(x=slider1XPos, color='r', linewidth=4)
                rightline = ax.axvline(x=slider2XPos, color='r', linewidth=4)
                lines = [leftline, rightline]
                handles = []
                for line in lines:
                    h = DraggableLine(line)
                    h.connect()
                    handles.append(h)
                return handles  # need to return handlers, otherwise they are garbage collected and user cant move sliders

        elif len(labels) == 3:
            pax = ax.pcolormesh(y_vector)
            cbar = fig.colorbar(pax)
            cbar.ax.set_ylabel(labels.get('zlabel'))
            ax.autoscale(enable=True, axis='both', tight=True)
    else:
        surf = ax.plot_surface(y_vector, x_vector, z_vector, rstride=5, cstride=5, cmap=cm.coolwarm,  linewidth=0)
        fig.colorbar(surf)