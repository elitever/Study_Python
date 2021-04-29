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

# 视频保存路径
saveRootDirPath = os.path.abspath('.')

# 页面布局
class mainView(QWidget):

    def __init__(self):
        super(mainView, self).__init__()
        self.setWindowTitle("每日免费下载")
        # ---------------------------表单布局---------------------------
        self.grid=QGridLayout()
        # -------------------第一行---------------------
        self.firstvidolistLabel=QLabel("视频列表地址")
        self.firstvidolistEdit = QLineEdit('')
        self.grid.addWidget(self.firstvidolistLabel,1,0)
        self.grid.addWidget(self.firstvidolistEdit,1,1)
        # -------------------第二行---------------------
        self.secondbeginLabel = QLabel("从第几集开始")
        self.secondbeginEdit = QLineEdit('0')
        self.grid.addWidget(self.secondbeginLabel,2,0)
        self.grid.addWidget(self.secondbeginEdit,2,1)
        # -------------------第三行---------------------
        self.thirdQQLabel = QLabel("从第几个账号开始")
        self.thirdQQEdit = QLineEdit('0')
        self.grid.addWidget(self.thirdQQLabel,3,0)
        self.grid.addWidget(self.thirdQQEdit,3,1)
        # -------------------第六行---------------------
        self.sixthusernameLabel = QLabel("账号")
        self.sixthusernameEdit = QLineEdit()
        self.grid.addWidget(self.sixthusernameLabel,4,0)
        self.grid.addWidget(self.sixthusernameEdit,4,1)
        # -------------------第七行---------------------
        self.seventhpasswdLabel = QLabel("密码")
        self.seventhpasswdEdit = QLineEdit()
        self.grid.addWidget(self.seventhpasswdLabel,5,0)
        self.grid.addWidget(self.seventhpasswdEdit,5,1)
        # -------------------第八行---------------------
        self.eighthviderulLabel = QLabel("视频地址")
        self.eighthviderulEdit = QLineEdit()
        self.grid.addWidget(self.eighthviderulLabel,6,0)
        self.grid.addWidget(self.eighthviderulEdit,6,1)

        self.firstequlistButton = QPushButton(u'读取目录文件（一套课程点击一遍）', self)
        self.seventhemptyButton = QPushButton(u'重新下载', self)
        self.secondbeginaccountButton = QPushButton(u'获取账号密码网页', self)
        self.secondbeginaccountiphonButton = QPushButton(u'获取手机登录', self)
        self.thirdopenchromeButton = QPushButton(u'1.打开浏览器', self)
        self.fourthfillButton = QPushButton(u'2.手动填入QQ和密码', self)
        self.eighthdowloadButton = QPushButton(u'全流程自动', self)
        self.eighthdowloadshoujiButton = QPushButton(u'手机号全流程自动', self)

        self.grid.addWidget(self.firstequlistButton, 1, 2)
        self.grid.addWidget(self.seventhemptyButton, 1, 3)

        self.grid.addWidget(self.thirdopenchromeButton, 2, 2)
        self.grid.addWidget(self.fourthfillButton, 2, 3)

        self.grid.addWidget(self.secondbeginaccountButton, 3, 2)
        self.grid.addWidget(self.secondbeginaccountiphonButton, 3, 3)

        self.grid.addWidget(self.eighthdowloadButton, 4, 2)
        self.grid.addWidget(self.eighthdowloadshoujiButton, 4, 3)

        # 点击事件
        self.firstequlistButton.clicked.connect(self.handle_Manual)
        self.seventhemptyButton.clicked.connect(self.handle_Manual)
        self.thirdopenchromeButton.clicked.connect(self.handle_Manual)
        self.fourthfillButton.clicked.connect(self.handle_Manual)
        self.eighthdowloadButton.clicked.connect(self.handle_Manual)
        self.eighthdowloadshoujiButton.clicked.connect(self.handle_Manual)
        self.secondbeginaccountButton.clicked.connect(self.handle_Manual)
        self.secondbeginaccountiphonButton.clicked.connect(self.handle_Manual)

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
        global _homeurl, _username, _password , _titlename
        array = _qList[qModelIndex.row()].split('+')
        # 账号
        self.sixthusernameEdit.setText(array[1])
        _username = self.sixthusernameEdit.text()
        # 密码
        self.seventhpasswdEdit.setText(array[2])
        _password = self.seventhpasswdEdit.text()
        # 下载的地址
        self.eighthviderulEdit.setText(array[3])

        self.secondbeginEdit.setText(array[5])

        self.thirdQQEdit.setText(array[0])

        _titlename =array[4]
    # 手动点击事件
    def handle_Manual(self):
        sender = self.sender()
        clickevent = sender.text()
        global _homeurl, _header, _uid , _currencookie ,_browser ,_wait,_chromedriver ,_waterfall ,_slm ,_qList


        if clickevent == u'读取目录文件（一套课程点击一遍）':
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
        elif clickevent == u'重新下载':
            _browser.refresh()  # 刷新页面
            # 等待时间
            time.sleep(random.random() * 2)
            cookies = ''
            cookie_list = _browser.get_cookies()
            # 格式化打印cookie
            for cookie in cookie_list:
                cookies += '{0}={1};'.format(cookie['name'], cookie['value'])
            _currencookie = cookies

            if len(_currencookie) > 0:
                time.sleep(random.random() * 2)
                _header = {
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                    'Cookie': _currencookie}

                _browser.quit()
            copybox = QMessageBox.information(self, '下载完成', '点击复制', QMessageBox.Yes)
            if copybox == QMessageBox.Yes:
                pyautogui.leftClick(int(self.fourthcopyxEdit.text()), int(self.fivecopyyEdit.text()))
                pyautogui.hotkey('ctrl', 'c')
        elif clickevent == u'获取账号密码网页':
            def reqeJsonsurl():
                with open(saveRootDirPath + "/urllist.json") as json_file:
                    config = json.load(json_file)
                    return config
            urlname = reqeJsonsurl()['data_list']
            def reqeJsonsqq():
                with open(saveRootDirPath + "/qq.json") as json_file:
                    config = json.load(json_file)
                    return config
            urlqq = reqeJsonsqq()['data_list']
            _qList = []
            for url, qq in zip(urlname[int(self.secondbeginEdit.text()):], urlqq[int(self.thirdQQEdit.text()):]):  # 采用zip组合循环的方式来进行对象的匹配

                name = qq['nub'] + '+' + qq['name'] + '+' + qq['passwd'] + '+' + url['url'] + '+' + url['title'] + '+' + str(url['intnub'])
                _qList.append(name)
            _slm.setStringList(_qList)  # 将数据设置到model
        elif clickevent == u'获取手机登录':
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
            for url, qq in zip(urlname[int(self.secondbeginEdit.text()):],
                               urlqq[int(self.thirdQQEdit.text()):]):  # 采用zip组合循环的方式来进行对象的匹配

                name = qq['nub'] + '+' + qq['name'] + '+' + qq['passwd'] + '+' + url['url'] + '+' + url[
                    'title'] + '+' + str(url['intnub'])
                _qList.append(name)
            _slm.setStringList(_qList)  # 将数据设置到model
        elif clickevent == u'1.打开浏览器':
            # get直接返回，不再等待界面加载完成
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["pageLoadStrategy"] = "none"
            # Mac系统
            # _browser = webdriver.Chrome()
            # windows系统
            _chromedriver = "C:\chromedriver.exe"  # 这里写本地的chromedriver 的所在路径
            # # os.environ["webdriver.Chrome.driver"] = chromedriver  # 调用chrome浏览器
            _browser = webdriver.Chrome(_chromedriver)
            _wait = WebDriverWait(_browser, 100, 0.5)
            _homeurl = self.eighthviderulEdit.text()
            _browser.get(_homeurl)
        elif clickevent == u'2.手动填入QQ和密码':
            ptlogin_iframe = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ptlogin_iframe"]')))
            _browser.switch_to.frame(ptlogin_iframe)
            # 等待时间
            time.sleep(random.random() * 2)
            # 输入账号和密码
            user = _wait.until(EC.presence_of_element_located((By.ID, 'u')))
            passwd = _wait.until(EC.presence_of_element_located((By.ID, 'p')))
            _username = self.sixthusernameEdit.text()
            _password = self.seventhpasswdEdit.text()
            user.send_keys(_username)
            passwd.send_keys(_password)
        elif clickevent == u'全流程自动':
            _homeurl = self.eighthviderulEdit.text()
            # get直接返回，不再等待界面加载完成
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["pageLoadStrategy"] = "none"
            # Mac系统
            # browser = webdriver.Chrome()
            # windows系统
            _chromedriver = "C:\chromedriver.exe"  # 这里写本地的chromedriver 的所在路径
            # os.environ["webdriver.Chrome.driver"] = chromedriver  # 调用chrome浏览器
            _browser = webdriver.Chrome(_chromedriver)
            # _browser.set_window_size(1920 / 2 - 180, 800)
            # WebDriverWait
            _wait = WebDriverWait(_browser, 100, 0.5)
            _browser.get(_homeurl)
            # 开始下载

            reply = QMessageBox.information(self, '完成', '去下载', QMessageBox.Yes| QMessageBox.No )
            if reply == QMessageBox.Yes:
                _browser.refresh()  # 刷新页面
                # 等待时间
                time.sleep(random.random() * 2)
                # 点击播放按钮
                begin_play = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="begin_play"]')))
                begin_play.click()
                # 等待时间
                time.sleep(random.random() * 2)
                # 点击播放按钮
                play = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="free_btn_two"]')))
                play.click()
                # 等待时间
                time.sleep(random.random() * 2)
                cookies = ''
                cookie_list = _browser.get_cookies()
                # 格式化打印cookie
                for cookie in cookie_list:
                    cookies += '{0}={1};'.format(cookie['name'], cookie['value'])
                _currencookie = cookies

                if len(_currencookie) > 0:
                    time.sleep(random.random() * 2)
                    _header = {
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                        'Cookie': _currencookie}

                    _browser.quit()
                copybox = QMessageBox.information(self, '下载完成', '点击复制', QMessageBox.Yes)
                if copybox == QMessageBox.Yes:
                    pyautogui.leftClick(int(self.fourthcopyxEdit.text()), int(self.fivecopyyEdit.text()))
                    pyautogui.hotkey('ctrl', 'c')
            else:
                print( '完成')
        elif clickevent == u'手机号全流程自动':
            _homeurl = self.eighthviderulEdit.text()
            # get直接返回，不再等待界面加载完成
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["pageLoadStrategy"] = "none"
            # Mac系统
            # _browser = webdriver.Chrome()
            # # windows系统
            _chromedriver = "C:\chromedriver.exe"  # 这里写本地的chromedriver 的所在路径
            # os.environ["webdriver.Chrome.driver"] = chromedriver  # 调用chrome浏览器
            _browser = webdriver.Chrome(_chromedriver)
            # _browser.set_window_size(1920 / 2 - 180, 800)
            # WebDriverWait
            _wait = WebDriverWait(_browser, 100, 0.5)
            _browser.get(_homeurl)

            reply = QMessageBox.information(self, '完成', '去下载', QMessageBox.Yes| QMessageBox.No)
            if reply == QMessageBox.Yes:
                _browser.refresh()  # 刷新页面
                # 等待时间
                time.sleep(random.random() * 2)
                # 点击播放按钮
                begin_play = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="begin_play"]')))
                begin_play.click()
                # 等待时间
                time.sleep(random.random() * 2)
                # 点击播放按钮
                play = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="free_btn_two"]')))
                play.click()
                # 等待时间
                time.sleep(random.random() * 2)
                cookies = ''
                cookie_list = _browser.get_cookies()
                # 格式化打印cookie
                for cookie in cookie_list:
                    cookies += '{0}={1};'.format(cookie['name'], cookie['value'])
                _currencookie = cookies

                if len(_currencookie) > 0:
                    time.sleep(random.random() * 2)
                    _header = {
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                        'Cookie': _currencookie}

                    _browser.quit()
                copybox = QMessageBox.information(self, '下载完成', '点击复制', QMessageBox.Yes)
                if copybox == QMessageBox.Yes:
                    pyautogui.leftClick(int(self.fourthcopyxEdit.text()), int(self.fivecopyyEdit.text()))
                    pyautogui.hotkey('ctrl', 'c')
            else:
                print( '完成')
            pyautogui.hotkey('ctrl', 'c')
        elif clickevent == u'开始下载':

            # _browser.get(self.eighthviderulEdit.text())
            _browser.refresh()  # 刷新页面
            # 等待时间
            time.sleep(random.random() * 2)
            # 点击播放按钮
            begin_play = _wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="begin_play"]')))
            begin_play.click()
            # 等待时间
            time.sleep(random.random() * 2)
            # 点击播放按钮
            play = _wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="free_btn_two"]')))
            play.click()
            # 等待时间
            time.sleep(random.random() * 2)
            cookies = ''
            cookie_list = _browser.get_cookies()
            # 格式化打印cookie
            for cookie in cookie_list:
                cookies += '{0}={1};'.format(cookie['name'], cookie['value'])
            _currencookie = cookies

            if len(_currencookie) > 0:
                time.sleep(random.random() * 2)
                _header = {
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                    'Cookie': _currencookie}

                _browser.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 页面布局
    mainview =mainView()
    mainview.show()
    sys.exit(app.exec_())