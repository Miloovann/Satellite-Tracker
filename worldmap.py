import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
import plotly.graph_objects as go
import plotly.offline as offline

fig = go.Figure(go.Scattermapbox(
    mode = "markers+lines",
    lon = [10, 20, 30],
    lat = [10, 20,30],
    marker = {'size': 10}))

fig.add_trace(go.Scattermapbox(
    mode = "markers+lines",
    lon = [-50, -60,40],
    lat = [30, 10, -20],
    marker = {'size': 10}))

fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    mapbox = {
        'center': {'lon': 10, 'lat': 10},
        'style': "stamen-terrain",
        'center': {'lon': -20, 'lat': -20},
        'zoom': 1})

offline.plot(fig, filename='myplot.html', auto_open=False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a QWebEngineView widget and set the URL to the localhost website
        webview = QWebEngineView(self)
        webview.setGeometry(QRect(0, 0, 800, 600))
        webview.setUrl(QUrl.fromLocalFile('/Users/junyiho/Desktop/Centad/myplot.html'))

        # Add the QWebEngineView widget to the main window
        self.setCentralWidget(webview)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())