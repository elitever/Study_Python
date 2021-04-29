from PyQt5.QtWidgets import *
import sys,math

# 2、水平盒方式QHBoxLayout
# https://www.cnblogs.com/Yanjy-OnlyOne/p/12308069.html
class hboxlayout(QWidget):
    def __init__(self):
        super(hboxlayout,self).__init__()
        self.setWindowTitle("水平盒布局方式")
        self.layout=QHBoxLayout()

        self.label1=QLabel("欢迎")
        self.label2 = QLabel("欢迎")
        self.label3 = QLabel("欢迎")
        self.label4 = QLabel("欢迎")
        self.label5 = QLabel("欢迎")

        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.label4)
        self.layout.addWidget(self.label5)

        # 设置水平盒布局的控件间距大小
        self.layout.setSpacing(100)
        self.setLayout(self.layout)

if __name__=="__main__":
    app=QApplication(sys.argv)
    p=hboxlayout()
    p.show()
    sys.exit(app.exec_())