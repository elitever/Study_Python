#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
# @project :PythonStudy shikee
# @name :gan
# @Time :2021/3/19/15:40




import pyautogui
import random
import concurrent.futures
import time,re,os,sys,requests
import hashlib, binascii
import json, base64
from PyQt5.QtWidgets import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Crypto.Cipher import AES
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QWidget , QVBoxLayout , QListView, QMessageBox
from PyQt5.QtCore import QStringListModel
import pyperclip

# 视频保存路径
saveRootDirPath = os.path.abspath('.')

# 页面布局
class mainView(QWidget):

    def __init__(self):
        super(mainView, self).__init__()
        self.setWindowTitle("每日免费下载")
        # ---------------------------表单布局---------------------------
        self.grid=QGridLayout()
        # ----------------------------------------
        self.vidolistLabel=QLabel("视频列表地址")
        self.vidolistEdit = QLineEdit('')
        self.grid.addWidget(self.vidolistLabel,1,0)
        self.grid.addWidget(self.vidolistEdit,1,1)
        # ----------------------------------------
        self.beginVideolLabel = QLabel("从第几集开始")
        self.beginVideoEdit = QLineEdit('0')
        self.grid.addWidget(self.beginVideolLabel,2,0)
        self.grid.addWidget(self.beginVideoEdit,2,1)
        # ----------------------------------------
        self.beginaccountLabel = QLabel("从第几个账号开始")
        self.beginaccountEdit = QLineEdit('0')
        self.grid.addWidget(self.beginaccountLabel,3,0)
        self.grid.addWidget(self.beginaccountEdit,3,1)
        # ----------------------------------------
        self.accountLabel = QLabel("账号")
        self.accountEdit = QLineEdit()
        self.grid.addWidget(self.accountLabel,4,0)
        self.grid.addWidget(self.accountEdit,4,1)
        # ----------------------------------------
        self.passwdLabel = QLabel("密码")
        self.passwdEdit = QLineEdit()
        self.grid.addWidget(self.passwdLabel,5,0)
        self.grid.addWidget(self.passwdEdit,5,1)
        # ----------------------------------------
        self.urlLabel = QLabel("视频地址")
        self.urlEdit = QLineEdit()
        self.grid.addWidget(self.urlLabel,6,0)
        self.grid.addWidget(self.urlEdit,6,1)
        # ----------------------------------------
        self.cookieLabel = QLabel("cookie")
        self.cookieEdit = QLineEdit()
        self.grid.addWidget(self.cookieLabel,7,0)
        self.grid.addWidget(self.cookieEdit,7,1)

        self.equlistButton = QPushButton(u'1.读取目录文件（一套课程点击一遍）', self)
        self.accountButton = QPushButton(u'2.获取账号密码', self)
        self.openchromeButton = QPushButton(u'3-1-1.打开浏览器', self)
        self.fillButton = QPushButton(u'3-1-2.手动填入账号和密码', self)
        self.automaticButton = QPushButton(u'3-2.全自动流程', self)
        self.getcookieButton = QPushButton(u'3.获取并且复制cookie', self)

        self.grid.addWidget(self.equlistButton, 1, 2)
        self.grid.addWidget(self.accountButton, 2, 2)
        self.grid.addWidget(self.openchromeButton, 3, 2)
        self.grid.addWidget(self.fillButton, 4, 2)
        self.grid.addWidget(self.automaticButton, 5, 2)
        self.grid.addWidget(self.getcookieButton, 6, 2)
        self.grid.addWidget(self.copycookieButton, 7, 2)


        # 点击事件
        self.equlistButton.clicked.connect(self.handle_Manual)
        self.accountButton.clicked.connect(self.handle_Manual)
        self.openchromeButton.clicked.connect(self.handle_Manual)
        self.fillButton.clicked.connect(self.handle_Manual)
        self.automaticButton.clicked.connect(self.handle_Manual)
        self.getcookieButton.clicked.connect(self.handle_Manual)

        # ---------------------------创建一个列表---------------------------
        layoutbtn = QHBoxLayout()
        global  _slm
        listView = QListView()  # 创建一个listview对象
        _slm = QStringListModel();  # 创建mode
        listView.setModel(_slm)  ##绑定 listView 和 model
        listView.clicked.connect(self.fill_sender)
        layoutbtn.addWidget(listView)
        # ---------------------------增加到主界面---------------------------
        mainview = QVBoxLayout()
        mainview.addLayout(self.grid)
        mainview.addLayout(layoutbtn)
        self.setLayout(mainview)

    # 填入按钮
    def fill_sender(self, qModelIndex):
        global _homeurl, _username, _password
        array = _qList[qModelIndex.row()].split('+')
        # 从第几个账号开始
        self.beginaccountEdit.setText(array[0])
        # 账号
        self.accountEdit.setText(array[1])
        _username = self.accountEdit.text()
        # 密码
        self.passwdEdit.setText(array[2])
        _password = self.passwdEdit.text()
        # 下载的地址
        self.urlEdit.setText(array[3])
        # 从第几个视频下载
        self.beginVideoEdit.setText(array[5])

    # 手动点击事件
    def handle_Manual(self):
        sender = self.sender()
        clickevent = sender.text()
        global _homeurl, _header, _uid , _currencookie ,_browser ,_wait,_chromedriver ,_waterfall ,_slm ,_qList



        if clickevent == u'1.读取目录文件（一套课程点击一遍）':
            req_obj = requests.get(self.firstvidolistEdit.text())
            req_obj.encoding = req_obj.apparent_encoding
            soup = BeautifulSoup(req_obj.text, 'html.parser')
            li_quick = soup.find_all(attrs={'class':'normal list_num'})
            array = []
            dictlist = {}
            for href ,i in  zip(li_quick,range(0,len(li_quick))):
                urs = href.select('a')
                for herss in urs:
                        dict = {}
                        dict['title'] = herss.get('title')
                        dict['url'] = 'https:' + herss.get('href')
                        dict['intnub'] = i
                        array.append(dict)
            dictlist['data_list'] = array
            with open(saveRootDirPath + '/' + 'urllist.json', "w",encoding='utf-8') as json_file:
                json.dump(dictlist, json_file)
            reply = QMessageBox.information(self, '获取视频列表成功', '获取视频列表成功')
        elif clickevent == u'2.获取账号密码':
            def reqeJsonsurl():
                with open(saveRootDirPath + "/urllist.json") as json_file:
                    config = json.load(json_file)
                    return config

            urlname = reqeJsonsurl()['data_list']

            def reqeJsonsqq():
                with open(saveRootDirPath + "/iphone.json") as json_file:
                    config = json.load(json_file)
                    return config

            urlqq = reqeJsonsqq()['data_list']
            _qList = []
            for url, qq in zip(urlname[int(self.beginVideoEdit.text()):],
                               urlqq[int(self.beginaccountEdit.text()):]):  # 采用zip组合循环的方式来进行对象的匹配

                name = qq['nub'] + '+' + qq['name'] + '+' + qq['passwd'] + '+' + url['url'] + '+' + url[
                    'title'] + '+' + str(url['intnub'])
                _qList.append(name)
            _slm.setStringList(_qList)  # 将数据设置到model
        elif clickevent == u'3-1-1.打开浏览器':
            # get直接返回，不再等待界面加载完成
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["pageLoadStrategy"] = "none"
            # Mac系统
            _browser = webdriver.Chrome()
            # windows系统
            # _chromedriver = "C:\chromedriver.exe"  # 这里写本地的chromedriver 的所在路径
            # # os.environ["webdriver.Chrome.driver"] = chromedriver  # 调用chrome浏览器
            # _browser = webdriver.Chrome(_chromedriver)
            _wait = WebDriverWait(_browser, 100, 0.5)
            _homeurl = self.urlEdit.text()
            _browser.get(_homeurl)
        elif clickevent == u'3-1-2.手动填入账号和密码':
            ptlogin_iframe = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ptlogin_iframe"]')))
            _browser.switch_to.frame(ptlogin_iframe)
            # 等待时间
            time.sleep(random.random() * 2)
            # 输入账号和密码
            user = _wait.until(EC.presence_of_element_located((By.ID, 'u')))
            passwd = _wait.until(EC.presence_of_element_located((By.ID, 'p')))
            _username = self.accountEdit.text()
            _password = self.passwdEdit.text()
            user.send_keys(_username)
            passwd.send_keys(_password)
        elif clickevent == u'3-2.全自动流程':
            _homeurl = self.urlEdit.text()
            # get直接返回，不再等待界面加载完成
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["pageLoadStrategy"] = "none"
            # Mac系统
            _browser = webdriver.Chrome()
            # windows系统
            # _chromedriver = "C:\chromedriver.exe"  # 这里写本地的chromedriver 的所在路径
            # os.environ["webdriver.Chrome.driver"] = chromedriver  # 调用chrome浏览器
            # _browser = webdriver.Chrome(_chromedriver)
            # WebDriverWait
            _wait = WebDriverWait(_browser, 50, 0.5)
            _browser.get(_homeurl)
            # 开始下载
            automatic_main.automatic_dowloadbegin()
        elif clickevent == u'3.获取并且复制cookie':
            cookies = ''
            cookie_list = _browser.get_cookies()
            # 格式化打印cookie
            for cookie in cookie_list:
                cookies += '{0}={1};'.format(cookie['name'], cookie['value'])
            self.cookieEdit.setText(cookies)
            pyperclip.copy(cookies)

# 自动下载
class Automatic_main():

    global _homeurl, _header, _uid, _currencookie, _browser, _wait, _chromedriver, _username, _password

    def automatic_dowloadbegin(self):
        time.sleep(random.random() * 2)
        # 打开登录按钮
        login_btn = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_u-login"]/div/a[1]')))
        login_btn.click()
        # 等待时间
        time.sleep(random.random() * 2)

        # 切换登陆弹框
        J_iframe = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_iframe"]')))
        _browser.switch_to.frame(J_iframe)

        # 等待时间
        time.sleep(random.random() * 2)

        # 点击切换登陆按钮
        qiehuanlogin_btn = _wait.until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/ul/li[2]/p')))
        qiehuanlogin_btn.click()

        # 等待时间
        time.sleep(random.random() * 2)

        # 输入账号和密码
        user = _wait.until(EC.presence_of_element_located((By.ID, 'J_account')))
        passwd = _wait.until(EC.presence_of_element_located((By.ID, 'J_password')))
        user.send_keys(_username)
        passwd.send_keys(_password)

        # 等待时间
        time.sleep(random.random() * 2)
        # 点击登陆
        login_btn = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_sbbtn"]')))
        login_btn.click()


        return 1
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 页面布局
    mainview =mainView()
    mainview.show()
    # 自动下载函数
    automatic_main = Automatic_main()
    sys.exit(app.exec_())