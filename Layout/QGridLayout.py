from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys, math
# 8、栅格布局2
# https://www.cnblogs.com/Yanjy-OnlyOne/p/12308069.html

# 页面布局
class table(QWidget):
    def __init__(self):
        super(table, self).__init__()
        self.setWindowTitle("视频下载神器")

        # ---------------------------表单布局---------------------------
        grid=QGridLayout()
        label1=QLabel("qq号码")
        label2=QLabel("qq密码")
        label3=QLabel("视频地址")
        self.lineEdit = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.lineEdit3 = QLineEdit()
        grid.setSpacing(10)
        grid.addWidget(label1,1,0)
        grid.addWidget(self.lineEdit,1,1)
        grid.addWidget(label2,2,0)
        grid.addWidget(self.lineEdit2,2,1)
        grid.addWidget(label3,3,0)
        grid.addWidget(self.lineEdit3,3,1)
        #---------------------------右下角布局---------------------------
        ok = QPushButton(u'确定', self)
        cancel = QPushButton(u'取消', self)
        empty = QPushButton(u'清空', self)
        right=QHBoxLayout()
        right.addStretch(0)
        right.addWidget(ok)
        right.addWidget(cancel)
        right.addWidget(empty)
        # 添加事件
        ok.clicked.connect(self.handle_camsave)
        cancel.clicked.connect(self.handle_camsave)
        empty.clicked.connect(self.handle_camsave)


        # ---------------------------瀑布流布局---------------------------
        waterfall=QGridLayout()
        names=[{'name':'122942560','passwd':'123456','url':'https://www.yiihuu.com/v_131320.html','nub':'0'},
               {'name':'1200723702','passwd':'2198122','url':'https://www.yiihuu.com/v_131324.html','nub':'1'},
               {'name':'1200723703','passwd':'2198123','url':'https://www.yiihuu.com/v_131324.html','nub':'2'},
               {'name':'1200723704','passwd':'2198124','url':'https://www.yiihuu.com/v_131324.html','nub':'3'} ,
               {'name':'1200723705','passwd':'2198125','url':'https://www.yiihuu.com/v_131324.html','nub':'4'},
               {'name':'1200723706','passwd':'2198126','url':'https://www.yiihuu.com/v_131324.html','nub':'5'},
               {'name':'1200723707','passwd':'2198127','url':'https://www.yiihuu.com/v_131324.html','nub':'6'},
               {'name': '1200723702', 'passwd': '2198122', 'url': 'https://www.yiihuu.com/v_131324.html','nub':'7'},
               {'name': '1200723703', 'passwd': '2198123', 'url': 'https://www.yiihuu.com/v_131324.html','nub':'8'},
               {'name': '1200723704', 'passwd': '2198124', 'url': 'https://www.yiihuu.com/v_131324.html','nub':'9'},
               {'name': '1200723705', 'passwd': '2198125', 'url': 'https://www.yiihuu.com/v_131324.html','nub':'10'},
               {'name': '1200723706', 'passwd': '2198126', 'url': 'https://www.yiihuu.com/v_131324.html','nub':'11'},
               {'name': '1200723707', 'passwd': '2198127', 'url': 'https://www.yiihuu.com/v_131324.html','nub':'12'},
               ]

        positions=[(i,j) for i in range(100) for j in range(4)]
        for position,name in zip(positions,names):   #采用zip组合循环的方式来进行对象的匹配
            names =name['nub'] +'\n' +   name['name'] + '\n' + name['passwd']+ '\n' + name['url']
            btnSelect=QPushButton(names)
            btnSelect.clicked.connect(self.fill_sender)
            waterfall.addWidget(btnSelect,position[0],position[1])  #放置控件名称，位置坐标x,位置坐标y


        # ---------------------------增加到主界面---------------------------
        mainview = QVBoxLayout()
        mainview.addLayout(grid)
        mainview.addLayout(waterfall)
        mainview.addLayout(right)
        self.setLayout(mainview)


    # 填入按钮
    def fill_sender(self):
        sender = self.sender()
        clickevent = sender.text()
        array =  clickevent.split('\n')
        self.lineEdit.setText(array[1])
        self.lineEdit2.setText(array[2])
        self.lineEdit3.setText(array[3])

    # 确定，取消，清空按钮
    def handle_camsave(self):
        sender = self.sender()
        clickevent = sender.text()
        if clickevent == u'确定':
            user = self.lineEdit.text()
            passwd = self.lineEdit2.text()
            url = self.lineEdit3.text()
            print(user,passwd,url)
        elif clickevent == u'取消':
            print(u'单击了第二个按钮')
        elif clickevent == u'清空':
            self.lineEdit.setText("")
            self.lineEdit2.setText("")
            self.lineEdit3.setText("")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    p =table()
    p.show()
    sys.exit(app.exec_())