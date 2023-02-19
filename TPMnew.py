import os
import sys
from PyQt5 import uic
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import pandas as pd

# 그래프 그리기 모듈
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# Qt Designer 연결
qtFile = "TPMnew.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtFile)

# images 파일 리스트 가져오기
path = "./images/"
file_list = os.listdir(path)
print("images 파일 리스트\n",file_list)

# datetime, 온도, 습도, CT, CP 가져오기
df = pd.read_csv("./datas/tem_hum.csv",usecols = ["datetime","tem","hum","CT","CP"])

# 그래프 그릴 csv
csv = pd.read_csv("./datas/normal.csv", usecols = ["CT","CP"])

# x, y 범위
def make_range(flag, csv, cur):
    interval = 0
    wid = 0
    if flag == "CT":
        xran = np.arange(0, 63, 3)  # 0~63 까지 간격 3
        interval = 3
        wid = 1.8
    elif flag == "CP":
        xran = np.arange(-1.65, 2.6, 0.05)  # -1.65 ~2.55 까지 간격 0.05
        interval = 0.05
        wid = 0.035
    yran = [0] * (len(xran) - 1)
    color_idx = [0] * len(yran)
    i = 0
    for x in xran[:-1]:
        start, end = x, x + interval
        temp = csv[(csv[flag] >= start) & (csv[flag] < end)]
        yran[i] = len(temp[flag])
        if cur >= start and cur < end:
            color_idx[i] = 1
        i += 1
    if flag == "CT": xran = np.arange(0 + 1.5, 60 + 1.5, 3.00)
    elif flag == "CP": xran = np.arange((xran[0] + xran[1]) / 2, (xran[-1] + xran[-2]) / 2, 0.05)
    return flag, xran, yran, wid, color_idx


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas,self).__init__(self.fig)



class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.count = 0
        # 날짜
        self.date0.setDate(QDate.currentDate())
        self.date0.setMinimumDate(QDate(2017,1,1))
        self.date0.setMaximumDate(QDate(2021, 12, 31))
        self.date0.dateChanged.connect(self.loadImage)

        # 시간
        self.curtime = QTime.currentTime()
        self.timebox.currentIndexChanged.connect(self.loadImage)

        self.cnt = 0

        # 그래프
        # x = 550 / self.fig1.dpi  # 가로 길이
        # y = 328 / self.fig1.dpi  # 세로 길이
        # self.fig1.set_figwidth(x)
        # self.fig1.set_figheight(y)



    # def loadGraph(self):
        # 그래프를 이미지로
        '''self.qPix_han = QPixmap()
        self.qPix_han.load("./images/new 한온그.png")
        self.qPix_cp = QPixmap()
        self.qPix_cp.load("./images/new 공능그.png")
        self.qPix_han = self.qPix_han.scaledToHeight(360)
        self.lb_han.setPixmap(self.qPix_han)
        self.qPix_cp = self.qPix_cp.scaledToHeight(360)
        self.lb_cp.setPixmap(self.qPix_cp)'''

#CT
    def DoGraphCT(self, cur):
        self.vl_CT.removeWidget(self.lb_han)
        self.lb_han.setParent(None)
        flag1, xran1, yran1, wid1, color_idx1 = make_range("CT", csv, cur)
        for i in range(len(color_idx1)):
            if color_idx1[i] == 0:
                color_idx1[i] = "Silver"
            else: color_idx1[i] = "coral"

        self.sc = MplCanvas()
# 툴바 필요시        # self.toolbar1 = NavigationToolbar(self.sc, self)
        self.sc.axes.cla()
        self.sc.axes.bar(xran1, yran1, width = wid1, color = color_idx1)
        # self.sc.axes.set_ylabel('count')
        # self.sc.axes.set_xlabel(flag1)
        self.sc.axes.axvline(55, 0, 1, color="navy", linestyle='-', linewidth='3')

        # self.vl_CT.addWidget(toolbar1)
        self.vl_CT.addWidget(self.sc)
        self.sc.draw()
#CP
    def DoGraphCP(self, cur):
        self.vl_CP.removeWidget(self.lb_cp)
        self.lb_cp.setParent(None)
        flag2, xran2, yran2, wid2, color_idx2 = make_range("CP", csv, cur)

        self.sc1 = MplCanvas()
        fig = plt.Figure()
        y = 350 / fig.dpi  # 세로 길이
        self.sc1.fig.set_figheight(y)
        self.toolbar2 = NavigationToolbar(self.sc1, self)
        # self.sc1.axes.cla()
        self.sc1.axes.bar(xran2, yran2, width = wid2, color = "royalblue")
        # self.sc1.axes.set_ylabel('count')
        # self.sc1.axes.set_xlabel(flag2)
        "deeppink""silver"
        cp_nums = [1.67, 1.33, 1.0, 0.67]
        for c in cp_nums:
            self.sc1.axes.axvline(c, 0, 1, color="silver", linestyle='-', linewidth='2.5')
        if self.grade == 0:
            self.sc1.axes.axvline(1.67, 0, 1, color="deeppink", linestyle='-', linewidth='2.5')
        elif self.grade == 1:
            self.sc1.axes.axvline(1.33, 0, 1, color="deeppink", linestyle='-', linewidth='2.5')
        elif self.grade == 2:
            self.sc1.axes.axvline(1.0, 0, 1, color="deeppink", linestyle='-', linewidth='2.5')
        elif self.grade == 3:
            self.sc1.axes.axvline(0.67, 0, 1, color="deeppink", linestyle='-', linewidth='2.5')

        self.vl_CP.addWidget(self.toolbar2)
        self.vl_CP.addWidget(self.sc1)
        self.sc1.draw()

    def loadImage(self): # 날짜에 맞춰 이미지와 온도,습도 데이터 넣기
        self.count += 1
        selected_time = self.timebox.currentText()
        # selected_time = "   오후 21:00" -> 21
        time = selected_time[-5:-3]
        date = self.date0.date()
        date = date.toString("yyyyMMdd")
        datetime = date + time
        print(datetime)
        # 선택된 날짜 + 시간의 이미지가 images 폴더에 있으면
        # datetime0 은 원본 datetime1 은 열화상
        # 2021070521 # 2021070609 # 2021070818

        if '%s0.png'%datetime in file_list and '%s1.png'%datetime in file_list:
            self.cnt += 1

        # 열화상 이미지
            self.qPix_origin = QPixmap()
            self.qPix_gaek = QPixmap()
            self.qPix_origin.load("./images/%s0"%datetime)
            self.qPix_gaek.load("./images/%s1"%datetime)
            # 사이즈 맞추기
            self.qPix_origin = self.qPix_origin.scaled(297,247)
            self.qPix_gaek = self.qPix_gaek.scaled(297, 247)
            # 이미지 넣기
            self.lb_origin.setPixmap(self.qPix_origin)
            self.lb_gaek.setPixmap(self.qPix_gaek)

        # 온도, 습도 넣기
            row = df[df["datetime"]==int(datetime)]
            self.tem.setText("%.1f °C"%row["tem"])
            self.hum.setText("%d %%"%row["hum"])
            print("날짜: %d 온도: %.1f 습도: %d"%(row["datetime"],row["tem"],row["hum"]))

        # CT 현재온도, 공정능력지수 Cp
            self.lb_cur.setText("%.1f"%row["CT"])
            self.lb_55.setText("%d"%55)
            self.lb_cpval.setText("%.2f"%row["CP"])
            self.cp, self.grade = float(row["CP"]), 0
            if self.cp > 1.67:
                self.grade = 0
                self.lb_state.setText("안정")
                self.lb_state.setStyleSheet("color:rgb(0, 170, 0); font: 75 10pt '나눔스퀘어_ac ExtraBold';")
            elif self.cp > 1.33:
                self.grade = 1
                self.lb_state.setText("안정")
                self.lb_state.setStyleSheet("color:rgb(0, 170, 0); font: 75 10pt '나눔스퀘어_ac ExtraBold';")
            elif self.cp > 1.00:
                self.grade = 2
                self.lb_state.setText("주의")
                self.lb_state.setStyleSheet("color: rgb(220, 0, 0); font: 75 10pt '나눔스퀘어_ac ExtraBold';")
            elif self.cp > 0.67:
                self.grade = 3
                self.lb_state.setText("주의")
                self.lb_state.setStyleSheet("color: rgb(220, 0, 0); font: 75 10pt '나눔스퀘어_ac ExtraBold';")
            else:
                self.grade = 4
                self.lb_state.setText("위험")
                self.lb_state.setStyleSheet("color: rgb(220, 0, 0); font: 75 10pt '나눔스퀘어_ac ExtraBold';")
            self.lb_grade.setText("%d" %self.grade)
            print("날짜: %d CT: %.2f 등급: %d Cp: %.2f"%(row["datetime"],row["CT"],self.cp,self.grade))

        # 그래프 로드
            if self.cnt > 1:
                self.vl_CT.removeWidget(self.sc)
                self.vl_CP.removeWidget(self.sc1)
                self.vl_CP.removeWidget(self.toolbar2)
                self.sc.setParent(None)
                self.sc1.setParent(None)
                self.toolbar2.setParent(None)
            self.DoGraphCT(float(row["CT"]))
            self.DoGraphCP(self.grade)

        else:
            self.lb_origin.setText("<원본 이미지>")
            self.lb_gaek.setText("<열화상 이미지>")
            self.tem.setText("     °C")
            self.hum.setText("    %")
            self.lb_cur.setText("_____")
            self.lb_55.setText("___")
            self.lb_cpval.setText("_____")
            self.lb_grade.setText("__")
            self.lb_state.setText("_____")

            if self.cnt >= 1:
                self.sc.setParent(None)
                self.sc1.setParent(None)
                self.toolbar2.setParent(None)
                self.vl_CT.addWidget(self.lb_han)
                self.vl_CP.addWidget(self.lb_cp)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())