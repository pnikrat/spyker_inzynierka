class DraggableLine(object):
    def __init__(self, line, otherline, interval):
        self.line = line
        self.otherline = otherline
        self.press = None
        self.last_x_pos = self.line.get_xdata()
        self.last_x_pos_other = self.otherline.get_xdata()
        self.interval = interval
        self.limits = self.line.figure.axes[0].get_xlim()

    def get_last_x_pos(self):
        return self.last_x_pos, self.last_x_pos_other

    def set_other_x_pos(self, xpos):
        current = self.line.get_xdata()
        self.otherline.set_xdata(current + self.interval)
        self.otherline.figure.canvas.draw()

    def connect(self):
        self.idpress = self.line.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.idrelease = self.line.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.idmotion = self.line.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        #see if mouse is over the line
        # if event.inaxes != self.line.axes:
        #     return
        # contains, attrd = self.line.contains(event)
        # if not contains:
        #     return
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
        if self.limits[0] < x0[0] + dx < self.limits[1] - self.interval:
            self.line.set_xdata(x0 + dx)
            self.set_other_x_pos(dx)
            self.line.figure.canvas.draw()

    def on_release(self, event):
        #reset the press data
        self.press = None
        self.line.figure.canvas.draw()
        self.last_x_pos = self.line.get_xdata()
        self.last_x_pos_other = self.otherline.get_xdata()

    def disconnect(self):
        self.line.figure.canvas.mpl_disconnect(self.idpress)
        self.line.figure.canvas.mpl_disconnect(self.idrelease)
        self.line.figure.canvas.mpl_disconnect(self.idmotion)