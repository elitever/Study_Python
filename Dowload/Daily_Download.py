#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
# @project :PythonStudy shikee
# @name :gan
# @Time :2021/2/22/09:49

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
# title
title = None
# ts count
sumCount = None
# 已处理的ts
doneCount = None
# cache path
cachePath = saveRootDirPath + "/cache"
# log path
logPath = cachePath + "/log.log"
# log file
logFile = None
#=================================================================
BS = AES.block_size  # 这个等于16
mode = AES.MODE_CBC
pad = lambda s: s + (BS-len(s))*"\0"  # 用于补全key
# 用于补全下面的text，上面两个网址就是用以下形式补全的
pad_txt = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[-1]]

global _homeurl, _header, _uid , _currencookie ,_browser ,_wait ,_chromedriver ,_username ,_password ,_waterfall ,_slm ,_qList,_titlename

# 页面布局
class mainView(QWidget):

    def __init__(self):
        super(mainView, self).__init__()
        self.setWindowTitle("每日免费下载")
        # ---------------------------表单布局---------------------------
        self.grid=QGridLayout()
        # ---------------------------------------
        self.firstvidolistLabel=QLabel("视频列表地址")
        self.firstvidolistEdit = QLineEdit('')
        self.grid.addWidget(self.firstvidolistLabel,1,0)
        self.grid.addWidget(self.firstvidolistEdit,1,1)
        # ---------------------------------------
        self.secondbeginLabel = QLabel("从第几集开始")
        self.secondbeginEdit = QLineEdit('0')
        self.grid.addWidget(self.secondbeginLabel,2,0)
        self.grid.addWidget(self.secondbeginEdit,2,1)
        # ---------------------------------------
        self.thirdQQLabel = QLabel("从第几个账号开始")
        self.thirdQQEdit = QLineEdit('0')
        self.grid.addWidget(self.thirdQQLabel,3,0)
        self.grid.addWidget(self.thirdQQEdit,3,1)
        # ---------------------------------------
        self.sixthusernameLabel = QLabel("账号")
        self.sixthusernameEdit = QLineEdit()
        self.grid.addWidget(self.sixthusernameLabel,4,0)
        self.grid.addWidget(self.sixthusernameEdit,4,1)
        # ---------------------------------------
        self.seventhpasswdLabel = QLabel("密码")
        self.seventhpasswdEdit = QLineEdit()
        self.grid.addWidget(self.seventhpasswdLabel,5,0)
        self.grid.addWidget(self.seventhpasswdEdit,5,1)
        # ---------------------------------------
        self.eighthviderulLabel = QLabel("视频地址")
        self.eighthviderulEdit = QLineEdit()
        self.grid.addWidget(self.eighthviderulLabel,6,0)
        self.grid.addWidget(self.eighthviderulEdit,6,1)


        self.firstequlistButton = QPushButton(u'读取目录文件', self)
        self.seventhemptyButton = QPushButton(u'重新下载', self)
        self.secondbeginaccountButton = QPushButton(u'获取账号密码网页', self)
        self.secondbeginaccountiphonButton = QPushButton(u'获取手机登录', self)
        self.thirdopenchromeButton = QPushButton(u'1.打开浏览器', self)
        self.fourthfillButton = QPushButton(u'2.手动填入账号和密码', self)
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

        if clickevent == u'读取目录文件':
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
                # 开始下载
                manual_main.dowloadbegin()
                _browser.quit()
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
        elif clickevent == u'2.手动填入账号和密码':
            ptlogin_iframe = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ptlogin_iframe"]')))
            _browser.switch_to.frame(ptlogin_iframe)
            # 等待时间
            time.sleep(random.random() * 2)
            # 输入账号和密码
            # user = _wait.until(EC.presence_of_element_located((By.ID, 'u')))
            # passwd = _wait.until(EC.presence_of_element_located((By.ID, 'p')))
            # 输入账号和密码
            user = _wait.until(EC.presence_of_element_located((By.ID, 'J_account')))
            passwd = _wait.until(EC.presence_of_element_located((By.ID, 'J_password')))
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
            automatic_main.automatic_dowloadbegin('YES')
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
                    # 开始下载
                    manual_main.dowloadbegin()
                    _browser.quit()
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
            # 开始下载
            automatic_main.automatic_dowloadbegin('NO')
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
                    # 开始下载
                    manual_main.dowloadbegin()
                    _browser.quit()
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
                # 开始下载
                manual_main.dowloadbegin()
                _browser.quit()
# 手动下载函数
class Manual_main():

    global _homeurl, _header, _uid , _currencookie ,_browser ,_wait ,_chromedriver ,_username ,_password,_titlename

    # get请求数据
    def urlget(self,url, header):
        response = requests.get(url, headers=header)
        return response.content.decode('utf-8')

    # post请求数据
    def urlpost(self,url, postdata, header):
        response = requests.post(url, postdata, headers=header)
        return response.content.decode('utf-8')

    # 0.创建本地存储目录
    def mkdir(self,path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)

            print(path + ' 创建成功')
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(path + ' 目录已存在')
            return False

    # 1.读取本地JSON数据,全局赋值
    def reqeJson(self):
        with open(saveRootDirPath + "/content111.json") as json_file:
            config = json.load(json_file)
            homeurl = config['url']
            header = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                'Cookie': config['Cookie']}
            uid = config['uid']
        return {'homeurl': homeurl, 'header': header, 'uid': uid}

    # 2.请求vid
    def getVid(self,url):
        if ('lib' in url):
            libvid = url[url.rindex('vid=') + 1:].replace('id=', '')
            return libvid
        libvid = url[url.rindex('v_') + 1:].replace('_', '').replace('.html', '')
        return libvid

    # 3.请求videoid
    def getVideoid(self,vid):
        if ('lib' in _homeurl):
            libvideo = 'https://www.yiihuu.com/get_yhdesigner_video_uri.php?video_type=xhtml&play_video_id=' + vid + '&uid=' + _uid
            content = self.urlget(libvideo, _header).strip()
            info_enc = json.loads(content)
            subcon = info_enc["url"]
            if '.mp4' in subcon:
                self.dowloadMP4(subcon)
                sys.exit(0)
            subcontent = subcon[0:-14]
            return subcontent
        libvideo = 'https://www.yiihuu.com/get_video_uri.php?video_type=xhtml&play_video_id=' + vid
        content = self.urlget(libvideo, _header).strip()
        if '.mp4' in content:
            self.dowloadMP4(content)
            sys.exit(0)
        subcontent = content[0:-11]
        return subcontent

    # 3.当前是MP4，则下载完成够退出程序
    def dowloadMP4(self,url):
        # 获取标题
        req_obj = requests.get(_homeurl)
        req_obj.encoding = req_obj.apparent_encoding
        soup = BeautifulSoup(req_obj.text, 'html.parser')
        titleName = soup.find(attrs={"name": "keywords"})['content']
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            outputFp = open(saveRootDirPath + '/' + titleName + '.mp4', "wb+")
            outputFp.write(response.content)
            print('下载完成')
            _browser.quit()

    # 4.请求body
    def vidinfo(self,g_videoid):
        url = 'https://player.polyv.net/secure/' + g_videoid + '.json'
        content = self.urlget(url, _header).strip()
        if not content:
            return None
        info_enc = json.loads(content)
        if int(info_enc["code"]) != 200:
            print(info_enc)
            return None
        body = info_enc["body"]
        # 4-1.解密返回的JSON数据
        info = json.loads(self.videoinfo_decrypt(g_videoid, body))
        return {"m3u8": info["hls"][-1], "seed_const": info["seed_const"], "title": info["title"]}

    # 4-1.解密返回的JSON数据
    def videoinfo_decrypt(self,vid, body):
        # print("vid: " + _vid)
        hash = hashlib.md5()
        hash.update(vid.encode('utf-8'))
        str = hash.hexdigest()
        # print("vid md5: " + _str)
        key = str[0: 16]
        iv = str[16:]
        # print("key: " + _key + " iv: " + _iv)
        body_raw = binascii.a2b_hex(body)
        cryptor = AES.new(key.encode('utf-8'), mode, iv.encode('utf-8'))
        ret = base64.b64decode(unpad(cryptor.decrypt(body_raw))).decode('utf-8')
        return ret

    # 5.m3u8key文件获取
    def get_m3u8Key(self,m3u8, vid):
        m3u8content = self.urlget(m3u8, _header)
        if not m3u8content:
            print("get m3u8(%s) error" % (m3u8))
            return 0
        rem = re.search(r'URI="([^"]+)"', m3u8content, re.M | re.I)
        if not rem:
            print("m3u8 key url not found")
            return 0
        # 5-1请求token
        m3u8keyurl = rem.group(1).strip() + "?token=" + self.get_playsafe_token(vid)
        m3u8keyurl = re.sub(r'://([^/]+)/', r'://\1/playsafe/', m3u8keyurl, 1, re.I)
        m3u8key = requests.get(m3u8keyurl).content

        return {'m3u8key': m3u8key, 'm3u8content': m3u8content}

    # 5-1请求token
    def get_playsafe_token(self,_vid):
        # // 保利威视自定义参数存视频id和专辑id, 随机对应id
        _url = 'https://www.yiihuu.com/polyv/polyv_get_token.php?vid=' + _vid
        _content = self.urlget(_url, _header).strip()
        return _content

    # 6.解密key文件
    def decode_key(self,seed_const, key_enc):
        m = hashlib.md5()
        strseed_const = str(seed_const)
        seed_md5 = strseed_const.encode(encoding='utf-8')
        m.update(seed_md5)
        str_md5 = m.hexdigest()
        aeskey = str_md5[0: 16]
        aesiv = b'\x01\x02\x03\x05\x07\x0B\x0D\x11\x13\x17\x1D\x07\x05\x03\x02\x01'
        cryptor = AES.new(aeskey.encode('utf-8'), AES.MODE_CBC, aesiv)
        plain_text = (cryptor.decrypt(key_enc))
        ret = re.findall(b"[\s\S]{16}", plain_text)  # 就是这里需要做小小的改造，看仔细哦
        return ret

    # 7.获取iv偏移量
    def get_IV(self,m3u8contents, g_videoid):

        m3u8content = re.sub(r'URI="([^"]+)"', 'URI="%s"' % (g_videoid + ".key"), m3u8contents, 1, re.M | re.I)
        jiami = re.findall('#EXT-X-KEY:(.*)\n', m3u8content)
        iv = re.findall('IV=(.*)', jiami[0])[0]
        IVV = iv.replace('0x', '')[:16].encode()
        return {'iv': IVV, 'm3u8content': m3u8content}

    # 8.多线程ts视频链接
    def download_all(self,sites):
        # future列表中每个future完成的顺序，和它在列表中的顺序并不一定完全一致。
        # 到底哪个先完成、哪个后完成，取决于系统的调度和每个future的执行时间
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            to_do = []
            for site in sites:
                # executor.submit返回future实例
                future = executor.submit(self.download_one, site)
                to_do.append(future)
                # future.add_done_callback(over)
            # 在futures完成后打印结果
            for future in concurrent.futures.as_completed(to_do):
                if future.exception() is not None:
                    print(future.exception())
                else:
                    print(future.result())

    # 8-1.单线程ts视频链接
    def download_one(self,url):
        global logFile
        global sumCount
        global doneCount
        global cachePath
        titleTS = url.split('_')[-1].replace('.ts', '')
        outputPaths = cachePath + "/" + "{0:0>8}.ts".format(int(titleTS))
        outputFp = open(outputPaths, "wb+")
        response = requests.get(url)
        if response.status_code == 200:
            expected_length = int(response.headers.get('Content-Length'))
            actual_length = len(response.content)
            if expected_length > actual_length:
                raise Exception("分片下载不完整")
            outputFp.write(response.content)
            doneCount += 1
            self.printProcessBar(sumCount, doneCount, 50)
            succeed = True
        print('Read {} from {}'.format(len(response.content), url))
        return f'download {len(response.content)} ok'

    # 9、合并ts
    def mergeTs(self,tsFileDir, outputFilePath, cryptor, count):
        global logFile
        outputFp = open(outputFilePath, "wb+")
        for index in range(count):
            self.printProcessBar(count, index + 1, 50)

            inputFilePath = tsFileDir + "/" + "{0:0>8}.ts".format(index)
            if not os.path.exists(outputFilePath):
                print("\n分片{0:0>8}.ts, 不存在，已跳过！".format(index))
                continue
            inputFp = open(inputFilePath, "rb")
            fileData = inputFp.read()
            try:
                if cryptor is None:
                    outputFp.write(fileData)
                else:
                    outputFp.write(cryptor.decrypt(fileData))
            except Exception as exception:
                inputFp.close()
                outputFp.close()
                print(exception)
                return False
            inputFp.close()
        outputFp.close()
        return True

    # 10.convert to mp4（调用了FFmpeg，将合并好的视频内容放置到一个mp4容器中）
    def ffmpegConvertToMp4(self,inputFilePath, ouputFilePath):
        global logFile
        if not os.path.exists(inputFilePath):
            print(inputFilePath + " 路径不存在！")
            return False
        cmd = r'ffmpeg -i "{0}" -vcodec copy -acodec copy "{1}"'.format(inputFilePath, ouputFilePath)
        if os.system(cmd) == 0:
            print(inputFilePath + "转换成功！")
            _browser.quit()
            return True
        else:
            print(inputFilePath + "转换失败！")
            return False

    # 11.删除ts文件
    def removeTsDir(self,tsFileDir):
        # 先清空文件夹
        for root, dirs, files in os.walk(tsFileDir, topdown=False):

            for name in files:
                os.remove(os.path.join(root, name))
        return True

    # 8、模拟输出进度条
    def printProcessBar(self,sumCount, doneCount, width):
        precent = doneCount / sumCount
        useCount = int(precent * width)
        spaceCount = int(width - useCount)
        precent = precent * 100
        print('\t{0}/{1} {2}{3} {4:.2f}%'.format(sumCount, doneCount, useCount * '■', spaceCount * '□', precent),
              file=sys.stdout, flush=True, end='\r')
    # 开始下载
    def dowloadbegin(self):

        # 1.创建目录
        self.mkdir(cachePath)
        # 2.请求vid
        vid = self.getVid(_homeurl)
        if not vid:
            print("get vid(%s) information error" % (vid))
            return 0
        # 3.请求videoid
        g_videoid = self.getVideoid(vid)
        if not g_videoid:
            print("get g_videoid(%s) information error" % (g_videoid))
            return 0
        # 4.请求body
        vinfo = self.vidinfo(g_videoid)
        if not vinfo:
            print("get vinfo(%s) information error" % (vinfo))
            _browser.quit()
            return 0

        # 5.请求m3u8key
        m3u8keyDict = self.get_m3u8Key(vinfo["m3u8"], vid)
        m3u8key = m3u8keyDict['m3u8key']

        # 6.解密key
        if len(m3u8key) == 32:
            print("key length is 32, decoding...")
            m3u8key = self.decode_key(vinfo["seed_const"], m3u8key)

        # 7.获取iv偏移量
        iv_dict = self.get_IV(m3u8keyDict['m3u8content'], g_videoid)
        iv = iv_dict['iv']
        m3u8content = iv_dict['m3u8content']

        if not iv:
            print("get vinfo(%s) information error" % (iv))
            return 0

        cryptor = AES.new(m3u8key[0], AES.MODE_CBC, iv)  # 解密视频流

        # 8.多线程ts视频链接
        tslist = re.findall('EXTINF:(.*),\n(.*)\n#', m3u8content)
        newlist = []
        for i in tslist:
            newlist.append(i[1])
        start_time = time.perf_counter()
        self.download_all(newlist)
        end_time = time.perf_counter()
        print('Download {} sites in {} seconds'.format(len(newlist), end_time - start_time))

        # 9.合并ts
        if self.mergeTs(cachePath, cachePath + "/cache.flv", cryptor, len(newlist)):
            print("ts合并完成---------------------！")
        else:
            print("ts合并失败---------------------！")
            return False

        # 10.convert to mp4（调用了FFmpeg，将合并好的视频内容放置到一个mp4容器中）
        self.ffmpegConvertToMp4(cachePath + "/cache.flv", saveRootDirPath + "/" + _titlename + ".mp4")

        # # 11.删除ts文件
        self.removeTsDir(cachePath)

        return 0
# 自动下载
class Automatic_main():

    global _homeurl, _header, _uid, _currencookie, _browser, _wait, _chromedriver, _username, _password

    def automatic_dowloadbegin(self,type):

        if (type == "YES"):
            # 打开登录按钮
            login_btn = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_u-login"]/div/a[1]')))
            login_btn.click()

            # 切换登陆弹框
            J_iframe = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_iframe"]')))
            _browser.switch_to.frame(J_iframe)

            # 等待时间
            time.sleep(random.random() * 2)

            # 点击QQ登陆按钮
            loginQQ_btn = _wait.until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/ul/li[1]/a')))
            loginQQ_btn.click()

            # 等待时间
            time.sleep(random.random() * 2)

            def gotoRe():
                res = EC.title_is("browser.title")(_browser)
                if res:
                    loginQQ_btn.click()
                else:
                    ptlogin_iframe()

            def ptlogin_iframe():
                # 切换QQ登陆界面
                res = EC.title_is("QQ帐号安全登录")(_browser)
                if res:
                    ptlogin_iframe = _wait.until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="ptlogin_iframe"]')))
                    _browser.switch_to.frame(ptlogin_iframe)
                    # 等待时间
                    time.sleep(random.random() * 2)
                else:
                    gotoRe()

            # 等待时间
            time.sleep(random.random() * 2)

            ptlogin_iframe()

            # 等待时间
            time.sleep(random.random() * 2)

            loginqiehuan_btn = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="switcher_plogin"]')))
            loginqiehuan_btn.click()

            # 输入账号和密码
            user = _wait.until(EC.presence_of_element_located((By.ID, 'u')))
            passwd = _wait.until(EC.presence_of_element_located((By.ID, 'p')))
            user.send_keys(_username)
            passwd.send_keys(_password)

            # 等待时间
            time.sleep(random.random() * 2)
            # 点击登陆按钮事件
            login = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_button"]')))
            login.click()
        else:
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

            # 等待时间
            time.sleep(random.random() * 2)

            # 等待时间
            time.sleep(random.random() * 2)
            cookies = ''
            cookie_list = _browser.get_cookies()
            # 格式化打印cookie
            for cookie in cookie_list:
                cookies += '{0}={1};'.format(cookie['name'], cookie['value'])
            _currencookie = cookies

        return 1

if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # # 页面布局
    # mainview =mainView()
    # mainview.show()
    # # 手动下载函数
    # manual_main = Manual_main()
    # # 自动下载函数
    # automatic_main = Automatic_main()
    #
    # sys.exit(app.exec_())

    array = []
    dictlist = {}
    for i in range(0,500):
        dict = {}
        if i > 99:
            dict['name'] = 'wobuxin000' + str(i) + '@yopmail.com'
            dict['passwd'] = 'zxcvbnm'
            dict['nub'] = str(137 + i)
        array.append(dict)
    dictlist['data_list'] = array
    with open(saveRootDirPath + '/' + 'newiphong.json', "w", encoding='utf-8') as json_file:
        json.dump(dictlist, json_file)
