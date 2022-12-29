import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
matplotlib.use('Qt5Agg')

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, azimuth, elevation, width=5, height=4, dpi=100):
        fig = plt.figure(figsize=(width, height), dpi=dpi)
        ax = fig.add_subplot(polar=True)
        ax.set_ylim(90, 0)
        ax.set_yticks(np.arange(90,0, -30))
        ax.plot(azimuth,elevation, lw=2)
        super(MplCanvas, self).__init__(fig)
