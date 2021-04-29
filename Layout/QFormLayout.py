from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys, math
# 9、表单布局QFormLayout()
# https://www.cnblogs.com/Yanjy-OnlyOne/p/12308069.html
class tab(QWidget):
    def __init__(self):
        super(tab, self).__init__()
        self.setWindowTitle("表单布局")
        form=QFormLayout()

        label1=QLabel("标题")
        label2=QLabel("作者")
        label3=QLabel("内容")
        label4=QLabel("内容")

        l1=QLineEdit()
        l2=QLineEdit()
        l3 = QLineEdit()
        l4=QTextEdit()

        # 表单布局直接使用addrow(函数)进行表单布局的放置
        form.addRow(label1,l1)
        form.addRow(label2,l2)
        form.addRow(label3,l3)
        self.setLayout(form)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p =tab()
    p.show()
    sys.exit(app.exec_())