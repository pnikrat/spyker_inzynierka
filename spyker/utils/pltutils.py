from matplotlib import cm
from spyker.model.draggableplots import DraggableLine


def plot_function(fig, data):
    fig.clear()

    x_vector = data['x_vector']
    y_vector = data['y_vector']
    if 'z_vector' in data:
        ax = fig.gca(projection='3d')
        z_vector = data['z_vector']
    else:
        ax = fig.add_subplot(1, 1, 1)

    labels = data['labels']

    ax.set_xlabel(labels.get('xlabel'))
    ax.set_ylabel(labels.get('ylabel'))

    if 'cursors' in data:
        for x in data['cursors']:
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
                handlers = []
                for line in lines:
                    h = DraggableLine(line)
                    h.connect()
                    handlers.append(h)
                return handlers  # need to return handlers, otherwise they are garbage collected and user cant move sliders

        elif len(labels) == 3:
            pax = ax.pcolormesh(y_vector)
            cbar = fig.colorbar(pax)
            cbar.ax.set_ylabel(labels.get('zlabel'))
            ax.autoscale(enable=True, axis='both', tight=True)
    else:
        surf = ax.plot_surface(y_vector, x_vector, z_vector, rstride=5, cstride=5, cmap=cm.coolwarm, linewidth=0)
        fig.colorbar(surf)


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
