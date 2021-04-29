from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys, math
# 5、垂直盒方式QVBoxLayout（）
# https://www.cnblogs.com/Yanjy-OnlyOne/p/12308069.html
class vboxlayout(QWidget):
    def __init__(self):
        super(vboxlayout, self).__init__()
        self.setWindowTitle("垂直盒布局方式")
        self.resize(300,200)
        self.layout = QVBoxLayout()

        self.label1 = QPushButton("欢迎")
        self.label2 = QPushButton("欢迎")
        self.label3 = QPushButton("欢迎")
        self.label4 = QPushButton("欢迎")
        self.label5 = QPushButton("欢迎")

        #设置垂直盒布局的对齐方式layout.addwidget(控件，控件位置长度比例，对齐方式)
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.label3)
        self.layout.addWidget(self.label4)
        self.layout.addWidget(self.label5)

        # 设置垂直盒布局的控件间距大小
        self.layout.setSpacing(20)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    p =vboxlayout()
    p.show()
    sys.exit(app.exec_())