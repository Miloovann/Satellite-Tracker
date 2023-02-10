from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

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
