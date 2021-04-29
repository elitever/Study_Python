from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys, math
# 7、栅格布局方式QGridLayout()
# https://www.cnblogs.com/Yanjy-OnlyOne/p/12308069.html
class calcu(QWidget):
    def __init__(self):
        super(calcu, self).__init__()
        self.setWindowTitle("栅格布局实现计算器UI")
        self.resize(400,300)
        grid=QGridLayout()

        names=["CLS","Back","","Close",
              "7","8","9","/",
              "4","5","6","*",
              "1","2","3","-",
              "0",".","=","+"]
        positions=[(i,j) for i in range(5) for j in range(4)]

        for position,name in zip(positions,names):   #采用zip组合循环的方式来进行对象的匹配
            if name=="":
                continue
            print(position)
            print(name)
            b=QPushButton(name)
            grid.addWidget(b,position[0],position[1])  #放置控件名称，位置坐标x,位置坐标y

      # grid.addWidget(b, *position)  #  *p表示将元组（x,y）转换为x y


        self.setLayout(grid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p =calcu()
    p.show()
    sys.exit(app.exec_())