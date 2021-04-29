from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from dowload import *
from PyQt5.QtWidgets import *
class dowload_mainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(dowload_mainWindow,self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)

    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.setWindowModality(QtCore.Qt.WindowModal)
        mainWindow.resize(500,600)

        self.centralWidget = QtWidgets.QWidget(mainWindow)
        self.centralWidget.setObjectName("centralWidget")

        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(50, 20, 100, 20))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(50, 50, 100, 20))
        self.lineEdit_2.setText("")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(50, 80, 100, 20))
        self.lineEdit_3.setText("")
        self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 24, 24, 12))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 54, 24, 12))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(10, 84, 24, 12))
        self.label_3.setObjectName("label_3")


        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(190, 104, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(290, 104, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")


        mainWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "视频下载神器"))

        self.lineEdit.setPlaceholderText(_translate("MainWindow", "请输入qq帐号"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "请输入qq密码"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "请输入视频地址"))
        self.label.setText(_translate("MainWindow", "帐号"))
        self.label_2.setText(_translate("MainWindow", "密码"))
        self.label_3.setText(_translate("MainWindow", "地址"))

        self.pushButton.setText(_translate("MainWindow", "开始下载"))
        self.pushButton_2.setText(_translate("MainWindow", "取消"))


    def word_get(self):
        login_user = self.lineEdit.text()
        login_password = self.lineEdit_2.text()
        # login_url = self.lineEdit_3.text()
        print(login_user,login_password)
        # if login_user == 'admin' and login_password == '123456':
        #     print()
        # else:
        #     QMessageBox.warning(self,
        #             "警告",
        #             "用户名或密码错误！",
        #             QMessageBox.Yes)
        #     self.lineEdit.setFocus()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = dowload_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())



