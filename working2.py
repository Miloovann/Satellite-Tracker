import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import *

class VideoPlayer(QVideoWidget):
    def __init__(self):
        super(VideoPlayer, self).__init__()
        videoWidget = QVideoWidget()
        
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        self.setLayout(layout)
        
        MediaPlayer = QMediaPlayer()
        MediaPlayer.setVideoOutput(videoWidget)
        MediaPlayer.setSource(QUrl.fromLocalFile("/Users/junyiho/Desktop/Centad/video.mp4"))
        MediaPlayer.play()
        
        self.mediaplayer = MediaPlayer
        self.resize(600, 400)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    sys.exit(app.exec())