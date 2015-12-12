from spyker.model.draggableplots import DraggableLine


def plot_function(fig, data):

    fig.clear()
    ax = fig.add_subplot(1, 1, 1)

    y_vector = data['y_vector']
    x_vector = data['x_vector']
    labels = data['labels']

    ax.set_xlabel(labels.get('xlabel'))
    ax.set_ylabel(labels.get('ylabel'))

    if 'cursors' in data:
        cursors = data['cursors']
        for x in cursors:
            ly = ax.axvline(color='r')
            ly.set_xdata(x)

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