# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import webdriver_manager.chrome
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QCoreApplication, QThread, QObject, pyqtSignal
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import *
from datetime import datetime as dt
import qtmodern.styles

import Crawler
# noinspection PyUnresolvedReferences
import movieCrawler
# noinspection PyUnresolvedReferences
import movieCrawler
# noinspection PyUnresolvedReferences
import music_player
# noinspection PyUnresolvedReferences

import os


# noinspection PyUnresolvedReferences


# 파일정보 없을 때 크롤링 -> 크롤링 프로그램과 별개로 ui 프로그램이 동결상태가 되지 않도록 하기 위해 스레드 처리
class Thread(QThread):
    def __init__(self, parent, keyword):
        super(Thread, self).__init__(parent)
        self.parent = parent
        self.keyword = keyword

    # run() -> thread.start()로 시작
    def run(self):
        crawl = Crawler.Crawler()
        crawl.start(self.keyword)


class Thread2(QThread):
    # keyword = QtCore.pyqtSignal(str)
    def __init__(self, parent, keyword):
        super().__init__(parent)
        self.parent = parent
        self.keyword = keyword

    def run(self):
        crawl = movieCrawler.movieCrawler(self.keyword)
        crawl.youtubeDown()


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        QWidget.__init__(self)

    # 스택위젯(0) 정보
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("MusicPlayer")
        MainWindow.resize(470,550)
        MainWindow.setWindowIcon(QIcon("./image/icon.png"))


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        # 스택위젯 생성해줌
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(9, 5, 470, 550))
        self.stackedWidget.setObjectName("stackedWidget")

        _translate = QtCore.QCoreApplication.translate
        # 첫 번째 페이지(Qwidget)
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setAttribute(True)

        self.label = QtWidgets.QLabel(self.page_1)
        self.label.setGeometry(QtCore.QRect(80, 80, 300, 45))
        self.label.setObjectName("label")
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Select Music Site</span></p></body></html>"))
        self.label.setStyleSheet("border-style:solid; border-width:2px; border-color: rgb(255,255,255); font: 20pt \"휴먼엑스포\"")


        self.pushButton_1 = QtWidgets.QPushButton(self.page_1)
        self.pushButton_1.setGeometry(QtCore.QRect(175, 170, 110, 40))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_1.setText(_translate("MainWindow", "Melon"))
        self.pushButton_1.setStyleSheet("font: 11pt \"휴먼엑스포\"")

        self.pushButton_2 = QtWidgets.QPushButton(self.page_1)
        self.pushButton_2.setGeometry(QtCore.QRect(175, 240, 110, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText(_translate("MainWindow", "Genie"))
        self.pushButton_2.setStyleSheet("font: 11pt \"휴먼엑스포\"")

        self.pushButton_3 = QtWidgets.QPushButton(self.page_1)
        self.pushButton_3.setGeometry(QtCore.QRect(175, 310, 110, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText(_translate("MainWindow", "Bugs"))
        self.pushButton_3.setStyleSheet("font: 11pt \"휴먼엑스포\"")

        self.pushButton_4 = QtWidgets.QPushButton(self.page_1)
        self.pushButton_4.setGeometry(QtCore.QRect(175, 380, 110, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setText(_translate("MainWindow", "Vibe"))
        self.pushButton_4.setStyleSheet("font: 11pt\"휴먼엑스포\"")

        self.pushButton_5 = QtWidgets.QPushButton(self.page_1)
        self.pushButton_5.setGeometry(QtCore.QRect(175, 450, 110, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setText(_translate("MainWindow", "Flo"))
        self.pushButton_5.setStyleSheet("font: 11pt\"휴먼엑스포\"")
        # Page(Qwidget) 구성품들

        # 여기까지 page_1 구성하고 배치함

        # 스택위젯에 해당 page_1 위젯을 추가해줌
        self.stackedWidget.addWidget(self.page_1)

        # MainWindow centralWidget 영역
        MainWindow.setCentralWidget(self.centralwidget)
        # 이벤트 connect
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 메인으로부터 제일 먼저 실행되므로 스택위젯 index(0)으로 접근
        self.stackedWidget.setCurrentIndex(0)

        # 5.28 클릭버튼 True or False 활성화
        self.pushButton_1.setCheckable(True)
        self.pushButton_2.setCheckable(True)
        self.pushButton_3.setCheckable(True)
        self.pushButton_4.setCheckable(True)
        self.pushButton_5.setCheckable(True)

        self.pushButton_1.clicked.connect(lambda: self.startCrawling(self.pushButton_1.text()))
        self.pushButton_2.clicked.connect(lambda: self.startCrawling(self.pushButton_2.text()))
        self.pushButton_3.clicked.connect(lambda: self.startCrawling(self.pushButton_3.text()))
        self.pushButton_4.clicked.connect(lambda: self.startCrawling(self.pushButton_4.text()))
        self.pushButton_5.clicked.connect(lambda: self.startCrawling(self.pushButton_5.text()))



    # 사이트 선택 -> 파일 유무에 따른 크롤링 or 재생목록 띄우기
    def startCrawling(self, keyword):
        now = dt.now()
        day = now.strftime('%Y%m%d')
        path = "./songList/" + keyword + "_" + day + ".csv"

        if os.path.isfile(path):
            self.stackPage_3(keyword)
        else:
            self.x = Thread(self, keyword)
            self.x.start()
            self.stackPage_2(keyword)  # 파일 없으면 크롤링돌아가면서 노래정보 띄워줄 스택위젯으로 넘어감



    # 스택위젯(1) 정보 -> 파일 x, 크롤링할 때 띄워줄 화면
    def stackPage_2(self, keyword):
        _translate = QtCore.QCoreApplication.translate

        # 마찬가지로 page_2(QWidget) 생성해주고
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        #self.page_2.setAttribute(True)


        self.page2_label1 = QtWidgets.QLabel(self.page_2)
        self.page2_label1.setGeometry(QtCore.QRect(78, 215, 300, 40))
        self.page2_label1.setObjectName("page2_label1")
        self.page2_label1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">노래파일이 없어 가져오는 중입니다</span></p></body></html>"))
        self.page2_label1.setStyleSheet("border-style:solid; border-width:2px; border-color: rgb(255,255,255); font: 20pt \"휴먼엑스포\"")


        self.page2_label2 = QtWidgets.QLabel(self.page_2)
        self.page2_label2.setGeometry(QtCore.QRect(150, 267, 165, 41))
        self.page2_label2.setObjectName("page2_label2")
        self.page2_label2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">약 3분 소요됩니다</span></p></body></html>"))
        self.page2_label2.setStyleSheet("border-style:solid; border-width:2px; border-color: rgb(255,255,255); font: 20pt \"휴먼엑스포\"")


        self.page_2_init_button = QtWidgets.QPushButton(self.page_2)
        self.page_2_init_button.setGeometry(QtCore.QRect(392, 0, 55, 35))
        self.page_2_init_button.setObjectName("page_2_init_button")
        self.page_2_init_button.setText("Reset")
        self.page_2_init_button.setStyleSheet("font: 8pt \"휴먼엑스포\"")
        self.page_2_init_button.clicked.connect(self.init_rayout)

        self.stackedWidget.addWidget(self.page_2)
        self.stackedWidget.setCurrentWidget(self.page_2)

        time = QTimer(self)
        time.singleShot(180000, lambda: self.stackPage_3(keyword))



    # 스택위젯(2) 정보
    '''
    스택위젯 - page_3(QWidget) - tabWidget(QTabWidget) - tab_1(QWidget) 및 tab_2(QWidget) 이렇게 내려감

    1. page_3(QWidget) 먼저 생성
    2. page_3(QWidget)안에 tabWidget(QTabWidget)생성
    3. tabWidget(QTabWidget)안에 tab_1(QWidget), tab_2(QWidget) 생성, 각각 TOP100, 장르별
    4. tab_1(QWidget)에 TOP100 구성품, tab_2(QWidget)에 장르별 구성품 생성
    5. tabWidget(QTabWidget).addTab(tab_1, tab_2)해서 넣어줌
    6. 스택위젯.addWidget(page_3)으로 page_3(QWidget)을 넣어줌
      * 탭위젯은 처음에 생성할때 page_3(QWidget)으로 해줬으므로 page_3의 구성품인 상태이므로 스택위젯에 탭위젯 넣을 필요없이 page_3을 넣어줌

    나머지는 그대로이고 QWidget 구성만 바뀐거 내용은 달라진거 없음
    '''
    def stackPage_3(self, keyword):
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.page_3.setAttribute(True)

        # 탭위젯 생성(self.page_3)
        self.tabWidget = QtWidgets.QTabWidget(self.page_3)  # 탭위젯은 page_2안의 구성품
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 450, 530))
        self.tabWidget.setObjectName("tabWidget")

        # 탭1 위젯으로 생성(Top 100)
        self.tab_1 = QtWidgets.QWidget()  # TOP100 탭(창 하나의 위젯)
        self.tab_1.setObjectName("tab_1")


        # 탭1 정보>>
        # textBrowser -> 노래정보 띄워줄 거
        self.textBrowser_1 = QtWidgets.QTextBrowser(self.tab_1)
        self.textBrowser_1.setGeometry(QtCore.QRect(60, 75, 330, 110))
        self.textBrowser_1.setObjectName("textBrowser")
        _translate = QtCore.QCoreApplication.translate
        self.textBrowser_1.setHtml(_translate("MainWindow",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                              "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textBrowser_1.setStyleSheet("font: 10pt \"HY목각파임B\"")

        # label -> 제목 띄울 거 (TOP 100 재생목록)
        self.label_1 = QtWidgets.QLabel(self.tab_1)
        self.label_1.setGeometry(QtCore.QRect(60, 45, 330, 30))
        self.label_1.setObjectName("label_1")
        self.label_1.setAlignment(Qt.AlignCenter)
        self.label_1.setText(keyword + " MusicPlayer")
        #self.label_1.setText(_translate("MainWindow","<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">MusicPlayer</span></p></body></html>"))
        self.label_1.setStyleSheet("border-style:solid; border-width:0.5px; border-color: rgb(255,255,255); font: 12pt \"휴먼옛체\"")
        

        # mv_save -> 버튼으로 뮤비(음원) 추출
        self.mvSave_button_1 = QtWidgets.QPushButton(self.tab_1)
        self.mvSave_button_1.setGeometry(QtCore.QRect(60, 154, 110, 31))
        self.mvSave_button_1.setObjectName("mvSave_button_1")
        self.mvSave_button_1.setText(_translate("MainWindow", "Download"))
        self.mvSave_button_1.setStyleSheet("font: 9.5pt \"휴먼엑스포\"")


        # musicPlay_button_1 -> 음원 재생 버튼
        self.musicPlay_button_1 = QtWidgets.QPushButton(self.tab_1)
        self.musicPlay_button_1.setGeometry(QtCore.QRect(170, 154, 110, 31))
        self.musicPlay_button_1.setObjectName("musicPlay_button_1")
        self.musicPlay_button_1.setText(_translate("MainWindow", "play"))
        self.musicPlay_button_1.setStyleSheet("font: 10pt \"휴먼엑스포\"")

        # moviePlay_button_1 -> 뮤비 재생 버튼
        self.moviePlay_button_1 = QtWidgets.QPushButton(self.tab_1)
        self.moviePlay_button_1.setGeometry(QtCore.QRect(280, 154, 110, 31))
        self.moviePlay_button_1.setObjectName("moviePlay_button_1")
        self.moviePlay_button_1.setText(_translate("MainWindow", "movieView"))
        self.moviePlay_button_1.setStyleSheet("font: 10pt \"휴먼엑스포\"")

        # tableWidget_1 -> TOP 100 재생목록 테이블로 띄워줌
        self.tableWidget_1 = QtWidgets.QTableWidget(self.tab_1)
        self.tableWidget_1.setGeometry(QtCore.QRect(0, 220, 450, 285))
        self.tableWidget_1.setObjectName("tableWidget")
        self.tableWidget_1.setColumnCount(3)  # Column
        self.tableWidget_1.setRowCount(100)  # Row
        self.tableWidget_1.setStyleSheet("font: 9pt \"맑은 고딕\";")

        header1 = self.tableWidget_1.horizontalHeader()
        header1.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header1.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header1.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header1.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        # tableWidget_1 요소 생성 -> 인덱스별 item 생성
        for i in range(100):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget_1.setVerticalHeaderItem(i, item)
            for j in range(3):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget_1.setHorizontalHeaderItem(i, item)
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget_1.setItem(i, j, item)
                #item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)

        # tableWidget_1 행/열 정보 -> 행/열 정보 구성
        for i in range(100):
            item = self.tableWidget_1.verticalHeaderItem(i)
            item.setText(_translate("dialog", str(i + 1)))
            if i == 0:
                item = self.tableWidget_1.horizontalHeaderItem(i)
                item.setText(_translate("dialog", "노래제목"))
            if i == 1:
                item = self.tableWidget_1.horizontalHeaderItem(i)
                item.setText(_translate("dialog", "가수"))
            if i == 2:
                item = self.tableWidget_1.horizontalHeaderItem(i)
                item.setText(_translate("dialog", "장르"))

        # tableWidget_1 정렬기능
        __sortingEnabled = self.tableWidget_1.isSortingEnabled()
        self.tableWidget_1.setSortingEnabled(False)


        try:
            # 파일정보 읽어서 생성한 각 요소(item)에 넣어주기
            # 파일 읽기, 5.26 작업
            if self.pushButton_1.isChecked():
                self.music_list = self.file_read(self.pushButton_1.text())
            elif self.pushButton_2.isChecked():
                self.music_list = self.file_read(self.pushButton_2.text())
            elif self.pushButton_3.isChecked():
                self.music_list = self.file_read(self.pushButton_3.text())
            elif self.pushButton_4.isChecked():
                self.music_list = self.file_read(self.pushButton_4.text())
            elif self.pushButton_5.isChecked():
                self.music_list = self.file_read(self.pushButton_5.text())

            for i in range(100):
                for j in range(3):
                    if j == 0:
                        item = self.tableWidget_1.item(i, j)
                        item.setText(_translate("dialog", str(self.music_list[i][1])))
                        continue
                    if j == 1:
                        item = self.tableWidget_1.item(i, j)
                        item.setText(_translate("dialog", str(self.music_list[i][2])))
                        continue
                    if j == 2:
                        item = self.tableWidget_1.item(i, j)
                        item.setText(_translate("dialog", str(self.music_list[i][3])))
                        continue
                    #item = self.tableWidget_1.item(i, j)
                    #item.setText(_translate("dialog", str(self.music_list[i][j])))

            # 탭1에서 초기화면(사이트 선택) 돌아가기 버튼
            self.tab_1_init_button = QtWidgets.QPushButton(self.tab_1)
            self.tab_1_init_button.setGeometry(QtCore.QRect(392, 0, 55, 35))
            self.tab_1_init_button.setObjectName("tab_1_init_button")
            self.tab_1_init_button.setText("Reset")
            self.tab_1_init_button.setStyleSheet("font: 9pt \"휴먼엑스포\"")


            # 위에 지금까지 구성한 tab_1(TOP100) 위젯을 탭위젯에 add함
            self.tabWidget.addTab(self.tab_1, "")

            # 뮤비(음원)추출, 음원 재생, 뮤비재생
            self.mvSave_button_1.clicked.connect(self.mv_crawler)
            self.musicPlay_button_1.clicked.connect(self.music_play1)
            self.moviePlay_button_1.clicked.connect(self.movie_play1)
            # tableWidget_1의 클릭 이벤트 -> 셀 클릭을 하면 해당 행의 '노래제목 - 가수' text가 가운데 textBrowser에 출력됨
            self.tableWidget_1.cellClicked.connect(lambda: self.top100_cellClicked_event(self.tableWidget_1.currentRow()))
            # 탭1에서 초기화면(사이트 선택)으로 돌아가는 클릭 이벤트
            self.tab_1_init_button.clicked.connect(self.init_rayout)
            # ------------------여기까지 탭1의 정보----------------------------






            # 탭2 (장르별) -> 장르별 재생목록
            # 탭1과 유사한 구성 -> textBrowser, label, button, table 등

            # 탭2 위젯으로 생성(장르별)
            self.tab_2 = QtWidgets.QWidget()  # 장르별 탭(창 하나의 위젯)
            self.tab_2.setObjectName("tab_2")

            self.textBrowser_2 = QtWidgets.QTextBrowser(self.tab_2)
            self.textBrowser_2.setGeometry(QtCore.QRect(60, 75, 330, 110))
            self.textBrowser_2.setObjectName("textBrowser_2")
            _translate = QtCore.QCoreApplication.translate
            self.textBrowser_2.setHtml(_translate("MainWindow",
                                                  "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                  "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                  "p, li { white-space: pre-wrap; }\n"
                                                  "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                  "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
            self.textBrowser_2.setStyleSheet("font: 10pt \"HY목각파임B\"")


            self.label_2 = QtWidgets.QLabel(self.tab_2)
            self.label_2.setGeometry(QtCore.QRect(60, 45, 330, 30))
            self.label_2.setObjectName("label_1")
            self.label_2.setAlignment(Qt.AlignCenter) # 중앙정렬
            self.label_2.setText(keyword + " MusicPlayer")
            # self.label_2.setText(_translate("MainWindow","<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">MusicPlayer</span></p></body></html>"))
            self.label_2.setStyleSheet("border-style:solid; border-width:0.5px; border-color: rgb(255,255,255); font: 12pt \"휴먼옛체\"")


            # mv_save -> 버튼으로 뮤비(음원) 추출
            self.mvSave_button_2 = QtWidgets.QPushButton(self.tab_2)
            self.mvSave_button_2.setGeometry(QtCore.QRect(60, 154, 110, 31))
            self.mvSave_button_2.setObjectName("mvSave_button_2")
            self.mvSave_button_2.setText(_translate("MainWindow", "Download"))
            self.mvSave_button_2.setStyleSheet("font: 9.5pt \"휴먼엑스포\"")

            # musicPlay_button_1 -> 음원 재생 버튼
            self.musicPlay_button_2 = QtWidgets.QPushButton(self.tab_2)
            self.musicPlay_button_2.setGeometry(QtCore.QRect(170, 154, 110, 31))
            self.musicPlay_button_2.setObjectName("musicPlay_button_2")
            self.musicPlay_button_2.setText(_translate("MainWindow", "play"))
            self.musicPlay_button_2.setStyleSheet("font: 10pt \"휴먼엑스포\"")

            # moviePlay_button_1 -> 뮤비 재생 버튼
            self.moviePlay_button_2 = QtWidgets.QPushButton(self.tab_2)
            self.moviePlay_button_2.setGeometry(QtCore.QRect(280, 154, 110, 31))
            self.moviePlay_button_2.setObjectName("moviePlay_button_2")
            self.moviePlay_button_2.setText(_translate("MainWindow", "movieView"))
            self.moviePlay_button_2.setStyleSheet("font: 10pt \"휴먼엑스포\"")

            self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
            self.tableWidget_2.setGeometry(QtCore.QRect(0, 220, 450, 285))
            self.tableWidget_2.setObjectName("")
            self.tableWidget_2.setColumnCount(3)
            self.tableWidget_2.setRowCount(100)
            self.tableWidget_2.setStyleSheet("font: 9pt \"맑은 고딕\"")

            header2 = self.tableWidget_2.horizontalHeader()
            header2.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            header2.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header2.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            header2.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)


            for i in range(100):
                gerne_item = QtWidgets.QTableWidgetItem()
                self.tableWidget_2.setVerticalHeaderItem(i, gerne_item)
                for j in range(3):
                    gerne_item = QtWidgets.QTableWidgetItem()
                    self.tableWidget_2.setHorizontalHeaderItem(i, gerne_item)
                    gerne_item = QtWidgets.QTableWidgetItem()
                    self.tableWidget_2.setItem(i, j, gerne_item)

            for i in range(100):
                gerne_item = self.tableWidget_2.verticalHeaderItem(i)
                gerne_item.setText(_translate("dialog", str(i + 1)))
                if i == 0:
                    gerne_item = self.tableWidget_2.horizontalHeaderItem(i)
                    gerne_item.setText(_translate("dialog", "노래제목"))
                if i == 1:
                    gerne_item = self.tableWidget_2.horizontalHeaderItem(i)
                    gerne_item.setText(_translate("dialog", "가수"))
                if i == 2:
                    gerne_item = self.tableWidget_2.horizontalHeaderItem(i)
                    gerne_item.setText(_translate("dialog", "장르"))



            # 장르별 버튼
            genreName = ['댄스', 'POP', '발라드', '록/포크', 'R&B/Soul', '힙합', 'OST', '트로트', '재즈/인디']

            # 장르별 버튼 생성
            self.dance_button = QtWidgets.QPushButton(self.tab_2)
            self.dance_button.setGeometry(QtCore.QRect(4, 187, 45, 30))
            self.dance_button.setObjectName(genreName[0])
            self.dance_button.setStyleSheet("font: 8pt \"휴먼엑스포\"")

            self.pop_button = QtWidgets.QPushButton(self.tab_2)
            self.pop_button.setGeometry(QtCore.QRect(53, 187, 45, 30))
            self.pop_button.setObjectName(genreName[1])
            self.pop_button.setStyleSheet("font: 8pt \"휴먼엑스포\"")

            self.ballade_button = QtWidgets.QPushButton(self.tab_2)
            self.ballade_button.setGeometry(QtCore.QRect(102, 187, 45, 30))
            self.ballade_button.setObjectName(genreName[2])
            self.ballade_button.setStyleSheet("font: 8pt \"휴먼엑스포\"")

            self.rock_button = QtWidgets.QPushButton(self.tab_2)
            self.rock_button.setGeometry(QtCore.QRect(151, 187, 45, 30))
            self.rock_button.setObjectName(genreName[3])
            self.rock_button.setStyleSheet("font: 8pt \"휴먼엑스포\"")

            self.rnb_button = QtWidgets.QPushButton(self.tab_2)
            self.rnb_button.setGeometry(QtCore.QRect(200, 187, 45, 30))
            self.rnb_button.setObjectName(genreName[4])
            self.rnb_button.setStyleSheet("font: 7pt \"휴먼엑스포\"")

            self.hiphop_button = QtWidgets.QPushButton(self.tab_2)
            self.hiphop_button.setGeometry(QtCore.QRect(249, 187, 45, 30))
            self.hiphop_button.setObjectName(genreName[5])
            self.hiphop_button.setStyleSheet("font: 8pt \"휴먼엑스포\"")

            self.ost_button = QtWidgets.QPushButton(self.tab_2)
            self.ost_button.setGeometry(QtCore.QRect(298, 187, 45, 30))
            self.ost_button.setObjectName(genreName[6])
            self.ost_button.setStyleSheet("font: 8pt \"휴먼엑스포\"")

            self.trot_button = QtWidgets.QPushButton(self.tab_2)
            self.trot_button.setGeometry(QtCore.QRect(347, 187, 45, 30))
            self.trot_button.setObjectName(genreName[7])
            self.trot_button.setStyleSheet("font: 8pt \"휴먼엑스포\"")

            self.jazz_button = QtWidgets.QPushButton(self.tab_2)
            self.jazz_button.setGeometry(QtCore.QRect(396, 187, 45, 30))
            self.jazz_button.setObjectName(genreName[8])
            self.jazz_button.setStyleSheet("font: 8pt \"휴먼엑스포\"")

            # 장르별 버튼 text정보
            self.dance_button.setText(_translate("MainWindow", genreName[0]))
            self.pop_button.setText(_translate("MainWindow", genreName[1]))
            self.ballade_button.setText(_translate("MainWindow", genreName[2]))
            self.rock_button.setText(_translate("MainWindow", genreName[3]))
            self.rnb_button.setText(_translate("MainWindow", genreName[4]))
            self.hiphop_button.setText(_translate("MainWindow", genreName[5]))
            self.ost_button.setText(_translate("MainWindow", genreName[6]))
            self.trot_button.setText(_translate("MainWindow", genreName[7]))
            self.jazz_button.setText(_translate("MainWindow", genreName[8]))

            # 초기화면 돌아가는 버튼
            self.tab_2_init_button = QtWidgets.QPushButton(self.tab_2)
            self.tab_2_init_button.setGeometry(QtCore.QRect(392, 0, 55, 35))
            self.tab_2_init_button.setObjectName("tab_2_init_button")
            self.tab_2_init_button.setText("Reset")
            self.tab_2_init_button.setStyleSheet("font: 9pt \"휴먼엑스포\"")

            # --------------여기까지 탭2(장르별) 정보임--------------------------

            # 지금까지 만든 탭1과 탭2를 tabWidget에 넣어줌 << tabWidget은 page_3에 구성된 상태임
            self.tabWidget.addTab(self.tab_1, 'All')
            self.tabWidget.addTab(self.tab_2, 'Genre')

            # 그러므로 스택위젯에 탭위젯을 넣는게 아닌 page_3 위젯을 add해줌
            self.stackedWidget.addWidget(self.page_3)

            # 페이지 이동
            self.stackedWidget.setCurrentWidget(self.page_3)

            # 장르 선택 버튼 이벤트 -> 장르를 선택하면 테이블에 노래정보가 채워짐
            self.dance_button.clicked.connect(lambda: self.genre_list_event(genreName[0]))
            self.pop_button.clicked.connect(lambda: self.genre_list_event(genreName[1]))
            self.ballade_button.clicked.connect(lambda: self.genre_list_event(genreName[2]))
            self.rock_button.clicked.connect(lambda: self.genre_list_event(genreName[3]))
            self.rnb_button.clicked.connect(lambda: self.genre_list_event(genreName[4]))
            self.hiphop_button.clicked.connect(lambda: self.genre_list_event(genreName[5]))
            self.ost_button.clicked.connect(lambda: self.genre_list_event(genreName[6]))
            self.trot_button.clicked.connect(lambda: self.genre_list_event(genreName[7]))
            self.jazz_button.clicked.connect(lambda: self.genre_list_event(genreName[8][0:2]))

            # 탭2의 tableWidget 셀 클릭 이벤트 -> 해당 노래정보 출력
            self.tableWidget_2.cellClicked.connect(lambda: self.genre_cellClicked_event(self.tableWidget_2.currentRow()))

            # 추출, 음원 재생, 뮤비 재생, 초기화면 돌아가기
            self.mvSave_button_2.clicked.connect(self.mv_crawler)
            self.musicPlay_button_2.clicked.connect(self.music_play2)
            self.moviePlay_button_2.clicked.connect(self.movie_play2)
            self.tab_2_init_button.clicked.connect(self.init_rayout)

        except FileNotFoundError:
            print("파일이 업서용!")

    # 뮤비(음원) 추출하는 이벤트 함수
    def mv_crawler(self):
        print("뮤비 추츌")
        keyword = self.textBrowser_1.toPlainText()
        path = './src/merge' + keyword + ".mp4"

        if os.path.isfile(path):
            pass
        else:
            self.x2 = Thread2(self, keyword)
            self.x2.start()

    # 음원 재생 이벤트 함수
    def music_play1(self):
        from music_player import AudioPlayer

        keyword = self.textBrowser_1.toPlainText()
        print(keyword)

        v = AudioPlayer(keyword)
        v.showModal()

    # 음원 재생 이벤트 함수
    def music_play2(self):
        from music_player import AudioPlayer

        keyword = self.textBrowser_2.toPlainText()

        v = AudioPlayer(keyword)
        v.showModal()

    # 뮤비 재생하는 이벤트 함수
    def movie_play1(self):
        from video_player import VideoPlayer

        keyword = self.textBrowser_1.toPlainText()
        v = VideoPlayer(keyword)
        v.showModal()

    def movie_play2(self):
        from video_player import VideoPlayer

        keyword = self.textBrowser_2.toPlainText()

        v = VideoPlayer(keyword)
        v.showModal()

    # TOP100 재생목록의 셀클릭 이벤트 -> 선택 노래정보 출력
    def top100_cellClicked_event(self, row):
        tab1_text = " - ".join(self.music_list[row][1:3])
        self.textBrowser_1.setPlainText(tab1_text)

        keyword = self.textBrowser_1.toPlainText()
        path = './src/merge/' + keyword + ".mp4"
        print(path)

        if os.path.isfile(path):
            self.mvSave_button_1.setEnabled(False)
            self.musicPlay_button_1.setEnabled(True)
            self.moviePlay_button_1.setEnabled(True)
        else:
            self.mvSave_button_1.setEnabled(True)
            self.musicPlay_button_1.setEnabled(False)
            self.moviePlay_button_1.setEnabled(False)

            # 장르별 재생목록의 셀클릭 이벤트 -> 선택 노래정보 출력

    def genre_cellClicked_event(self, row):
        tab2_text = " - ".join(self.genreList[row][1:3])
        self.textBrowser_2.setPlainText(tab2_text)

        keyword = self.textBrowser_2.toPlainText()
        path = './src/merge/' + keyword + ".mp4"
        if os.path.isfile(path):
            self.mvSave_button_2.setEnabled(False)
            self.musicPlay_button_2.setEnabled(True)
            self.moviePlay_button_2.setEnabled(True)
        else:
            self.mvSave_button_2.setEnabled(True)
            self.musicPlay_button_2.setEnabled(False)
            self.moviePlay_button_2.setEnabled(False)

    # 장르별 재생목록에서 장르 선택 시 테이블 채워지는 이벤트 -> 장르 선택하면 테이블이 길이에 맞게 생성됨
    def genre_list_event(self, genre):
        self.genreList = []

        for i in self.music_list:
            if genre in i[3]:
                self.genreList.append(i)

        _translate = QtCore.QCoreApplication.translate
        self.tableWidget_2.setGeometry(QtCore.QRect(0, 220, 450, 285))
        self.tableWidget_2.setObjectName("genre_item")
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setRowCount(len(self.genreList))
        header2 = self.tableWidget_2.horizontalHeader()
        header2.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header2.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header2.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header2.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        for i in range(len(self.genreList)):
            gerne_item = QtWidgets.QTableWidgetItem()
            self.tableWidget_2.setVerticalHeaderItem(i, gerne_item)
            for j in range(3):
                gerne_item = QtWidgets.QTableWidgetItem()
                self.tableWidget_2.setHorizontalHeaderItem(i, gerne_item)
                gerne_item = QtWidgets.QTableWidgetItem()
                self.tableWidget_2.setItem(i, j, gerne_item)

        for i in range(len(self.genreList)):
            gerne_item = self.tableWidget_2.verticalHeaderItem(i)
            gerne_item.setText(_translate("dialog", str(i + 1)))
            if i == 0:
                gerne_item = self.tableWidget_2.horizontalHeaderItem(i)
                gerne_item.setText(_translate("dialog", "노래제목"))
            if i == 1:
                gerne_item = self.tableWidget_2.horizontalHeaderItem(i)
                gerne_item.setText(_translate("dialog", "가수"))
            if i == 2:
                gerne_item = self.tableWidget_2.horizontalHeaderItem(i)
                gerne_item.setText(_translate("dialog", "장르"))

        for i in range(len(self.genreList)):
            for j in range(3):
                if j == 0:
                    gerne_item = self.tableWidget_2.item(i, j)
                    gerne_item.setText(_translate("dialog", str(self.genreList[i][1])))
                    continue
                if j == 1:
                    gerne_item = self.tableWidget_2.item(i, j)
                    gerne_item.setText(_translate("dialog", str(self.genreList[i][2])))
                    continue
                if j == 2:
                    gerne_item = self.tableWidget_2.item(i, j)
                    gerne_item.setText(_translate("dialog", str(self.genreList[i][3])))
                    continue
                gerne_item = self.tableWidget_2.item(i, j)
                gerne_item.setText(_translate("dialog", str(self.genreList[i][j])))
        return self.genreList

    # 초기화면으로 돌아가는 이벤트 함수 -> reset 버튼 누를 시 초기 사이트 선택으로 넘어감
    def init_rayout(self):
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()


    # 파일정보 읽기
    def file_read(self, music_site):
        now = dt.now()
        day = now.strftime('%Y%m%d')
        path = "./songList/" + music_site + "_" + day + ".csv"

        import csv
        slist = []
        f = open(path, encoding="UTF8")
        rdr = csv.reader(f)
        for line in rdr:
            if line[1] == '제목':  # 처음 순위 제거
                continue
            slist.append(line)
        f.close()
        return slist  # 노래정보 담기기


# main
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    app.setStyle('Windows')
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    qtmodern.styles.dark(app)
    MainWindow.show()
    sys.exit(app.exec_())

