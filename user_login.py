import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import GUI_Parameter as Parameter

# 主窗口
class MainWindow(QMainWindow):
    # *args是非关键字参数，用于元组，**kwargs是关键字参数 （字典）
    def __init__(self , *args , **kwargs):
        # super() 调用父类(超类)的一个方法。
        super().__init__(*args , **kwargs)
        self.setWindowTitle(Parameter.Window_Name["Login"])
        self.mainwindow_layout()

    def mainwindow_layout(self):
        self.setWindowTitle(Parameter.Window_Name["Main"])
        self.resize(Parameter.Window_Size["Width"]["Main"], Parameter.Window_Size["Height"]["Main"])

        # 把窗口的问号按钮去掉
        self.setWindowFlags(Qt.WindowCloseButtonHint)

# 对话框
class Login_dialog(QDialog):
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
        self.level_Layout = QHBoxLayout()

        # 单行输入框
        self.lineEdit_account = QLineEdit()
        self.lineEdit_password = QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入账号..")
        self.lineEdit_password.setPlaceholderText("请输入密码..")

        #按钮框
        self.enter_butten = QPushButton()
        self.cancel_butten = QPushButton()
        self.enter_butten.setText(Parameter.Butten_Name["Enter"])
        self.cancel_butten.setText(Parameter.Butten_Name["Cancel"])

        # 将各类框加入垂直布局
        self.verticalLayout.addWidget(self.lineEdit_account)
        self.verticalLayout.addWidget(self.lineEdit_password)
        # 先将按钮加入水平布局再将水平布局控件加入垂直布局
        self.level_Layout.addWidget(self.enter_butten)
        self.level_Layout.addWidget(self.cancel_butten)
        self.verticalLayout.addLayout(self.level_Layout)

        # 处理按钮信号
        self.enter_butten.clicked.connect(self.entet_click)
        self.cancel_butten.clicked.connect(QCoreApplication.instance().quit)

        self.setLayout(self.verticalLayout)

    def entet_click(self):
        # 账号信息判断
        if self.lineEdit_account.text() == "":
            # 密码信息判断
            if self.lineEdit_password.text() == "":
                self.accept()
                return


if __name__ == "__main__":
    # 运行主循环
    app = QApplication(sys.argv)
    dialog = Login_dialog()
    if dialog.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        # 退出应用程序并返回app.exec_()到父进程
        sys.exit(app.exec_())
