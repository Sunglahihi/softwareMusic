# -*- coding: utf-8 -*-
"""
Created on Wed May 26 21:59:41 2021

@author: Lee
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May 23 21:13:13 2021

@author: Lee
"""
import os

from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QPushButton, QSlider, QStyle, QVBoxLayout, QStatusBar)


class VideoPlayer(QDialog):
    def __init__(self,keyword):
        super().__init__()
        self.keyword = keyword
        self.initUI()
        
    def initUI(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVolume(10)  # 첫 음악 크기 세팅
        btnSize = QSize(16, 16)
        videoWidget = QVideoWidget()
        
        openButton = QPushButton("Open Video")
        openButton.setCheckable(True)
        openButton.setToolTip("Open Video File")
        openButton.setStatusTip("Open Video File")
        openButton.setFixedHeight(24)
        openButton.setIconSize(btnSize)
        openButton.setFont(QFont("Noto Sans", 8))
        openButton.setIcon(QIcon.fromTheme("document-open", QIcon("D:/_Qt/img/open.png")))
        # openButton 숨김
        openButton.hide()
        volumeDescBtn = QPushButton('V (-)')#Decrease Volume
        volumeIncBtn = QPushButton('V (+)')	#Increase Volume
        volumeDescBtn.clicked.connect(self.decreaseVolume)
        volumeIncBtn.clicked.connect(self.increaseVolume)
        
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedHeight(24)
        self.playButton.setIconSize(btnSize)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        
        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto Sans", 7))
        self.statusBar.setFixedHeight(14)
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(openButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(volumeDescBtn)
        controlLayout.addWidget(volumeIncBtn)
        
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.statusBar)
        self.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.statusBar.showMessage("Ready")
        
        # 실행하면 뮤비 자동재생
        fileName = os.path.abspath("./src/merge/" + self.keyword + ".mp4")
        print("1 fileName", fileName)
        
        if fileName != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.statusBar.showMessage(fileName)
            self.mediaPlayer.play()
            
        self.setWindowTitle('Movie')
        self.resize(600, 400)
        self.move(1200, 400)
        
    def abrir(self):
        # 파일 불러오기 -> keyword는 처리해야함
        fileName = os.path.abspath("./src/merge/" + self.keyword + ".mp4")

        
        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
            self.statusBar.showMessage(fileName)
            self.play()
    
    def increaseVolume(self):
        vol = self.mediaPlayer.volume()
        vol = max(vol+5,100)
        self.mediaPlayer.setVolume(vol)
        
    def decreaseVolume(self):
        vol = self.mediaPlayer.volume()
        vol = max(vol-5,0)
        self.mediaPlayer.setVolume(vol)
        
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
            
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
            
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
    def handleError(self):
        self.playButton.setEnabled(False)
        self.statusBar.showMessage("파일이 없습니다!" + self.mediaPlayer.errorString())
        
    def showModal(self):
        return super().exec_()
    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    player = VideoPlayer('헤픈 우연 - 헤이즈 (Heize)')
    player.setWindowTitle("Player")
    player.resize(600, 400)
    player.show()
    sys.exit(app.exec_())
 