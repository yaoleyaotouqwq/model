import pickle
import sys

from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from qtpy import QtCore

import GUI_Parameter as Parameter

import path_define as Model_Parameter

import Model


# 主窗口
class MainWindow(QMainWindow):
    # *args是非关键字参数，用于元组，**kwargs是关键字参数 （字典）
    def __init__(self , *args , **kwargs):
        # super() 调用父类(超类)的一个方法。
        super().__init__(*args , **kwargs)

        self.model_LR = Model.logistics_regression()

        self.db = self.connect_Db()
        self.query = QSqlQuery()
        # 数据表视图
        self.table_model = QSqlTableModel()
        self.mainwindow_layout()

        # 个人信息界面
        self.infor = Information(self)
        # 预测界面
        self.predict = Predict(self)
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

    def closeEvent(self, *args, **kwargs):
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

    def information(self):
        self.infor.account_text.setText(Parameter.Text_label["Infor"]["account"] + self.user_id)
        self.infor.identity_text.setText(Parameter.Text_label["Infor"]["identity"] + self.identity)
        self.infor.lineEdit_name.setText(self.name)
        self.infor.show()

    def func1(self):
        if self.identity == Parameter.identity["Teacher"]:
            self.predict.verticalLayout.addLayout(self.predict.level_Layout2)
            self.predict.verticalLayout.addLayout(self.predict.level_Layout3)
            self.predict.verticalLayout.addLayout(self.predict.level_Layout4)
            self.predict.verticalLayout.addLayout(self.predict.level_Layout5)
            self.predict.show()

        elif self.identity == Parameter.identity["Student"]:
            self.predict.verticalLayout.addLayout(self.predict.level_Layout1)
            self.predict.verticalLayout.addLayout(self.predict.level_Layout5)
            self.predict.lineEdit_account.setText(self.user_id)
            self.predict.show()
        else:
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

            with open(Model_Parameter.id_path, 'wb') as f:
                pickle.dump(int(id), f)

            if len(datas) >= Model_Parameter.Batch_size['logistics_regression']:
                with open(Model_Parameter.id_path, 'wb') as f:
                    pickle.dump(int(id), f)

                self.model_LR.logistics_regression_train(Model_Parameter.Model_mode[0], datas)
                msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Train finish"], QMessageBox.Ok)
            else:
                msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Data Missing"], QMessageBox.Ok)

    def func2(self):
        if self.identity == Parameter.identity["Teacher"]:
            self.search_dialog.show()
        elif self.identity == Parameter.identity["Student"]:
            self.search_dialog.lineEdit_account.setText(self.user_id)
            self.search_dialog.show()
        else:
            msgBox = QMessageBox()
            datas = []
            f = open(Model_Parameter.id_path, 'rb')
            id = pickle.load(f)

            sql_word = "SELECT * FROM `score_data` where 序号 > '" + str(id) + "'"
            if self.query.exec_(sql_word):
                while self.query.next():
                    datas.append([str(self.query.value(temp), encoding="utf-8")
                                  for temp in range(Parameter.Score_data_num["score_start"],
                                                    Parameter.Score_data_num["variety"])])
                    id = self.query.value(0)

                if len(datas) >= Model_Parameter.Batch_size['logistics_regression']:
                    with open(Model_Parameter.id_path, 'wb') as f:
                        pickle.dump(int(id), f)

                    self.model_LR.logistics_regression_train(Model_Parameter.Model_mode[1], datas)
                    msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                                   Parameter.Message_tips["Train finish"], QMessageBox.Ok)
                else:
                    msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                                   Parameter.Message_tips["Train Failed"], QMessageBox.Ok)
            else:
                msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Train Failed"], QMessageBox.Ok)

    def func3(self):
        if self.identity == Parameter.identity["Teacher"]:
            self.table_model.setTable('score_data')
            self.table_model.select()
        elif self.identity == Parameter.identity["Student"]:
            pass
        else:
            pass

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

    def cancel_click(self):
        self.reset_and_quit()


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
        self.level_Layout2 = QHBoxLayout()
        self.level_Layout3 = QHBoxLayout()
        self.level_Layout4 = QHBoxLayout()
        self.level_Layout5 = QHBoxLayout()

        # 单行文本
        self.account_text = QLabel(Parameter.Text_label["Predict"]["account"])
        self.account_text1 = QLabel(Parameter.Text_label["Predict"]["account1"])
        self.account_text2 = QLabel(Parameter.Text_label["Predict"]["account2"])
        self.account_text3 = QLabel(Parameter.Text_label["Predict"]["account3"])

        # 单行输入框
        self.lineEdit_account = QLineEdit()
        self.lineEdit_account1 = QLineEdit()
        self.lineEdit_account2 = QLineEdit()
        self.lineEdit_account3 = QLineEdit()
        self.lineEdit_account.setPlaceholderText(Parameter.Text_tips['Predict']["account"])
        self.lineEdit_account1.setPlaceholderText(Parameter.Text_tips['Predict']["account"])
        self.lineEdit_account2.setPlaceholderText(Parameter.Text_tips['Predict']["account"])
        self.lineEdit_account3.setPlaceholderText(Parameter.Text_tips['Predict']["account"])

        # 按钮框
        self.predict_butten = QPushButton()
        self.cancel_butten = QPushButton()
        self.predict_butten.setText(Parameter.Butten_Name["Enter"])
        self.cancel_butten.setText(Parameter.Butten_Name["Cancel"])

        # 分别加入水平布局
        self.level_Layout1.addWidget(self.account_text)
        self.level_Layout1.addWidget(self.lineEdit_account)
        self.level_Layout2.addWidget(self.account_text1)
        self.level_Layout2.addWidget(self.lineEdit_account1)
        self.level_Layout3.addWidget(self.account_text2)
        self.level_Layout3.addWidget(self.lineEdit_account2)
        self.level_Layout4.addWidget(self.account_text3)
        self.level_Layout4.addWidget(self.lineEdit_account3)
        self.level_Layout5.addWidget(self.predict_butten)
        self.level_Layout5.addWidget(self.cancel_butten)

        # 处理按钮信号
        self.predict_butten.clicked.connect(self.predict_click)
        self.cancel_butten.clicked.connect(self.cancel_click)

        self.setLayout(self.verticalLayout)

    def run_predict(self,account):

        msgBox = QMessageBox()
        sql_word = "SELECT * FROM `score_data` where 学号 ='" + account + "' and 卷面成绩 = ''"
        # 账号密码信息判断,用exec执行sql，用next判断是否成功
        if self.query.exec_(sql_word) and self.query.next():

            datas = [str(self.query.value(temp), encoding="utf-8")
                     for temp in range(Parameter.Score_data_num["score_start"],
                                       Parameter.Score_data_num["variety"])]

            self.Main_win.model_LR.logistics_regression_prediction(datas)
            self.lineEdit_account.setText("")
        else:
            sql_word = "SELECT * FROM `score_data` where 学号 ='" + account + "'"
            if self.query.exec_(sql_word) and self.query.next():
                datas = [str(self.query.value(temp), encoding="utf-8")
                         for temp in range(Parameter.Score_data_num["score_start"],
                                           Parameter.Score_data_num["variety"])]

                self.Main_win.model_LR.logistics_regression_prediction(datas)
                self.lineEdit_account.setText("")
            else:
                msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Search Failed"], QMessageBox.Ok)
                self.lineEdit_account.setText("")
                return False

        return True

    def predict_click(self):
        msgBox = QMessageBox()
        if self.Main_win.identity == Parameter.identity["Teacher"]:
            account1 = self.lineEdit_account1.text()
            account2 = self.lineEdit_account2.text()
            account3 = self.lineEdit_account3.text()
            if account1 and account2 and account3:
                if self.run_predict(account1):
                    if self.run_predict(account2):
                        self.run_predict(account3)
            else:
                msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Predict Own"], QMessageBox.Ok)
        else:
            account = self.lineEdit_account.text()
            if account and account == self.Main_win.user_id:
                self.run_predict(account)
            else:
                msgBox.warning(self, Parameter.Message_tips["Windows_title"],
                               Parameter.Message_tips["Predict Own"], QMessageBox.Ok)

        self.setVisible(False)

    def cancel_click(self):
        self.lineEdit_account.setText("")
        self.setVisible(False)


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


if __name__ == "__main__":
    # 运行主循环
    app = QApplication(sys.argv)
    main_window = MainWindow()
    # 退出应用程序并返回app.exec_()到父进程
    sys.exit(app.exec_())




