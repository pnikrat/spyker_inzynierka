import matplotlib.pyplot as plt

def plot_function(fig, data):
    fig.clear()
    ax = fig.add_subplot(1, 1, 1)

    x_vector = data['x_vector']
    y_vector = data['y_vector']
    labels = data['labels']

    ax.set_xlabel(labels.get('xlabel'))
    ax.set_ylabel(labels.get('ylabel'))

    if 'cursors' in data:
        for x in data['cursors']:
            ly = ax.axvline(color='r')
            ly.set_xdata(x)

    if len(labels) == 2:
        ax.plot(x_vector, y_vector)
    elif len(labels) == 3:
        pax = ax.pcolormesh(y_vector)
        cbar = fig.colorbar(pax)
        cbar.ax.set_ylabel(labels.get('zlabel'))
        ax.autoscale(enable=True, axis='both', tight=True)


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