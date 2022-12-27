import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
import plotly.graph_objects as go
import plotly.offline as offline

with open("data2.txt", "r") as f:
    x = f.readlines()
    lat, lon = [], []
    for txt in x:
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        webview = QWebEngineView(self)
        webview.setGeometry(QRect(0, 0, 800, 600))
        webview.setUrl(QUrl.fromLocalFile('/Users/junyiho/Desktop/Centad/myplot.html'))
        self.setCentralWidget(webview)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())