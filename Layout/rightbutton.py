from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys, math
# 6、将按钮永远放在窗口右下角
# https://www.cnblogs.com/Yanjy-OnlyOne/p/12308069.html
class rightbutton(QWidget):
    def __init__(self):
        super(rightbutton, self).__init__()
        self.setWindowTitle("按钮放在窗口的右下角")
        self.resize(400,300)

        ok=QPushButton("确定")
        cancel=QPushButton("取消")

        h=QHBoxLayout()
        h.addStretch(1)
        h.addWidget(ok)
        h.addWidget(cancel)

        v=QVBoxLayout()
        bt1=QPushButton("按钮1")
        bt2 = QPushButton("按钮2")
        bt3 = QPushButton("按钮3")

        v.addStretch(0)   #放在上面
        v.addWidget(bt1)
        v.addWidget(bt2)
        v.addWidget(bt3)

        v.addStretch(1)  #始终保持在放在右下角
        v.addLayout(h)
        self.setLayout(v)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = rightbutton()
    p.show()
    sys.exit(app.exec_())