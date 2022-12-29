# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Satellite Tracking GUI developed using PyQt5"""

import sys, re
from CCTV_Player import VideoPlayer
from PolarPlot import MplCanvas
from PyQt5.QtWidgets import (QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, 
                             QWidget, QFrame, QGridLayout, QLabel, QDesktopWidget)
from PyQt5.QtCore import (Qt, QUrl, QRect)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.offline as offline

class Clock(QLabel):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Times New Roman", 30))
        self.setStyleSheet("color:aquamarine; border: none;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # update every second

    def update_time(self):
        current_time = datetime.now().strftime('%H:%M')
        self.setText(current_time)

class Satellite(QMainWindow):
    def __init__(self, parent=None):
        super(Satellite, self).__init__()
        self.create_UI()
    
    def create_UI(self):
        self.setWindowTitle("Satellite Tracker")
        desktop = QDesktopWidget()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        self.setMinimumSize(screen_width, screen_height)
        
        
        timedis = self.displayTime()
        posdis = self.displayPosition()
        video_player = VideoPlayer()
        firstrow = QHBoxLayout()
        firstrow.addLayout(timedis)
        firstrow.addLayout(posdis)
        firstrow.addWidget(video_player)
        
        
        pplot = self.polarPlot()
        map = self.displayMap()
        secondrow = QHBoxLayout()
        secondrow.addLayout(pplot)
        secondrow.addLayout(map)
        
        # firstrow.setStretch(1,1)
        # secondrow.setStretch(1, 1)
        
        mainlayout = QVBoxLayout()
        mainlayout.addLayout(firstrow)
        mainlayout.addLayout(secondrow)
        
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
        aos_P = r"default: AOS: .* (\d+):(\d+):\d+ .*"
        los_P = r"default: LOS: .* (\d+):(\d+):\d+ .*"

        with open("main.txt", "r") as f:
            x = f.readlines()
            for txt in x:
                if "default: AOS:" in txt:
                    match = re.search(aos_P, txt)
                    hour, minute = match.groups()
                    initial = f"{hour}:{minute}"
                    
                elif "default: LOS:" in txt:
                    match = re.search(los_P, txt)
                    hour, minute = match.groups()
                    final = f"{hour}:{minute}"
                    break
                
        
        localtime = Clock()
        
        layout = QGridLayout()

        headers = ["Local", "Contact", "Initial", initial, "Final", final]
        localheader, contacttime, initialheader, initialtime, finalheader, finaltime = [self.setText(i) for i in headers]

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
        
        headers = ["Satellite", "Name", "Azimuth", "Elevation"]
        title, SatName, SatAzi, SatEle = [self.setText(i) for i in headers]
        
        details = ["VELOX 2", "99.2", "76.1"]
        Name1, Azi1, Ele1 = [self.setText(i) for i in details]
        
        H = [self.setLine("H") for i in range(3)]
        linetop, linemid1, linebtm = H[0], H[1], H[2]
        
        V = [self.setLine("V") for i in range(5)]
        lineleft, lineright, line1, line2 = V[0], V[1], V[2], V[3]
        line1.setStyleSheet("color:transparent")
        line2.setStyleSheet("color:transparent")

        maxrow, maxcol = 6, 8

        layout.addWidget(lineleft,  0,      0,      maxrow+1, 1) 
        layout.addWidget(lineright, 0,      maxcol, maxrow+1, 1)
        layout.addWidget(linetop,   0,      0,      1,        maxcol+1)    
        layout.addWidget(linebtm,   maxrow, 0,      1,        maxcol+1)
        layout.addWidget(linemid1, 2, 0, 1, maxcol+1)
        [layout.addWidget(name, 2, pos*2, maxrow-1, 1) for pos, name in enumerate([line1, line2], start=1)] ##invisible lines to format consistent gap
        
        
        layout.addWidget(title, 1, 1, 1, maxcol)
        [layout.addWidget(name, 3, pos*2 + 1) for pos, name in enumerate([SatName, SatAzi, SatEle])]
        [layout.addWidget(name, 4, pos*2 + 1) for pos, name in enumerate([Name1, Azi1, Ele1])]
        
        return layout
    
    def polarPlot(self):
        with open("main.txt", "r") as f:
            x = f.readlines()
            az, el = [], []
            for txt in x:
                if "default: AZ: " in txt:
                    clean = txt[txt.find("AZ: ") + 4 : txt.find(", RX: ")]
                    az.append(float(clean[ : clean.find(",")]))
                    el.append(float(clean[clean.find(",")+6 : ]))
                
        azimuth = np.array(az)*np.pi/180
        elevation = np.array(el)
        
        sc = MplCanvas(azimuth, elevation, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(sc, self)

        layout = QGridLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        return layout

    def displayMap(self):
        H = [self.setLine("H") for i in range(2)]
        linetop, linebtm = H[0], H[1]
        
        V = [self.setLine("V") for i in range(2)]
        lineleft, lineright = V[0], V[1]
        
        layout = QGridLayout()

        maxrow, maxcol = 2,2

        layout.addWidget(lineleft,  0,      0,      maxrow+1, 1) 
        layout.addWidget(lineright, 0,      maxcol, maxrow+1, 1)
        layout.addWidget(linetop,   0,      0,      1,        maxcol+1)    
        layout.addWidget(linebtm,   maxrow, 0,      1,        maxcol+1)
         
        with open("main.txt", "r") as f:
            x = f.readlines()
            lat, lon = [], []
            for txt in x:
                if "default: Sat Latitude:" in txt:
                    clean = txt[txt.find("Latitude: ")+10 : txt.find(", Altitude")]
                    lat.append(float(clean[ : clean.find(",")]))
                    lon.append(float(clean[clean.find(",")+13 : ]))
                
        fig = go.Figure()

        # Add the curve to the figure
        fig.add_trace(go.Scattermapbox(
            lat=lat,
            lon=lon,
            mode='lines',
            line=dict(color='red', width=2)
        ))

        # Set the map style and zoom level
        fig.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            mapbox=dict(
                style='open-street-map',
                center=go.layout.mapbox.Center(lat=1.28967, lon=103.85007),
                zoom=3
            )
        )

        offline.plot(fig, filename='myplot.html', auto_open=False)
        
        webview = QWebEngineView(self)
        webview.setGeometry(QRect(0, 0, 800, 600))
        webview.setUrl(QUrl.fromLocalFile('/Users/junyiho/Desktop/Centad/myplot.html')) ##set path
        layout.addWidget(webview, 1, 1)
        
        return layout
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Sate = Satellite()
    sys.exit(app.exec())