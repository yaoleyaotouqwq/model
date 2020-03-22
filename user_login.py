import sys

from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from qtpy import QtCore

import GUI_Parameter as Parameter

# 主窗口
class MainWindow(QMainWindow):
    # *args是非关键字参数，用于元组，**kwargs是关键字参数 （字典）
    def __init__(self , *args , **kwargs):
        # super() 调用父类(超类)的一个方法。
        super().__init__(*args , **kwargs)

        self.db = self.connect_Db()
        self.query = QSqlQuery()
        # 数据表视图
        self.table_model = QSqlTableModel()
        self.mainwindow_layout()

        self.dialog = Login_dialog()
        self.dialog.show()
        # 先将主界面隐藏
        # self.setVisible(False)

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
        # 仅可读数据表
        self.table_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.table_model.select()
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

    def get_slot(self,user_id):
        self.user_id = user_id
        # 显示主界面
        self.setVisible(True)
        self.choose_client()

    def choose_client(self):
        sql_word = "SELECT identity FROM `user` where account='" + self.user_id + "'"
        # 账号密码信息判断,用exec执行sql，用next判断是否成功
        if self.query.exec_(sql_word) and self.query.next():
            print("Welcome to my system.")
            # 传递用户身份
            user_id = str(self.query.value(0), encoding="utf=8")
            # 设置欢迎词
            self.label1.setText(user_id + "专用")
            self.label2.setText("欢迎用户："+self.user_id)

            if user_id == Parameter.identity["Student"]:
                self.Student_client()
            elif user_id == Parameter.identity["Teacher"]:
                self.Techer_client()
            else:
                self.Administrator_client()
        else:
            print("Error! the User not normal identity.")


    def Student_client(self):
        self.table_model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        print("this is Student Client.")


    def Techer_client(self):
        # 可修改数据表
        self.table_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        print("this is Teacher Client.")

    def Administrator_client(self):
        # 仅可读数据表
        self.table_model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        print("this is Administrator Client.")


# 对话框
class Login_dialog(QDialog):

    login_sendmsg = pyqtSignal(str)

    # *args是非关键字参数，用于元组，**kwargs是关键字参数 （字典）
    def __init__(self, *args, **kwargs):
        # super() 调用父类(超类)的一个方法。
        super().__init__(*args , **kwargs)

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
        # 创建基类控件
        self.frame = QFrame(self)
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
        self.enter_butten.setText(Parameter.Butten_Name["Enter"])
        self.cancel_butten.setText(Parameter.Butten_Name["Cancel"])

        # 分别加入水平布局
        self.level_Layout1.addWidget(self.account_text)
        self.level_Layout1.addWidget(self.lineEdit_account)
        self.level_Layout2.addWidget(self.password_text)
        self.level_Layout2.addWidget(self.lineEdit_password)
        self.level_Layout3.addWidget(self.enter_butten)
        self.level_Layout3.addWidget(self.cancel_butten)
        # 水平布局控件加入垂直布局
        self.verticalLayout.addLayout(self.level_Layout1)
        self.verticalLayout.addLayout(self.level_Layout2)
        self.verticalLayout.addLayout(self.level_Layout3)

        # 处理按钮信号
        self.enter_butten.clicked.connect(self.entet_click)
        self.cancel_butten.clicked.connect(QCoreApplication.instance().quit)

        self.setLayout(self.verticalLayout)

    def entet_click(self):
        # 建立SQL语句
        query = QSqlQuery()
        sql_word = "SELECT account FROM `user` where account='"+self.lineEdit_account.text()+\
                   "' and password='"+self.lineEdit_password.text()+"'"
        # 账号密码信息判断,用exec执行sql，用next判断是否成功
        if query.exec_(sql_word) and query.next():
            # 传递用户身份
            self.login_sendmsg.emit(str(query.value(0), encoding="utf=8"))
            # 把登录界面隐藏
            self.setVisible(False)
            return
        else:
            print("No this account or password error!")


if __name__ == "__main__":
    # 运行主循环
    app = QApplication(sys.argv)
    main_window = MainWindow()
    # 退出应用程序并返回app.exec_()到父进程
    sys.exit(app.exec_())




