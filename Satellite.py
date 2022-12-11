# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Satellite Tracking GUI developed using PyQt6"""

import sys
import numpy as np

from sgp4 import api
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import *
from datetime import datetime, timedelta

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        
        r = np.arange(0, 2, 0.01)
        theta = 2 * np.pi * r

        theta = np.linspace(0, 2*np.pi, 2001)
        curve1 = 5*np.cos(theta)


        self.axes = fig.add_subplot(polar=True)
        self.axes.plot(theta, curve1, color='xkcd:salmon', label='rose curve1')
        super(MplCanvas, self).__init__(fig)


WINDOW_SIZE = 900

class Satellite(QMainWindow):
    def __init__(self, parent=None):
        super(Satellite, self).__init__()
        self.create_UI()
    
    def create_UI(self):
        self.setWindowTitle("Satellite Tracker")
        self.setMinimumSize(WINDOW_SIZE, WINDOW_SIZE)
        
        mainlayout = QVBoxLayout()
        timedis = self.displayTime()
        posdis = self.displayPosition()
        mainlayout.addLayout(timedis)
        mainlayout.addLayout(posdis)
        
        sidelayout = QHBoxLayout()
        pplot = self.polarPlot()
        cctv = self.CCTV_Feed()
        sidelayout.addLayout(pplot)
        sidelayout.addLayout(cctv)
        
        mainlayout.addLayout(sidelayout)
        
        widget = QWidget()
        widget.setLayout(mainlayout)
        self.setMenuWidget(widget)
        
        self.show()
    
    def setLine(self, dir, width=2):
        obj = QFrame()
        if dir == "V":      obj.setFrameShape(QFrame.Shape.VLine)
        elif dir == "H":    obj.setFrameShape(QFrame.Shape.HLine)
        else:               obj.setFrameShape(QFrame.Shape.Box)
        obj.setStyleSheet("background-color: gold; border:none")
        obj.setLineWidth(width)
        return obj
        
    def setText(self, obj):
        obj = QLabel(obj)
        obj.setFont(QFont("Times New Roman", 30))
        obj.setStyleSheet("color:aquamarine; border: none;")
        obj.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return obj
    
    def displayTime(self): 
        timing = str(datetime.now().strftime("%H:%M"))
        initial = str((datetime.now() - timedelta(hours=3)).strftime("%H:%M"))
        final = str((datetime.now() + timedelta(hours=3)).strftime("%H:%M"))
        
        layout = QGridLayout()

        headers = ["Local Time", timing, "Contact Time", "Initial", initial, "Final", final]
        localheader, localtime, contacttime, initialheader, initialtime, finalheader, finaltime = [self.setText(i) for i in headers]

        H = [self.setLine("H") for i in range(3)]
        linetop, linemid, linebtm = H[0], H[1], H[2]
        
        V = [self.setLine("V") for i in range(4)]
        lineleft, lineright, line1, line2 = V[0], V[1], V[2], V[3]
        line2.setStyleSheet("color:transparent")

        maxrow, maxcol = 6, 6

        layout.addWidget(lineleft,  0,      0,      maxrow+1, 1) 
        layout.addWidget(lineright, 0,      maxcol, maxrow+1, 1)
        layout.addWidget(linetop,   0,      0,      1,        maxcol+1)    
        layout.addWidget(linebtm,   maxrow, 0,      1,        maxcol+1)
        
        
        layout.addWidget(localheader, 1, 1, 3, 1)   
        layout.addWidget(localtime, 4, 1)           
        layout.addWidget(line1, 0, 2, maxrow+1, 1)


        layout.addWidget(contacttime, 1, 3, 1, 3)   
        layout.addWidget(linemid, 2, 2, 1, maxcol-1)
        layout.addWidget(initialheader, 3, 3)       
        layout.addWidget(initialtime, 4, 3)    
             
        layout.addWidget(line2, 2, 4, maxrow-1, 1)  
               
        layout.addWidget(finalheader, 3, 5)         
        layout.addWidget(finaltime, 4, 5)

        return layout

    def displayPosition(self):
        layout = QGridLayout()
        
        headers = ["Satellite", "Name", "Location", "Azimuth", "Elevation"]
        title, SatName, SatLoc, SatAzi, SatEle = [self.setText(i) for i in headers]
        
        details = ["Orion", "Jurong", "99.2", "76.1"]
        Name1, Loc1, Azi1, Ele1 = [self.setText(i) for i in details]
        
        H = [self.setLine("H") for i in range(3)]
        linetop, linemid1, linebtm = H[0], H[1], H[2]
        
        V = [self.setLine("V") for i in range(5)]
        lineleft, lineright, line1, line2, line3 = V[0], V[1], V[2], V[3], V[4]
        line1.setStyleSheet("color:transparent")
        line2.setStyleSheet("color:transparent")
        line3.setStyleSheet("color:transparent")

        maxrow, maxcol = 5, 8

        layout.addWidget(lineleft,  0,      0,      maxrow+1, 1) 
        layout.addWidget(lineright, 0,      maxcol, maxrow+1, 1)
        layout.addWidget(linetop,   0,      0,      1,        maxcol+1)    
        layout.addWidget(linebtm,   maxrow, 0,      1,        maxcol+1)
        layout.addWidget(linemid1, 2, 0, 1, maxcol+1)
        [layout.addWidget(name, 2, pos*2, maxrow-1, 1) for pos, name in enumerate([line1, line2, line3], start=1)]
        
        
        layout.addWidget(title, 1, 1, 1, maxcol)
        [layout.addWidget(name, 3, pos*2 + 1) for pos, name in enumerate([SatName, SatLoc, SatAzi, SatEle])]
        [layout.addWidget(name, 4, pos*2 + 1) for pos, name in enumerate([Name1, Loc1, Azi1, Ele1])]
        
        return layout
    
    def polarPlot(self):
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        
        toolbar = NavigationToolbar(sc, self)

        layout = QGridLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        return layout

    def CCTV_Feed(self):
        H = [self.setLine("H") for i in range(2)]
        linetop, linebtm = H[0], H[1]
        
        V = [self.setLine("V") for i in range(2)]
        lineleft, lineright = V[0], V[1]
        
        layout = QGridLayout()

        maxrow, maxcol = 30,30

        layout.addWidget(lineleft,  0,      0,      maxrow+1, 1) 
        layout.addWidget(lineright, 0,      maxcol, maxrow+1, 1)
        layout.addWidget(linetop,   0,      0,      1,        maxcol+1)    
        layout.addWidget(linebtm,   maxrow, 0,      1,        maxcol+1)
        
        return layout
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Sate = Satellite()
    sys.exit(app.exec())