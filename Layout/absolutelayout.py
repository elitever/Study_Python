from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys, math
# 4、水平盒方式QHBoxLayout的对齐方式.
# https://www.cnblogs.com/Yanjy-OnlyOne/p/12308069.html
class absolutelayout(QWidget):
    def __init__(self):
        super(absolutelayout, self).__init__()
        self.setWindowTitle("控件对齐方式")
        self.layout = QHBoxLayout()

        self.label1 = QLabel("欢迎")
        self.label2 = QLabel("欢迎")
        self.label3 = QLabel("欢迎")
        self.label4 = QLabel("欢迎")
        self.label5 = QLabel("欢迎")

        #设置水平盒布局的对齐方式layout.addwidget(控件，控件位置长度比例，对齐方式)
        self.layout.addWidget(self.label1,2,Qt.AlignLeft | Qt.AlignTop)
        self.layout.addWidget(self.label2,1,Qt.AlignLeft | Qt.AlignTop)
        self.layout.addWidget(self.label3,1,Qt.AlignLeft | Qt.AlignBottom)
        self.layout.addWidget(self.label4,1,Qt.AlignLeft | Qt.AlignBottom)
        self.layout.addWidget(self.label5,1,Qt.AlignLeft)

        # 设置水平盒布局的控件间距大小
        self.layout.setSpacing(20)
        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = absolutelayout()
    p.show()
    sys.exit(app.exec_())