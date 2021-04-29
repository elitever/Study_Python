from PyQt5.QtWidgets import *
import sys,math
# 1、绝对布局方式
# https://www.cnblogs.com/Yanjy-OnlyOne/p/12308069.html
class absolutelayout(QWidget):
    def __init__(self):
        super(absolutelayout,self).__init__()
        self.setWindowTitle("绝对布局方式")
        self.label1=QLabel("欢迎",self)
        self.label1.move(15,20)

        self.label2 = QLabel("欢迎",self)
        self.label2.move(35, 40)

        self.label3 = QLabel("欢迎",self)
        self.label3.move(55, 80)

if __name__=="__main__":
    app=QApplication(sys.argv)
    p=absolutelayout()
    p.show()
    sys.exit(app.exec_())