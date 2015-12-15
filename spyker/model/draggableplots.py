class DraggableLine(object):
    def __init__(self, line):
        self.line = line
        self.press = None
        self.last_x_pos = self.line.get_xdata()

    def get_last_x_pos(self):
        return self.last_x_pos

    def connect(self):
        self.idpress = self.line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.idrelease = self.line.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.idmotion = self.line.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        #see if mouse is over the line
        if event.inaxes != self.line.axes:
            return
        contains, attrd = self.line.contains(event)
        if not contains:
            return
        x0 = self.line.get_xdata()
        #only need to move along the x axis!
        self.press = x0, event.xdata

    def on_motion(self, event):
        #move the line if the mouse is still over line
        if self.press is None:
            return
        if event.inaxes != self.line.axes:
            return
        x0, xpress = self.press
        dx = event.xdata - xpress
        self.line.set_xdata(x0 + dx)
        self.line.figure.canvas.draw()

    def on_release(self, event):
        #reset the press data
        self.press = None
        self.line.figure.canvas.draw()
        self.last_x_pos = self.line.get_xdata()

    def disconnect(self):
        self.line.figure.canvas.mpl_disconnect(self.idpress)
        self.line.figure.canvas.mpl_disconnect(self.idrelease)
        self.line.figure.canvas.mpl_disconnect(self.idmotion)