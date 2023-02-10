# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Satellite Tracking GUI developed using PyQt5"""

Current_Directory = "/home/kelvin/Desktop/hci_project"


import sys, re, importlib, time
import algosgp4, extractdata ##python file in same directory
#from VLCrtsp import RTSPWidget ##python file in same directory VLCrtsp
from PolarPlot import MplCanvas ##python file in same directory 
from PyQt5.QtWidgets import (QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, 
                             QWidget, QFrame, QGridLayout, QLabel, QDesktopWidget)
from PyQt5.QtCore import (Qt, QUrl, QRect)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.offline as offline

class RTSPWidget(QWidget):
    def _init_(self, rtsp_url, parent=None):
        super()._init_(parent)

        # Create a QMediaPlayer object and set the video output to a QVideoWidget
        self.player = QMediaPlayer(self)
        self.video_widget = QVideoWidget(self)
        self.player.setVideoOutput(self.video_widget)

        # Set the RTSP url as the media source
        self.player.setMedia(QMediaContent(QUrl(rtsp_url)))

        # Create play/pause buttons
        self.play_button = QPushButton("Play", self)
        self.pause_button = QPushButton("Pause", self)
        self.play_button.clicked.connect(self.player.play)
        self.pause_button.clicked.connect(self.player.pause)

        # Create a layout and add the video widget and buttons
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_widget)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        layout.addLayout(button_layout)

class Satellite(QMainWindow):
    def __init__(self, parent=None):
        super(Satellite, self).__init__()
        self.initial, self.final = algosgp4.aosdt.strftime("%H:%M"), algosgp4.losdt.strftime("%H:%M") ##importlib accounted
        self.lat, self.lon = extractdata.lat, extractdata.lon
        self.az, self.el = extractdata.az, extractdata.el
        self.AZList, self.ELList = list(map(str, np.around(self.az, decimals = 2))), list(map(str, np.around(self.el, decimals = 2)))
        self.create_UI()
    
    def create_UI(self):
        self.setWindowTitle("Satellite Tracker")
        desktop = QDesktopWidget()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        self.setMinimumSize(screen_width-100, screen_height-100)
        

        pplot = self.polarPlot()
        plotmap = self.displayMap()
        secondrow = QHBoxLayout()
        secondrow.addLayout(pplot)
        secondrow.addLayout(plotmap)
      
        timedis = self.displayTime()
        posdis = self.displayPosition()
        #video_player = VideoPlayer()
        firstrow = QHBoxLayout()
        firstrow.addLayout(timedis)
        firstrow.addLayout(posdis)
        #firstrow.addWidget(video_player)

        # Create an RTSPWidget with a specific RTSP URL
        self.rtsp_widget = RTSPWidget("rtsp://star_admin2:fyPe40801_2022@172.20.46.13:554/Streaming/Channels/101/")

        # Create a layout and add the RTSP widget to it
        layout = QVBoxLayout(self)
        firstrow.addWidget(self.rtsp_widget)

        firstrow.setStretch(1,1)
        secondrow.setStretch(1, 1)   

        
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
        obj.setStyleSheet("color:black; border: none;")
        obj.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return obj

    def updateTimes(self):
        self.localtime.setText(datetime.now().strftime('%H:%M'))
        importlib.reload(algosgp4)
        self.initial = algosgp4.aosdt.strftime("%H:%M")
        self.final = algosgp4.losdt.strftime("%H:%M")
        self.initialtime = self.setText(self.initial)
        self.finaltime = self.setText(self.final)
    
    def displayTime(self):
        self.localtime = self.setText(datetime.now().strftime('%H:%M'))
        self.initialtime = self.setText(self.initial)
        self.finaltime = self.setText(self.final)

        timer = QTimer(self)
        timer.timeout.connect(self.updateTimes)
        timer.start(30000)

        layout = QGridLayout()
        
        headers = ["Local", "Contact", "Initial","Final"]
        localheader, contacttime, initialheader, finalheader= [self.setText(i) for i in headers]

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
        layout.addWidget(self.localtime, 4, 1)           
        layout.addWidget(line1, 0, 2, maxrow+1, 1)

        layout.addWidget(contacttime, 1, 3, 1, 3)   
        layout.addWidget(linemid, 2, 2, 1, maxcol-1)
        layout.addWidget(initialheader, 3, 3)       
        layout.addWidget(self.initialtime, 4, 3)    
             
        layout.addWidget(line2, 2, 4, maxrow-1, 1)  
               
        layout.addWidget(finalheader, 3, 5)         
        layout.addWidget(self.finaltime, 4, 5)

        return layout

    def updatePositions(self):
        importlib.reload(extractdata)
        self.lat, self.lon = extractdata.lat, extractdata.lon
        self.az, self.el = extractdata.az, extractdata.el
        self.AZList, self.ELList = list(map(str, np.around(self.az, decimals = 2))), list(map(str, np.around(self.el, decimals = 2)))

        self.Azi1.setText(self.AZList[0])
        self.AZList.pop(0)
        self.Ele1.setText(self.ELList[0])
        self.ELList.pop(0)
        
        
    def displayPosition(self):
        layout = QGridLayout()
        
        headers = ["Satellite", "Name", "Lat", "Lon", "VELOX 2"]
        title, SatName, SatAzi, SatEle, Name1 = [self.setText(i) for i in headers]

        self.Azi1 = self.setText(self.AZList[0])
        self.AZList.pop(0)
        self.Ele1 = self.setText(self.ELList[0])
        self.ELList.pop(0)
        timer = QTimer(self)
        timer.timeout.connect(self.updatePositions)
        timer.start(600000)
        
        H = [self.setLine("H") for i in range(3)]
        linetop, linemid1, linebtm = H[0], H[1], H[2]
        
        V = [self.setLine("V") for i in range(5)]
        lineleft, lineright, line1, line2 = V[0], V[1], V[2], V[3]
        line1.setStyleSheet("color:transparent")
        line2.setStyleSheet("color:transparent")

        maxrow, maxcol = 6, 6

        layout.addWidget(lineleft,  0,      0,      maxrow+1, 1) 
        layout.addWidget(lineright, 0,      maxcol, maxrow+1, 1)
        layout.addWidget(linetop,   0,      0,      1,        maxcol+1)    
        layout.addWidget(linebtm,   maxrow, 0,      1,        maxcol+1)
        layout.addWidget(linemid1, 2, 0, 1, maxcol+1)
        [layout.addWidget(name, 2, pos*2, maxrow-1, 1) for pos, name in enumerate([line1, line2], start=1)] ##invisible lines to format consistent gap
        
        
        layout.addWidget(title, 1, 1, 1, maxcol)
        [layout.addWidget(name, 3, pos*2 + 1) for pos, name in enumerate([SatName, SatAzi, SatEle])]
        [layout.addWidget(name, 4, pos*2 + 1) for pos, name in enumerate([Name1, self.Azi1, self.Ele1])]
        
        return layout
    
    def polarPlot(self):
        azimuth = np.array(self.az)*np.pi/180
        elevation = np.array(self.el)
        
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
                
        fig = go.Figure()

        # Add the curve to the figure
        fig.add_trace(go.Scattermapbox(
            lat=self.lat,
            lon=self.lon,
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
        webview.setUrl(QUrl.fromLocalFile(Current_Directory + '/myplot.html')) ##set path
        layout.addWidget(webview, 1, 1)
        
        return layout
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    Sate = Satellite()
    sys.exit(app.exec())
