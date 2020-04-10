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


# 主窗口
class MainWindow(QMainWindow):
    # *args是非关键字参数，用于元组，**kwargs是关键字参数 （字典）
    def __init__(self , *args , **kwargs):
        # super() 调用父类(超类)的一个方法。
        super().__init__(*args , **kwargs)

        self.model_LR = Model.LR()
        self.model_SVM = Model.SVM()
        self.model_DNN = Model.DNN()

        self.db = self.connect_Db()
        self.query = QSqlQuery()
        # 数据表视图
        self.table_model = QSqlTableModel()
        self.mainwindow_layout()

        # 个人信息界面
        self.infor = Information(self)
        # 预测界面
        self.predict = Predict(self)
        # 数据可视化图表界面
        self.echarts = Echarts(self)
        # 查找界面
        self.search_dialog = Search_dialog(self)
        # 登录界面，首先执行
        self.dialog = Login_dialog()
        self.dialog.show()

        self.dialog.login_sendmsg.connect(self.get_slot)

    def connect_Db(self):
        # 连接数据库
        db = QSqlDatabase.addDatabase(Parameter.Db["Db_app"])
        db.setHostName(Parameter.Db['HostName'])
        db.setPort(Parameter.Db['Port'])
        db.setDatabaseName(Parameter.Db['Db_Name'])
        db.setUserName(Parameter.Db['Username'])
        db.setPassword(Parameter.Db['Password'])

        if not db.open():
            db.close()
            exit()

        return db

    # 关闭程序后
    def closeEvent(self, *args, **kwargs):
        # 断开数据库连接
        self.db.close()

    def initialize_table(self):
        self.table_model.setTable('score_data')
        self.table_model.setHeaderData(0, Qt.Horizontal, Parameter.Tablefield_Name[0])
        self.table_model.setHeaderData(1, Qt.Horizontal, Parameter.Tablefield_Name[1])
        self.table_model.setHeaderData(2, Qt.Horizontal, Parameter.Tablefield_Name[2])
        self.table_model.setHeaderData(3, Qt.Horizontal, Parameter.Tablefield_Name[3])
        self.table_model.setHeaderData(4, Qt.Horizontal, Parameter.Tablefield_Name[4])
        self.table_model.setHeaderData(5, Qt.Horizontal, Parameter.Tablefield_Name[5])
        self.table_model.setHeaderData(6, Qt.Horizontal, Parameter.Tablefield_Name[6])
        self.table_model.setHeaderData(7, Qt.Horizontal, Parameter.Tablefield_Name[7])
        self.table_model.setHeaderData(8, Qt.Horizontal, Parameter.Tablefield_Name[8])
        self.table_model.setHeaderData(9, Qt.Horizontal, Parameter.Tablefield_Name[9])
        self.table_model.setHeaderData(10, Qt.Horizontal, Parameter.Tablefield_Name[10])
        self.table_model.setHeaderData(11, Qt.Horizontal, Parameter.Tablefield_Name[11])
        self.table_model.setHeaderData(12, Qt.Horizontal, Parameter.Tablefield_Name[12])
        self.table_model.setHeaderData(13, Qt.Horizontal, Parameter.Tablefield_Name[13])
        self.table_model.setHeaderData(14, Qt.Horizontal, Parameter.Tablefield_Name[14])
        self.table_model.setHeaderData(15, Qt.Horizontal, Parameter.Tablefield_Name[15])
        self.table_model.setHeaderData(16, Qt.Horizontal, Parameter.Tablefield_Name[16])
        self.table_model.setHeaderData(17, Qt.Horizontal, Parameter.Tablefield_Name[17])
        self.table_model.setHeaderData(18, Qt.Horizontal, Parameter.Tablefield_Name[18])
        self.table_model.setHeaderData(19, Qt.Horizontal, Parameter.Tablefield_Name[19])
        self.table_model.setHeaderData(20, Qt.Horizontal, Parameter.Tablefield_Name[20])
        self.table_model.setHeaderData(21, Qt.Horizontal, Parameter.Tablefield_Name[21])
        self.table_model.setHeaderData(22, Qt.Horizontal, Parameter.Tablefield_Name[22])
        self.table_model.setHeaderData(23, Qt.Horizontal, Parameter.Tablefield_Name[23])
        self.table_model.setHeaderData(24, Qt.Horizontal, Parameter.Tablefield_Name[24])
        self.table_model.setHeaderData(25, Qt.Horizontal, Parameter.Tablefield_Name[25])
        self.table_model.setHeaderData(26, Qt.Horizontal, Parameter.Tablefield_Name[26])
        self.table_model.setHeaderData(27, Qt.Horizontal, Parameter.Tablefield_Name[27])

    def mainwindow_layout(self):
        self.setWindowTitle(Parameter.Window_Name["Main"])
        self.resize(Parameter.Window_Size["Width"]["Main"], Parameter.Window_Size["Height"]["Main"])

        # 把窗口的问号按钮去掉
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # 初始化数据表
        self.initialize_table()

        # 建立分割窗口和各类小控件
        self.main_splitter = QSplitter()
        self.left_splitter = QSplitter()
        self.right_splitter = QSplitter()
        self.right_splitter_text = QSplitter()
        self.right_splitter_button = QSplitter()
        self.label1 = QLabel("")
        self.label2 = QLabel("")
        self.label1.setAlignment(QtCore.Qt.AlignRight)
        self.label2.setAlignment(QtCore.Qt.AlignRight)
        self.button1 = QPushButton()
        self.button2 = QPushButton()
        self.button3 = QPushButton()
        self.button4 = QPushButton()

        # 表视图
        self.table_view = QTableView()
        self.table_view.setModel(self.table_model)
        self.table_view.setWindowTitle(Parameter.TableView_Name)
        # 隐藏列头
        self.table_view.verticalHeader().hide()
        # 监听鼠标点击事件
        self.table_view.doubleClicked.connect(self.doubleClicked)

        # 将两个局部分割布局为垂直布局
        self.left_splitter.setOrientation(Qt.Vertical)
        self.right_splitter.setOrientation(Qt.Vertical)

        #  数据表文字提示为垂直布局
        self.right_splitter_text.setOrientation(Qt.Vertical)
        # 数据表功能按钮提示为水平布局
        self.right_splitter_button.setOrientation(Qt.Horizontal)

        # 变为不可拉伸
        self.left_splitter.setOpaqueResize(False)
        self.right_splitter.setOpaqueResize(False)
        self.right_splitter_text.setOpaqueResize(False)
        self.right_splitter_button.setOpaqueResize(False)

        # 依次装入左布局
        self.left_splitter.addWidget(self.button1)
        self.left_splitter.addWidget(self.button2)

        # 先将文字和按钮加入局部布局再加入到与数据表的垂直布局
        self.right_splitter_text.addWidget(self.label1)
        self.right_splitter_text.addWidget(self.label2)
        self.right_splitter_button.addWidget(self.button3)
        self.right_splitter_button.addWidget(self.button4)

        # 依次装入右布局
        self.right_splitter.addWidget(self.right_splitter_text)
        self.right_splitter.addWidget(self.table_view)
        self.right_splitter.addWidget(self.right_splitter_button)

        # 装入总布局
        self.main_splitter.addWidget(self.left_splitter)
        self.main_splitter.addWidget(self.right_splitter)

        # 中心放置
        self.setCentralWidget(self.main_splitter)

        # 个人信息按钮
        self.button1.clicked.connect(self.information)

        # 预测按钮or重新训练按钮
        self.button2.clicked.connect(self.func1)

        # 查找按钮or继续训练按钮
        self.button3.clicked.connect(self.func2)

        # 显示所有数据or展示数据图or评估模型
        self.button4.clicked.connect(self.func3)

    def doubleClicked(self):

        # 教师专用功能
        if self.identity == Parameter.identity["Teacher"]:
            # 双击数据行获取该行账号信息
            index = self.table_view.currentIndex()
            # 需要预测查询窗口或图表展示窗口打开才能使用,同时禁用数据直接修改的功能
            if index.isValid() and (self.predict.isVisible() or self.echarts.isVisible()):
                self.table_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
                record = self.table_model.record(index.row())
                account_string = str(record.value(Parameter.TableView_account_index), encoding="utf-8")

                # 不需要重复生成预测图
                if os.path.exists(Model_Parameter.Echarts_path):
                    for file in os.listdir(Model_Parameter.Echarts_path):
                        if file == account_string + ".html":
                            return

                self.predict.run_predict(str(record.value(Parameter.TableView_account_index), encoding="utf-8"))

                # 弹出图表窗口并关闭预测查询窗口
                if self.predict.isVisible():
                    self.predict.lineEdit_account.setText("")
                    self.predict.setVisible(False)
                    # 设置顶层显示，方便用户操作
                    self.echarts.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
                    self.echarts.show()
            else:
                self.table_view.setEditTriggers(QAbstractItemView.DoubleClicked)

    def information(self):
        # 禁用所有其他按钮保证系统稳定性
        self.button2.setEnabled(False)
        self.button3.setEnabled(False)
        self.button4.setEnabled(False)

        self.infor.account_text.setText(Parameter.Text_label["Infor"]["account"] + self.user_id)
        self.infor.identity_text.setText(Parameter.Text_label["Infor"]["identity"] + self.identity)
        self.infor.lineEdit_name.setText(self.name)
        self.infor.show()

    def func1(self):
        if self.identity == Parameter.identity["Teacher"]:
            # 禁用其他按钮保证系统稳定性
            self.button1.setEnabled(False)
            self.button2.setEnabled(False)
            self.predict.verticalLayout.addLayout(self.predict.level_Layout1)
            self.predict.verticalLayout.addLayout(self.predict.level_Layout5)
            self.predict.show()

        elif self.identity == Parameter.identity["Student"]:
            # 禁用其他按钮保证系统稳定性
            self.button1.setEnabled(False)
            self.button2.setEnabled(False)
            self.button4.setEnabled(False)
            self.predict.verticalLayout.addLayout(self.predict.level_Layout1)
            self.predict.verticalLayout.addLayout(self.predict.level_Layout5)
            self.predict.lineEdit_account.setText(self.user_id)
            self.predict.show()
        else:
            # 禁用其他按钮保证系统稳定性
            self.button1.setEnabled(False)
            self.button2.setEnabled(False)
            self.button3.setEnabled(False)
            self.button4.setEnabled(False)
            msgBox = QMessageBox()
            datas = []
            id = 0
            sql_word = "SELECT * FROM `score_data`"
            self.query.exec_(sql_word)
            while self.query.next():
                datas.append([str(self.query.value(temp), encoding="utf-8")
                         for temp in range(Parameter.Score_data_num["score_start"],
                                           Parameter.Score_data_num["variety"])])
                id = self.query.value(0)

            # 暂定每个模型的batch_size都一样，只有训练集大于一个batch_size才能进行训练
            if len(datas) >= Model_Parameter.Batch_size['LR']:
                with open(Model_Parameter.id_path, 'wb') as f:
                    pickle.dump(int(id), f)

                self.model_LR.LR_train(Model_Parameter.Model_mode[0], datas)
                self.model_SVM.SVM_train(Model_Parameter.Model_mode[0], datas)
                self.model_DNN.DNN_train(Model_Parameter.Model_mode[0], datas)

                msgBox.information(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Train Finish"], QMessageBox.Ok)
            else:
                msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Data Missing"], QMessageBox.Ok)

            # 恢复所有其他按钮
            if not self.button1.isEnabled():
                self.button1.setEnabled(True)
            if not self.button2.isEnabled():
                self.button2.setEnabled(True)
            if not self.button3.isEnabled():
                self.button3.setEnabled(True)
            if not self.button4.isEnabled():
                self.button4.setEnabled(True)

    def func2(self):

        if self.identity == Parameter.identity["Teacher"]:
            self.search_dialog.show()
        elif self.identity == Parameter.identity["Student"]:
            self.search_dialog.lineEdit_account.setText(self.user_id)
            self.search_dialog.show()
        else:
            # 禁用所有其他按钮保证系统稳定性
            self.button1.setEnabled(False)
            self.button2.setEnabled(False)
            self.button3.setEnabled(False)
            self.button4.setEnabled(False)

            msgBox = QMessageBox()
            datas = []
            f = open(Model_Parameter.id_path, 'rb')
            id = pickle.load(f)

            # sql_word = "SELECT * FROM `score_data`"  #测试继续训练是否可用
            sql_word = "SELECT * FROM `score_data` where 序号 > '" + str(id) + "'"
            if self.query.exec_(sql_word):
                while self.query.next():
                    datas.append([str(self.query.value(temp), encoding="utf-8")
                                  for temp in range(Parameter.Score_data_num["score_start"],
                                                    Parameter.Score_data_num["variety"])])
                    id = self.query.value(0)

                    # 暂定每个模型的batch_size都一样，只有新的训练集大于一个batch_size才能继续进行训练
                if len(datas) >= Model_Parameter.Batch_size['LR']:
                    with open(Model_Parameter.id_path, 'wb') as f:
                        pickle.dump(int(id), f)

                    self.model_LR.LR_train(Model_Parameter.Model_mode[1], datas)
                    self.model_SVM.SVM_train(Model_Parameter.Model_mode[1], datas)
                    self.model_DNN.DNN_train(Model_Parameter.Model_mode[1], datas)

                    msgBox.information(self, Parameter.Message_tips["Windows_title"],
                                   Parameter.Message_tips["Train Finish"], QMessageBox.Ok)
                else:
                    msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                                   Parameter.Message_tips["Train Failed"], QMessageBox.Ok)
            else:
                msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Train Failed"], QMessageBox.Ok)

            # 恢复所有其他按钮
            if not self.button1.isEnabled():
                self.button1.setEnabled(True)
            if not self.button2.isEnabled():
                self.button2.setEnabled(True)
            if not self.button3.isEnabled():
                self.button3.setEnabled(True)
            if not self.button4.isEnabled():
                self.button4.setEnabled(True)

    def func3(self):
        if self.identity == Parameter.identity["Teacher"]:
            self.table_model.setTable('score_data')
            self.table_model.select()
        elif self.identity == Parameter.identity["Student"]:

            # 禁用所有其他按钮保证系统稳定性
            self.button1.setEnabled(False)
            self.button2.setEnabled(False)
            self.button4.setEnabled(False)

            # 设置功能区域和图形区域的标题
            self.echarts.label_left.setText(Parameter.Visual_Graph["Graph_Name"][2])
            self.echarts.label_right.setText(Parameter.Visual_Graph["Graph_Name"][1])
            self.echarts.calculate_graph()
            self.echarts.show()
        else:
            # 禁用所有其他按钮保证系统稳定性
            self.button1.setEnabled(False)
            self.button2.setEnabled(False)
            self.button3.setEnabled(False)
            self.button4.setEnabled(False)

            msgBox = QMessageBox()
            datas = []
            id = 0
            sql_word = "SELECT * FROM `score_data`"
            self.query.exec_(sql_word)
            while self.query.next():
                datas.append([str(self.query.value(temp), encoding="utf-8")
                              for temp in range(Parameter.Score_data_num["score_start"],
                                                Parameter.Score_data_num["variety"])])
                id = self.query.value(0)

            # 暂定每个模型的batch_size都一样，只有训练集大于一个batch_size才能进行训练
            if len(datas)//Model_Parameter.Test_K_num >= Model_Parameter.Batch_size['LR']:
                with open(Model_Parameter.id_path, 'wb') as f:
                    pickle.dump(int(id), f)

                LR_ACC = self.model_LR.LR_test(datas)
                SVM_ACC = self.model_SVM.SVM_test(datas)
                DNN_ACC = self.model_DNN.DNN_test(datas)
                print("LR model level is ", LR_ACC)
                print("SVM model level is ", SVM_ACC)
                print("DNN model level is ", DNN_ACC)

                msgBox.information(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Test Finish"], QMessageBox.Ok)
            else:
                msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Test Failed"], QMessageBox.Ok)

            # 恢复所有其他按钮
            if not self.button1.isEnabled():
                self.button1.setEnabled(True)
            if not self.button2.isEnabled():
                self.button2.setEnabled(True)
            if not self.button3.isEnabled():
                self.button3.setEnabled(True)
            if not self.button4.isEnabled():
                self.button4.setEnabled(True)

    def get_slot(self,user_id):
        self.user_id = user_id
        # 显示主界面
        self.setVisible(True)
        self.choose_client()

    def choose_client(self):
        sql_word = "SELECT identity FROM `user` where account='" + self.user_id + "'"
        # 账号密码信息判断,用exec执行sql，用next判断是否成功
        if self.query.exec_(sql_word) and self.query.next():
            # 传递用户身份
            self.identity = str(self.query.value(0), encoding="utf=8")
            sql_word = "SELECT name FROM `user` where account='" + self.user_id + "'"
            if self.query.exec_(sql_word) and self.query.next():
                self.name = str(self.query.value(0), encoding="utf=8")

            # 设置欢迎词
            self.label1.setText(self.identity + "专用")
            self.label2.setText("欢迎用户："+self.user_id)

            # 设置按钮名称
            self.button1.setText(Parameter.Butten_Name["Information"])
            self.button1.setText(Parameter.Butten_Name["Information"])
            if self.identity == Parameter.identity["Teacher"]:
                self.button2.setText(Parameter.Butten_Name["Predict"])
                self.button3.setText(Parameter.Butten_Name["Search"])
                self.button4.setText(Parameter.Butten_Name["Find All"])

            elif self.identity == Parameter.identity["Student"]:
                self.button2.setText(Parameter.Butten_Name["Predict"])
                self.button3.setText(Parameter.Butten_Name["Search"])
                self.button4.setText(Parameter.Butten_Name["Score Graph"])
            else:
                self.button2.setText(Parameter.Butten_Name["Retraining"])
                self.button3.setText(Parameter.Butten_Name["Keep On Train"])
                self.button4.setText(Parameter.Butten_Name["Assessment Model"])

            if self.identity == Parameter.identity["Student"]:
                self.Student_client()
            elif self.identity == Parameter.identity["Teacher"]:
                self.Techer_client()
            else:
                self.Administrator_client()
        else:
            print("Error! the User not normal identity.")
            return

    def Student_client(self):
        # 仅只读数据表
        self.table_model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.statusBar().showMessage("欢迎进入系统.本客户端为学生使用.", 3000)  # 设置状态栏显示的消息

    def Techer_client(self):
        self.table_model.select()

        # 可修改数据表
        self.table_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.statusBar().showMessage("欢迎进入系统.本客户端为教师使用.", 3000)  # 设置状态栏显示的消息

    def Administrator_client(self):
        # 仅可读数据表
        self.table_model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.statusBar().showMessage("欢迎进入系统.本客户端为管理员使用.", 3000)  # 设置状态栏显示的消息


class Information(QDialog):
    def __init__(self,Main_win,*args, **kwargs):
        # super() 调用父类(超类)的一个方法。
        super().__init__(*args , **kwargs)
        self.Main_win = Main_win
        self.window_layout()
        self.item_layout()

    def window_layout(self):
        self.setWindowTitle(Parameter.Window_Name["Infor"])
        self.resize(Parameter.Window_Size["Width"]["Infor"], Parameter.Window_Size["Height"]["Infor"])
        # 固定窗体大小不被拉拽
        self.setFixedSize(self.width(), self.height())
        # 把窗口的问号按钮去掉
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def item_layout(self):

        # 创建垂直布局
        self.verticalLayout = QVBoxLayout()
        # 创建水平布局
        self.level_Layout1 = QHBoxLayout()
        self.level_Layout2 = QHBoxLayout()

        # 单行文本
        self.account_text = QLabel("")
        self.identity_text = QLabel("")
        self.name_text = QLabel(Parameter.Text_label["Infor"]["name"])

        # 单行输入框
        self.lineEdit_name = QLineEdit()

        # 按钮框
        self.change_butten = QPushButton()
        self.cancel_butten = QPushButton()
        self.change_butten.setText(Parameter.Butten_Name["Change"])
        self.cancel_butten.setText(Parameter.Butten_Name["Cancel"])

        # 分别加入水平布局
        self.level_Layout1.addWidget(self.name_text)
        self.level_Layout1.addWidget(self.lineEdit_name)
        self.level_Layout2.addWidget(self.change_butten)
        self.level_Layout2.addWidget(self.cancel_butten)

        # 水平布局控件加入垂直布局
        self.verticalLayout.addWidget(self.account_text)
        self.verticalLayout.addWidget(self.identity_text)
        self.verticalLayout.addLayout(self.level_Layout1)
        self.verticalLayout.addLayout(self.level_Layout2)

        # 处理按钮信号
        self.change_butten.clicked.connect(self.change_click)
        self.cancel_butten.clicked.connect(self.cancel_click)

        self.setLayout(self.verticalLayout)

    def reset_and_quit(self):
        self.lineEdit_name.setText(self.Main_win.name)
        self.setVisible(False)

    def setButtonEnable(self):
        # 恢复其他按钮使用

        if not self.Main_win.button2.isEnabled():
            self.Main_win.button2.setEnabled(True)
        if not self.Main_win.button3.isEnabled():
            self.Main_win.button3.setEnabled(True)
        if not self.Main_win.button4.isEnabled():
            self.Main_win.button4.setEnabled(True)

    def change_click(self):
        msgBox = QMessageBox()

        if self.lineEdit_name.text() == self.Main_win.name:
            msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Not Change"], QMessageBox.Ok)
        else:
            self.Main_win.name = self.lineEdit_name.text()
            msgBox.information(self, Parameter.Message_tips["Windows_title"],
                           Parameter.Message_tips["Change Success"], QMessageBox.Ok)

        self.reset_and_quit()
        self.setButtonEnable()

    def cancel_click(self):
        self.reset_and_quit()
        self.setButtonEnable()

    def closeEvent(self, *args, **kwargs):
        self.setButtonEnable()


class Predict(QDialog):
    def __init__(self,Main_win,*args, **kwargs):
        # super() 调用父类(超类)的一个方法。
        super().__init__(*args , **kwargs)
        self.query = QSqlQuery()
        self.Main_win = Main_win
        self.window_layout()
        self.item_layout()

    def window_layout(self):
        self.setWindowTitle(Parameter.Window_Name["Predict"])
        self.resize(Parameter.Window_Size["Width"]["Predict"], Parameter.Window_Size["Height"]["Predict"])
        # 固定窗体大小不被拉拽
        self.setFixedSize(self.width(), self.height())
        # 把窗口的问号按钮去掉
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def item_layout(self):

        # 创建垂直布局
        self.verticalLayout = QVBoxLayout()
        # 创建水平布局
        self.level_Layout1 = QHBoxLayout()
        self.level_Layout5 = QHBoxLayout()

        # 单行文本
        self.account_text = QLabel(Parameter.Text_label["Predict"]["account"])

        # 单行输入框
        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText(Parameter.Text_tips['Predict']["account"])

        # 按钮框
        self.predict_butten = QPushButton()
        self.cancel_butten = QPushButton()
        self.predict_butten.setText(Parameter.Butten_Name["Enter"])
        self.cancel_butten.setText(Parameter.Butten_Name["Cancel"])

        # 分别加入水平布局
        self.level_Layout1.addWidget(self.account_text)
        self.level_Layout1.addWidget(self.lineEdit_account)
        self.level_Layout5.addWidget(self.predict_butten)
        self.level_Layout5.addWidget(self.cancel_butten)

        # 处理按钮信号
        self.predict_butten.clicked.connect(self.predict_click)
        self.cancel_butten.clicked.connect(self.cancel_click)

        self.setLayout(self.verticalLayout)

    # 生成图表
    def general_graph(self,data_list,account):

        # 更改Graph的Y轴显示,该回调无法从其他文件获取数据只能将常量定义在函数内
        def change_data(data):
            score_space = ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30","30-35", "35-40",
                     "40-45", "45-50", "50-55", "55-60","60-65", "65-70", "70-75",
                     "75-80", "80-85", "85-90","90-95", "95-100"]
            return score_space[data]

        if self.Main_win.identity == Parameter.identity["Student"]:
            # 先清空文件夹
            if os.path.exists(Model_Parameter.Echarts_path):
                for file in os.listdir(Model_Parameter.Echarts_path):
                    os.remove(os.path.join(os.getcwd(), Model_Parameter.Echarts_path + file))

            # 先清空Echarts选择项
            self.Main_win.echarts.listwidget.clear()

        predict_data = []
        truly_data = []

        if len(data_list[0][0]) == 1:

            # 建立柱形图
            bar = Bar(Parameter.Visual_Graph["Bar_Name"], account)

            # 第一重选择模型
            for temp in data_list:
                predict_data.append(temp[0][0])
                truly_data.append(temp[1][0])

            bar.add(Parameter.Visual_Graph["Value_type"][0], Parameter.Visual_Graph["Algorithm_Name"], predict_data,
                    xaxis_name=Parameter.Visual_Graph["Columns_Name"][0],
                    yaxis_name=Parameter.Visual_Graph["Columns_Name"][1],
                    yaxis_name_gap=Parameter.Visual_Graph["Y_gap"],
                    is_more_utils=True,
                    yaxis_formatter = change_data)
            bar.add(Parameter.Visual_Graph["Value_type"][1], Parameter.Visual_Graph["Algorithm_Name"], truly_data,
                    xaxis_name=Parameter.Visual_Graph["Columns_Name"][0],
                    yaxis_name=Parameter.Visual_Graph["Columns_Name"][1],
                    yaxis_name_gap = Parameter.Visual_Graph["Y_gap"],
                    is_more_utils=True,
                    yaxis_formatter = change_data)

            bar.render(Model_Parameter.Echarts_path + account + ".html")

            #  在Echarts中建立item功能项
            item = QListWidgetItem()
            item.setText(account)
            self.Main_win.echarts.listwidget.addItem(item)

            # 展现数据图，仅一个item
            self.Main_win.echarts.Print_Graph(account)

        else:
            data_len = len(data_list[0][0])

            # 第一重选择数据mark_point
            for temp1 in range(data_len):

                # 建立柱形图
                bar = Bar(Parameter.Visual_Graph["Bar_Name"], account[temp1])

                # 第二重选择模型
                for temp2 in data_list:
                    predict_data.append(temp2[0][temp1])
                    truly_data.append(temp2[1][temp1])

                bar.add(Parameter.Visual_Graph["Value_type"][0], Parameter.Visual_Graph["Algorithm_Name"], predict_data,
                        xaxis_name=Parameter.Visual_Graph["Columns_Name"][0],
                        yaxis_name=Parameter.Visual_Graph["Columns_Name"][1],
                        yaxis_name_gap=Parameter.Visual_Graph["Y_gap"],
                        is_more_utils=True,
                        yaxis_formatter = change_data)
                bar.add(Parameter.Visual_Graph["Value_type"][1], Parameter.Visual_Graph["Algorithm_Name"], truly_data,
                        xaxis_name=Parameter.Visual_Graph["Columns_Name"][0],
                        yaxis_name=Parameter.Visual_Graph["Columns_Name"][1],
                        yaxis_name_gap=Parameter.Visual_Graph["Y_gap"],
                        is_more_utils=True,
                        yaxis_formatter = change_data)

                bar.render(Model_Parameter.Echarts_path + account[temp1] + ".html")

                # 在Echarts中建立item功能项
                item = QListWidgetItem()
                item.setText(account[temp1])
                self.Main_win.echarts.listwidget.addItem(item)

                # 清除数据重新利用list
                predict_data.clear()
                truly_data.clear()

            # 展现数据图，可含多个item
            self.Main_win.echarts.Print_Graph(account)

    def run_predict(self,account):
        msgBox = QMessageBox()
        if isinstance(account, list):
            datas = []
            for temp in account:
                sql_word = "SELECT * FROM `score_data` where 学号 ='" + temp + "' and 卷面成绩 = ''"
                # 账号密码信息判断,用exec执行sql，用next判断是否成功
                if self.query.exec_(sql_word) and self.query.next():
                    datas.append([str(self.query.value(temp), encoding="utf-8")
                         for temp in range(Parameter.Score_data_num["score_start"],
                                           Parameter.Score_data_num["variety"])])
                else:
                    sql_word = "SELECT * FROM `score_data` where 学号 ='" + temp + "'"
                    if self.query.exec_(sql_word) and self.query.next():
                        datas.append([str(self.query.value(temp), encoding="utf-8")
                                 for temp in range(Parameter.Score_data_num["score_start"],
                                                   Parameter.Score_data_num["variety"])])
                    else:
                        msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                                       Parameter.Message_tips["Search Failed"], QMessageBox.Ok)
                        self.cancel_click()

        else:
            sql_word = "SELECT * FROM `score_data` where 学号 ='" + account + "' and 卷面成绩 = ''"
            # 账号密码信息判断,用exec执行sql，用next判断是否成功
            if self.query.exec_(sql_word) and self.query.next():
                datas = ([str(self.query.value(temp), encoding="utf-8")
                              for temp in range(Parameter.Score_data_num["score_start"],
                                                Parameter.Score_data_num["variety"])])
            else:
                sql_word = "SELECT * FROM `score_data` where 学号 ='" + account + "'"
                if self.query.exec_(sql_word) and self.query.next():
                    datas = [str(self.query.value(temp), encoding="utf-8")
                                  for temp in range(Parameter.Score_data_num["score_start"],
                                                    Parameter.Score_data_num["variety"])]
                else:
                    msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                                   Parameter.Message_tips["Search Failed"], QMessageBox.Ok)
                    self.cancel_click()
                    # 不执行预测操作
                    return

        LR_result = self.Main_win.model_LR.LR_prediction(datas)
        SVM_result = self.Main_win.model_SVM.SVM_prediction(datas)
        DNN_result = self.Main_win.model_DNN.DNN_prediction(datas)

        # 生成图表
        self.general_graph([LR_result,SVM_result,DNN_result],account)

        # 设置功能区域和图形区域的标题
        self.Main_win.echarts.label_left.setText(Parameter.Visual_Graph["Graph_Name"][0])
        self.Main_win.echarts.label_right.setText(Parameter.Visual_Graph["Graph_Name"][1])

        if self.Main_win.identity == Parameter.identity["Student"]:
            self.lineEdit_account.setText("")
            self.Main_win.echarts.show()

    def predict_click(self):
        msgBox = QMessageBox()
        if self.Main_win.identity == Parameter.identity["Teacher"]:
            account = self.lineEdit_account.text()
            self.run_predict(account)
        else:
            account = self.lineEdit_account.text()
            if account and account == self.Main_win.user_id:
                self.run_predict(account)
            else:
                msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Predict Own"], QMessageBox.Ok)

                self.cancel_click()

        self.setVisible(False)

    def cancel_click(self):
        self.lineEdit_account.setText("")
        self.setVisible(False)

        # 恢复所有其他按钮
        if not self.Main_win.button1.isEnabled():
            self.Main_win.button1.setEnabled(True)
        if not self.Main_win.button2.isEnabled():
            self.Main_win.button2.setEnabled(True)
        if not self.Main_win.button4.isEnabled():
            self.Main_win.button4.setEnabled(True)

    def closeEvent(self, *args, **kwargs):

        # 恢复所有其他按钮
        if not self.Main_win.button1.isEnabled():
            self.Main_win.button1.setEnabled(True)
        if not self.Main_win.button2.isEnabled():
            self.Main_win.button2.setEnabled(True)
        if not self.Main_win.button4.isEnabled():
            self.Main_win.button4.setEnabled(True)

class Search_dialog(QDialog):
    def __init__(self,Main_win,*args, **kwargs):
        # super() 调用父类(超类)的一个方法。
        super().__init__(*args , **kwargs)
        self.query = QSqlQuery()
        self.Main_win = Main_win
        self.window_layout()
        self.item_layout()

    def window_layout(self):
        self.setWindowTitle(Parameter.Window_Name["Search"])
        self.resize(Parameter.Window_Size["Width"]["Search"], Parameter.Window_Size["Height"]["Search"])
        # 固定窗体大小不被拉拽
        self.setFixedSize(self.width(), self.height())
        # 把窗口的问号按钮去掉
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def item_layout(self):

        # 创建垂直布局
        self.verticalLayout = QVBoxLayout()
        # 创建水平布局
        self.level_Layout1 = QHBoxLayout()
        self.level_Layout2 = QHBoxLayout()

        # 单行文本
        self.account_text = QLabel(Parameter.Text_label["Search"]["account"])

        # 单行输入框
        self.lineEdit_account = QLineEdit()

        # 按钮框
        self.search_butten = QPushButton()
        self.cancel_butten = QPushButton()
        self.search_butten.setText(Parameter.Butten_Name["Search"])
        self.cancel_butten.setText(Parameter.Butten_Name["Cancel"])

        # 分别加入水平布局
        self.level_Layout1.addWidget(self.account_text)
        self.level_Layout1.addWidget(self.lineEdit_account)
        self.level_Layout2.addWidget(self.search_butten)
        self.level_Layout2.addWidget(self.cancel_butten)

        # 水平布局控件加入垂直布局
        self.verticalLayout.addLayout(self.level_Layout1)
        self.verticalLayout.addLayout(self.level_Layout2)

        # 处理按钮信号
        self.search_butten.clicked.connect(self.search_click)
        self.cancel_butten.clicked.connect(self.cancel_click)

        self.setLayout(self.verticalLayout)

    def clean_and_out(self):
        self.lineEdit_account.setText("")
        self.setVisible(False)

    def search_click(self):

        msgBox = QMessageBox()
        # 根据账号查找记录并更新查询结果
        self.Main_win.table_model.setFilter((Parameter.Search_Name + " = '%s'"%(self.lineEdit_account.text())))
        self.Main_win.table_model.select()

        sql_word = "SELECT 卷面成绩 FROM `score_data` where 学号='" + self.lineEdit_account.text() + "'"

        # 账号信息判断,由权限决定查询开关，用exec执行sql，用next判断是否成功
        if self.Main_win.identity == Parameter.identity["Teacher"] or self.Main_win.user_id == self.lineEdit_account.text():
            if self.query.exec_(sql_word) and self.query.next():
                # 查找成功
                msgBox.information(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Search Success"], QMessageBox.Ok)
                self.clean_and_out()
            else:
                #查询无结果
                msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Search Failed"], QMessageBox.Ok)
                self.clean_and_out()
        else:
            msgBox.critical(self, Parameter.Message_tips["Windows_title"],
                            Parameter.Message_tips["Search Ban"], QMessageBox.Ok)
            self.clean_and_out()

    def cancel_click(self):
        self.clean_and_out()


class Create_dialog(QDialog):
    def __init__(self, login_dialog,*args, **kwargs):
        # super() 调用父类(超类)的一个方法。
        super().__init__(*args , **kwargs)
        self.login_dialog = login_dialog
        self.window_layout()
        self.item_layout()

    def window_layout(self):
        self.setWindowTitle(Parameter.Window_Name["Create"])
        self.resize(Parameter.Window_Size["Width"]["Create"], Parameter.Window_Size["Height"]["Create"])
        # 固定窗体大小不被拉拽
        self.setFixedSize(self.width(), self.height())
        # 把窗口的问号按钮去掉
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def item_layout(self):

        # 创建垂直布局
        self.verticalLayout = QVBoxLayout()
        # 创建水平布局
        self.level_Layout1 = QHBoxLayout()
        self.level_Layout2 = QHBoxLayout()
        self.level_Layout3 = QHBoxLayout()
        self.level_Layout4 = QHBoxLayout()
        self.level_Layout5 = QHBoxLayout()

        # 单行文本
        self.account_text = QLabel(Parameter.Text_label["Create"]["account"])
        self.password_text = QLabel(Parameter.Text_label["Create"]["password"])
        self.name_text = QLabel(Parameter.Text_label["Create"]["name"])
        self.identity_text = QLabel(Parameter.Text_label["Create"]["identity"])

        # 单行输入框
        self.lineEdit_account = QLineEdit()
        self.lineEdit_password = QLineEdit()
        self.lineEdit_name = QLineEdit()
        self.lineEdit_account.setPlaceholderText(Parameter.Text_tips["Create"]["account"])
        self.lineEdit_password.setPlaceholderText(Parameter.Text_tips["Create"]["password"])
        self.lineEdit_name.setPlaceholderText(Parameter.Text_tips["Create"]["name"])

        # 下拉选择框
        self.choose_identity = QComboBox()
        # 将身份选择添加到下拉框
        for temp in Parameter.identity:
            self.choose_identity.addItem(Parameter.identity[temp])

        # 按钮框
        self.create_butten = QPushButton()
        self.cancel_butten = QPushButton()
        self.create_butten.setText(Parameter.Butten_Name["Create"])
        self.cancel_butten.setText(Parameter.Butten_Name["Cancel"])

        # 分别加入水平布局
        self.level_Layout1.addWidget(self.account_text)
        self.level_Layout1.addWidget(self.lineEdit_account)
        self.level_Layout2.addWidget(self.password_text)
        self.level_Layout2.addWidget(self.lineEdit_password)
        self.level_Layout3.addWidget(self.name_text)
        self.level_Layout3.addWidget(self.lineEdit_name)
        self.level_Layout4.addWidget(self.identity_text)
        self.level_Layout4.addWidget(self.choose_identity)
        self.level_Layout5.addWidget(self.create_butten)
        self.level_Layout5.addWidget(self.cancel_butten)

        # 水平布局控件加入垂直布局
        self.verticalLayout.addLayout(self.level_Layout1)
        self.verticalLayout.addLayout(self.level_Layout2)
        self.verticalLayout.addLayout(self.level_Layout3)
        self.verticalLayout.addLayout(self.level_Layout4)
        self.verticalLayout.addLayout(self.level_Layout5)

        # 处理按钮信号
        self.create_butten.clicked.connect(self.create_click)
        self.cancel_butten.clicked.connect(self.create_quit)

        self.setLayout(self.verticalLayout)

    def clean_text(self):
        self.lineEdit_account.setText("")
        self.lineEdit_password.setText("")
        self.lineEdit_name.setText("")

    def create_quit(self):
        self.login_dialog.setVisible(True)
        self.setVisible(False)

    def create_click(self):
        msgBox = QMessageBox()

        if self.lineEdit_account.text():
            if self.lineEdit_password.text():
                if self.lineEdit_name.text():
                    # 建立SQL语句
                    query = QSqlQuery()
                    sql_word = "SELECT account FROM `user` where account='"+self.lineEdit_account.text()+"'"
                    # 账号密码信息判断,用exec执行sql，用next判断是否成功
                    if query.exec_(sql_word) and query.next():
                        # 账号已存在
                        self.clean_text()
                        msgBox.warning(self,Parameter.Message_tips["Windows_title"],
                                       Parameter.Message_tips["Account_exists"],QMessageBox.Ok)

                    else:
                        # 注册成功
                        sql_word = "INSERT INTO `user`(`account`, `password`, `name`, `identity`) VALUES ('{0}', '{1}', '{2}', '{3}')".format(
                            self.lineEdit_account.text(),self.lineEdit_password.text(),self.lineEdit_name.text(),self.choose_identity.currentText()
                        )
                        query.exec_(sql_word)

                        msgBox.information(self, Parameter.Message_tips["Windows_title"],
                                        Parameter.Message_tips["Create_Success"], QMessageBox.Yes)

                        self.clean_text()
                        self.login_dialog.setVisible(True)
                        self.setVisible(False)
                else:
                    # 姓名未输入
                    self.clean_text()
                    msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                                   Parameter.Message_tips["Name_missing"], QMessageBox.Ok)
            else:
                # 密码未输入
                self.clean_text()
                msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Password_missing"], QMessageBox.Ok)

        else:
            # 账号未输入
            self.clean_text()
            msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                           Parameter.Message_tips["Account_missing"], QMessageBox.Ok)


# 登录框
class Login_dialog(QDialog):

    login_sendmsg = pyqtSignal(str)

    # *args是非关键字参数，用于元组，**kwargs是关键字参数 （字典）
    def __init__(self, *args, **kwargs):
        # super() 调用父类(超类)的一个方法。
        super().__init__(*args , **kwargs)
        # 注册界面
        self.create_view = Create_dialog(self)
        self.window_layout()
        self.item_layout()

    def window_layout(self):
        self.setWindowTitle(Parameter.Window_Name["Login"])
        self.resize(Parameter.Window_Size["Width"]["Login"], Parameter.Window_Size["Height"]["Login"])
        # 固定窗体大小不被拉拽
        self.setFixedSize(self.width(), self.height())
        # 把窗口的问号按钮去掉
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def item_layout(self):

        # 创建垂直布局
        self.verticalLayout = QVBoxLayout()
        # 创建水平布局
        self.level_Layout1 = QHBoxLayout()
        self.level_Layout2 = QHBoxLayout()
        self.level_Layout3 = QHBoxLayout()

        # 单行文本
        self.account_text = QLabel(Parameter.Text_label["Login"]["account"])
        self.password_text = QLabel(Parameter.Text_label["Login"]["password"])

        # 单行输入框
        self.lineEdit_account = QLineEdit()
        self.lineEdit_password = QLineEdit()
        self.lineEdit_account.setPlaceholderText(Parameter.Text_tips["Login"]["account"])
        self.lineEdit_password.setPlaceholderText(Parameter.Text_tips["Login"]["password"])

        #按钮框
        self.enter_butten = QPushButton()
        self.cancel_butten = QPushButton()
        self.create_butten = QPushButton()
        self.enter_butten.setText(Parameter.Butten_Name["Enter"])
        self.cancel_butten.setText(Parameter.Butten_Name["Cancel"])
        self.create_butten.setText(Parameter.Butten_Name["Create"])

        # 分别加入水平布局
        self.level_Layout1.addWidget(self.account_text)
        self.level_Layout1.addWidget(self.lineEdit_account)
        self.level_Layout2.addWidget(self.password_text)
        self.level_Layout2.addWidget(self.lineEdit_password)
        self.level_Layout3.addWidget(self.enter_butten)
        self.level_Layout3.addWidget(self.cancel_butten)
        self.level_Layout3.addWidget(self.create_butten)
        # 水平布局控件加入垂直布局
        self.verticalLayout.addLayout(self.level_Layout1)
        self.verticalLayout.addLayout(self.level_Layout2)
        self.verticalLayout.addLayout(self.level_Layout3)

        # 处理按钮信号
        self.enter_butten.clicked.connect(self.entet_click)
        self.cancel_butten.clicked.connect(self.clean_click)
        self.create_butten.clicked.connect(self.create_click)

        self.setLayout(self.verticalLayout)

    def entet_click(self):
        # 创建提示框
        msgBox = QMessageBox()

        # 建立SQL语句
        query = QSqlQuery()
        sql_word = "SELECT account FROM `user` where account='"+self.lineEdit_account.text()+\
                   "' and password='"+self.lineEdit_password.text()+"'"

        # 账号密码信息判断,用exec执行sql，用next判断是否成功
        if query.exec_(sql_word) and query.next():

            # 传递用户身份
            self.login_sendmsg.emit(str(query.value(0), encoding="utf-8"))
            # 把登录界面隐藏
            self.setVisible(False)

        else:
            msgBox.critical(self.enter_butten, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Input Error"], QMessageBox.Ok)

            self.clean_click()

    def clean_click(self):
        self.lineEdit_account.setText("")
        self.lineEdit_password.setText("")

    def create_click(self):
        # 先将登录界面隐藏
        self.setVisible(False)
        self.create_view.show()

        # 清空输入框
        self.clean_click()


class Echarts(QDialog):
    # *args是非关键字参数，用于元组，**kwargs是关键字参数 （字典）
    def __init__(self,Main_win,*args, **kwargs):
        # super() 调用父类(超类)的一个方法。
        super().__init__(*args , **kwargs)
        self.Main_win = Main_win
        # 默认未进行计算图操作
        self.is_Calculate = False
        # 数据项集合
        self.Calcul_data_lsit = []
        self.window_layout()
        self.item_layout()

    def window_layout(self):
        self.setWindowTitle(Parameter.Window_Name["Echarts"])
        self.resize(Parameter.Window_Size["Width"]["Echarts"], Parameter.Window_Size["Height"]["Echarts"])
        # 可拖拽大小
        self.setSizeGripEnabled(True)
        # 把窗口的问号按钮去掉
        self.setWindowFlags(Qt.WindowCloseButtonHint)

    def item_layout(self):

        # 创建基本控件基类
        self.frame = QFrame(self)
        # 绘制矩形面板
        self.frame.setFrameShape(QFrame.StyledPanel)
        # 3D凸起线
        self.frame.setFrameShadow(QFrame.Raised)

        # 建立水平布局，填充主窗口
        self.level_Layout = QHBoxLayout(self)
        # 设置左侧、顶部、右侧和底部边距
        self.level_Layout.setContentsMargins(Parameter.Visual_Graph["ContentsMargins"][0],
                                             Parameter.Visual_Graph["ContentsMargins"][1],
                                             Parameter.Visual_Graph["ContentsMargins"][2],
                                             Parameter.Visual_Graph["ContentsMargins"][3])
        # 各个控件之间的上下间距
        self.level_Layout.setSpacing(0)

        # 网格布局管理器
        self.gridLayout = QGridLayout(self.frame)

        # 多页面切换
        self.stackedWidget = QStackedWidget(self.frame)
        # 围绕内容画框
        self.stackedWidget.setFrameShape(QFrame.Box)

        # 分别设置行，列，占用行数，占用列数
        self.gridLayout.addWidget(self.stackedWidget, Parameter.Visual_Graph["StackedWidget"][0],
                                  Parameter.Visual_Graph["StackedWidget"][1],
                                  Parameter.Visual_Graph["StackedWidget"][2],
                                  Parameter.Visual_Graph["StackedWidget"][3])

        # 加载并显示多个列表项
        self.listwidget = QListWidget(self.frame)
        self.listwidget.setMaximumSize(QSize(Parameter.Visual_Graph["Listwidget_size"]["Width"],
                                             Parameter.Visual_Graph["Listwidget_size"]["Height"]))

        # 分别设置行，列，占用行数，占用列数
        self.gridLayout.addWidget(self.listwidget, Parameter.Visual_Graph["Listwidget"][0],
                                  Parameter.Visual_Graph["Listwidget"][1],
                                  Parameter.Visual_Graph["Listwidget"][2],
                                  Parameter.Visual_Graph["Listwidget"][3])

        self.line = QFrame(self.frame)
        # 无框架垂直线作为分隔符
        self.line.setFrameShape(QFrame.VLine)
        # 3D凹陷线
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        # 分别设置行，列，占用行数，占用列数
        self.gridLayout.addWidget(self.line, Parameter.Visual_Graph["Line"][0],
                                  Parameter.Visual_Graph["Line"][1],
                                  Parameter.Visual_Graph["Line"][2],
                                  Parameter.Visual_Graph["Line"][3])

        # 左侧功能列表的标题
        self.label_left = QLabel(self.frame)
        # 右侧功能列表的标题
        self.label_right = QLabel(self.frame)

        # 建立文字属性控件
        font = QtGui.QFont()
        # 文字大小
        font.setPointSize(Parameter.Visual_Graph["Word"]["Size"])
        # 设置粗体
        font.setBold(Parameter.Visual_Graph["Word"]["Bold"])
        # 禁用斜体
        font.setItalic(Parameter.Visual_Graph["Word"]["Italic"])
        font.setWeight(Parameter.Visual_Graph["Word"]["Weight"])

        # 设置好的文字格式添加到控件中
        self.label_left.setFont(font)
        self.label_right.setFont(font)

        # 分别设置行，列，占用行数，占用列数
        self.gridLayout.addWidget(self.label_left, Parameter.Visual_Graph["Label_left"][0],
                                  Parameter.Visual_Graph["Label_left"][1],
                                  Parameter.Visual_Graph["Label_left"][2],
                                  Parameter.Visual_Graph["Label_left"][3], QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.label_right, Parameter.Visual_Graph["Label_right"][0],
                                  Parameter.Visual_Graph["Label_right"][1],
                                  Parameter.Visual_Graph["Label_right"][2],
                                  Parameter.Visual_Graph["Label_right"][3], QtCore.Qt.AlignHCenter)

        # 基类布局放入水平布局
        self.level_Layout.addWidget(self.frame)

        # 网格布局居中显示
        self.setLayout(self.gridLayout)

    def calculate_graph(self):

        # 先清空文件夹
        if os.path.exists(Model_Parameter.Echarts_path):
            for file in os.listdir(Model_Parameter.Echarts_path):
                os.remove(os.path.join(os.getcwd(), Model_Parameter.Echarts_path + file))

        # 先清空Echarts选择项
        self.listwidget.clear()

        # 已计算的图不必再次计算
        if not self.is_Calculate:
            self.is_Calculate = True

            # 数据项
            datas = []

            # 实现饼图计算构建
            self.Main_win.query.exec_(Parameter.Sql_word["Score_calculate"][0]+"'"+self.Main_win.user_id+"'")
            while self.Main_win.query.next():
                datas.append([ 0. if str(self.Main_win.query.value(temp), encoding="utf-8") == "" else
                               float(str(self.Main_win.query.value(temp), encoding="utf-8"))
                               for temp in range(Parameter.Score_data_num["Score_calculate"][0])])

            self.Calcul_data_lsit.append(datas[0])
            datas = []

            # 实现折线图计算构建
            # 先进行全库数据的收集
            self.Main_win.query.exec_(Parameter.Sql_word["Score_calculate"][1])
            while self.Main_win.query.next():
                datas.append([0. if str(self.Main_win.query.value(temp), encoding="utf-8") == "" else
                              float(str(self.Main_win.query.value(temp), encoding="utf-8"))
                              for temp in range(Parameter.Score_data_num["Score_calculate"][1])])

            max_data = []
            min_data = []

            for temp in range(len(datas[0])):
                data_temp = sorted(datas, key=lambda a: a[temp])
                max_data.append(data_temp[len(datas) - 1][temp])
                min_data.append(data_temp[0][temp])

            datas = []

            # 接着进行本用户的数据定位
            self.Main_win.query.exec_(Parameter.Sql_word["Score_calculate"][3] + "'" + self.Main_win.user_id + "'")
            while self.Main_win.query.next():
                datas.append([0. if str(self.Main_win.query.value(temp), encoding="utf-8") == "" else
                              float(str(self.Main_win.query.value(temp), encoding="utf-8"))
                              for temp in range(Parameter.Score_data_num["Score_calculate"][1])])

            self.Calcul_data_lsit.append([datas[0],min_data,max_data])

            datas = []

            # 实现雷达图计算构建
            self.Main_win.query.exec_(Parameter.Sql_word["Score_calculate"][2] + "'" + self.Main_win.user_id + "'")
            while self.Main_win.query.next():
                # 课堂成绩存在等级和分数的转换
                for temp in range(Parameter.Score_data_num["Score_calculate"][2]):
                    string_temp = str(self.Main_win.query.value(temp), encoding="utf-8")
                    if string_temp == "":
                        datas.append(0.)
                    else:
                        if temp == Data_change.Score_dict["index"]:
                            datas.append(float(Data_change.Score_dict[string_temp]))
                        else:
                            datas.append(float(string_temp))

            self.Calcul_data_lsit.append([datas])

            # 保存饼图每块的名称
            self.pie_item_name = []
            for temp in range(Parameter.Visual_Graph["Func_data_name"][0][0],Parameter.Visual_Graph["Func_data_name"][0][1]):
                self.pie_item_name.append(Parameter.Tablefield_Name[temp])

            # 保存折线图坐标轴值的名称
            self.line_item_name = []
            for temp in range(Parameter.Visual_Graph["Func_data_name"][1][0],
                              Parameter.Visual_Graph["Func_data_name"][1][1]):
                self.line_item_name.append(Parameter.Tablefield_Name[temp])

            # 保存雷达图各维度的名称
            self.radar_item_name = []
            for temp in range(Parameter.Visual_Graph["Func_data_name"][2][0],
                              Parameter.Visual_Graph["Func_data_name"][2][1]):
                self.radar_item_name.append(
                    {
                        "name":Parameter.Tablefield_Name[temp],
                        "max":Parameter.Visual_Graph["Radar_space"][1],
                        "min":Parameter.Visual_Graph["Radar_space"][0]
                    }
                )


        # 构造饼图
        pie = Pie(Parameter.Visual_Graph["Func_name"][0],self.Main_win.user_id)
        pie.add(self.Main_win.user_id,self.pie_item_name,self.Calcul_data_lsit[0],
                is_label_show=True,
                is_more_utils=True
        )
        pie.render(path=Model_Parameter.Echarts_path + Parameter.Visual_Graph["Func_name"][0] + ".html")

        # 构造折线图
        line = Line(Parameter.Visual_Graph["Func_name"][1],self.Main_win.user_id)
        line.add(Parameter.Visual_Graph["Line_name"][0], self.line_item_name, self.Calcul_data_lsit[1][0],
                 xaxis_rotate=Parameter.Visual_Graph["Line_x_rotate"],
                 is_label_show=True)
        line.add(Parameter.Visual_Graph["Line_name"][1], self.line_item_name, self.Calcul_data_lsit[1][1],
                 xaxis_rotate=Parameter.Visual_Graph["Line_x_rotate"],
                 is_label_show=True)
        line.add(Parameter.Visual_Graph["Line_name"][2], self.line_item_name, self.Calcul_data_lsit[1][2],
                 xaxis_rotate=Parameter.Visual_Graph["Line_x_rotate"],
                 is_label_show=True)
        line.render(path=Model_Parameter.Echarts_path + Parameter.Visual_Graph["Func_name"][1] + ".html")

        # 构造雷达图
        radar = Radar(Parameter.Visual_Graph["Func_name"][1], self.Main_win.user_id)
        radar.config(c_schema=self.radar_item_name)
        radar.add(Parameter.Visual_Graph["Radar_name"], self.Calcul_data_lsit[2])

        radar.render(path=Model_Parameter.Echarts_path + Parameter.Visual_Graph["Func_name"][2] + ".html")

        #  在Echarts中建立item功能项
        item = QListWidgetItem()
        item.setText(Parameter.Visual_Graph["Student_func"][0])
        self.listwidget.addItem(item)
        item = QListWidgetItem()
        item.setText(Parameter.Visual_Graph["Student_func"][1])
        self.listwidget.addItem(item)
        item = QListWidgetItem()
        item.setText(Parameter.Visual_Graph["Student_func"][2])
        self.listwidget.addItem(item)

        # 展现数据图
        self.Print_Graph([Parameter.Visual_Graph["Func_name"][0],Parameter.Visual_Graph["Func_name"][1],Parameter.Visual_Graph["Func_name"][2]])

    def Print_Graph(self,func):

        # 用来收集和删除Widget
        self.Widget_list = []
        # 变为集合
        if not isinstance(func,list):
            func = [func]

        for item in func:
            page = QWidget()
            level_layout = QHBoxLayout(page)
            frame = QFrame(page)
            frame.setFrameShape(QFrame.StyledPanel)
            frame.setFrameShadow(QFrame.Raised)
            level_layout.addWidget(frame)

            # 每添加一个就记录，关闭窗口后全部删除
            self.stackedWidget.addWidget(page)
            self.Widget_list.append(page)

            browser = QWebEngineView()
            browser.load(QUrl("file:///" +r"/".join(os.getcwd().split("\\"))+"/"+Model_Parameter.Echarts_path+item+".html"))
            verticalLayout = QHBoxLayout(frame)
            verticalLayout.addWidget(browser)

        self.listwidget.currentRowChanged.connect(self.stackedWidget.setCurrentIndex)

    def closeEvent(self, *args, **kwargs):
        # 关闭窗口后清空所有切换项
        for widget_temp in self.Widget_list:
            self.stackedWidget.removeWidget(widget_temp)

        # 关闭窗口时清空选项
        self.listwidget.clear()

        # 关闭窗口时清空文件夹
        if os.path.exists(Model_Parameter.Echarts_path):
            for file in os.listdir(Model_Parameter.Echarts_path):
                os.remove(os.path.join(os.getcwd(), Model_Parameter.Echarts_path + file))

        # 恢复所有其他按钮
        if not self.Main_win.button1.isEnabled():
            self.Main_win.button1.setEnabled(True)
        if not self.Main_win.button2.isEnabled():
            self.Main_win.button2.setEnabled(True)
        if not self.Main_win.button4.isEnabled():
            self.Main_win.button4.setEnabled(True)

def Clear_Echarts():
    # # 程序有可能遭受非正常关闭，运行前清空先前生成的图表
    if os.path.exists(Model_Parameter.Echarts_path):
        for file in os.listdir(Model_Parameter.Echarts_path):
            os.remove(os.path.join(os.getcwd(), Model_Parameter.Echarts_path + file))


if __name__ == "__main__":

    Clear_Echarts()
    # 运行主循环
    app = QApplication(sys.argv)
    main_window = MainWindow()
    # 退出应用程序并返回app.exec_()到父进程
    sys.exit(app.exec_())




