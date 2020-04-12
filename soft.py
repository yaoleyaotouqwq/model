import os
import pickle
import sys

from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyecharts import Bar, Pie, Line, Radar
from qtpy import QtCore, QtGui

import GUI_Parameter as Parameter

import path_define as Model_Parameter

import Data as Data_change
import Model


class Stacked(QWidget):
    def __init__(self):
        super(Stacked, self).__init__()
        self.initUI()
        self.mainLayout()

    def initUI(self):
        self.setGeometry(400, 400, 800, 600)
        self.setWindowTitle("demo1")

    def mainLayout(self):
        step_list = [0]
        self.button = QPushButton()
        self.mainhboxLayout = QHBoxLayout(self)
        self.frame = QFrame(self)
        self.mainhboxLayout.addWidget(self.frame)
        self.mainhboxLayout.addWidget(self.button)
        self.hboxLayout = QHBoxLayout(self.frame)

        self.myHtml = QWebEngineView(self)

        # 预测按钮or重新训练按钮
        self.button.clicked.connect(self.func1)

    def func1(self):

        # 构造折线图
        line1 = Line(Parameter.Visual_Graph["Func_name"][3])
        # Loss图
        line1.add("1", self.data_x, self.data_y,
                  xaxis_rotate=Parameter.Visual_Graph["Line_x_rotate"],
                  is_label_show=True, is_smooth=True)

        line1.render(path=Model_Parameter.Echarts_path +
                     "1" + ".html")

        self.myHtml.load(QUrl("file:///" + r"/".join(
            os.getcwd().split("\\")) + "/" + Model_Parameter.Echarts_path + "1" + ".html"))

        self.hboxLayout.addWidget(self.myHtml)
        self.setLayout(self.mainhboxLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Stacked()
    ex.show()
    sys.exit(app.exec_())
