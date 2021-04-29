from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys, math

# 3、水平布局设置伸缩量
# https://www.cnblogs.com/Yanjy-OnlyOne/p/12308069.html
class absolutelayout(QWidget):
    def __init__(self):
        super(absolutelayout, self).__init__()
        self.setWindowTitle("设置伸缩量")
        self.resize(800,100)
        self.layout = QHBoxLayout()

        self.btn1=QPushButton("按钮1")
        self.btn2= QPushButton("按钮2")
        self.btn3= QPushButton("按钮3")
        self.btn4 = QPushButton("按钮4")
        self.btn5 = QPushButton("按钮5")

        #将前五个按钮放在左边显示
        self.layout.addStretch(0)  #设置布局的伸缩量-默认右对齐方式
        self.layout.addWidget(self.btn1)
        self.layout.addWidget(self.btn2)
        self.layout.addWidget(self.btn3)
        self.layout.addWidget(self.btn4)
        self.layout.addWidget(self.btn5)

        #将第6个和第7个按钮放在右边显示
        self.btn6=QPushButton("按钮6")
        self.btn7=QPushButton("按钮7")
        self.layout.addStretch(1)
        self.layout.addWidget(self.btn6)
        self.layout.addWidget(self.btn7)

        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = absolutelayout()
    p.show()
    sys.exit(app.exec_())