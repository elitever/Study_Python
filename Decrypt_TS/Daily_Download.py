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

global _homeurl, _header, _uid , _currencookie ,_browser ,_wait ,_chromedriver ,_username ,_password ,_waterfall ,_slm ,_qList,_PathtitleNme

# 页面布局
class mainView(QWidget):

    def __init__(self):
        super(mainView, self).__init__()
        self.setWindowTitle("每日免费下载")
        # ---------------------------表单布局---------------------------
        self.grid=QGridLayout()
        # -------------------第一行---------------------
        self.firstvidolistLabel=QLabel("视频列表地址")
        self.firstvidolistEdit = QLineEdit('https://www.yiihuu.com/v_180499.html')
        self.firstequlistButton = QPushButton(u'0.读取目录文件（一套课程点击一遍）', self)
        self.grid.addWidget(self.firstvidolistLabel,1,0)
        self.grid.addWidget(self.firstvidolistEdit,1,1)
        self.grid.addWidget(self.firstequlistButton, 1, 2)
        # -------------------第二行---------------------
        self.secondbeginLabel = QLabel("从第几集开始")
        self.secondbeginEdit = QLineEdit('67')
        self.secondbeginaccountButton = QPushButton(u'1.获取账号密码网页', self)
        self.grid.addWidget(self.secondbeginLabel,2,0)
        self.grid.addWidget(self.secondbeginEdit,2,1)
        self.grid.addWidget(self.secondbeginaccountButton, 2, 2)
        # -------------------第三行---------------------
        self.thirdQQLabel = QLabel("从第几个QQ开始")
        self.thirdQQEdit = QLineEdit('42')
        self.thirdopenchromeButton = QPushButton(u'2.打开浏览器', self)
        self.grid.addWidget(self.thirdQQLabel,3,0)
        self.grid.addWidget(self.thirdQQEdit,3,1)
        self.grid.addWidget(self.thirdopenchromeButton, 3, 2)
        # -------------------第四行---------------------
        self.fourthcopyxLabel = QLabel("复制的x轴")
        self.fourthcopyxEdit = QLineEdit('850')
        self.fourthfillButton = QPushButton(u'3.手动填入QQ和密码', self)
        self.grid.addWidget(self.fourthcopyxLabel,4,0)
        self.grid.addWidget(self.fourthcopyxEdit,4,1)
        self.grid.addWidget(self.fourthfillButton, 4, 2)
        # -------------------第五行---------------------
        self.fivecopyyLabel = QLabel("复制的y轴")
        self.fivecopyyEdit = QLineEdit('130')
        self.fiveupdatacookieButton = QPushButton(u'4.手动更新cookie', self)
        self.grid.addWidget(self.fivecopyyLabel,5,0)
        self.grid.addWidget(self.fivecopyyEdit,5,1)
        self.grid.addWidget(self.fiveupdatacookieButton, 5, 2)
        # -------------------第六行---------------------
        self.sixthusernameLabel = QLabel("qq号码")
        self.sixthusernameEdit = QLineEdit()
        self.sixthdowloadButton = QPushButton(u'5.手动开始下载', self)
        self.grid.addWidget(self.sixthusernameLabel,6,0)
        self.grid.addWidget(self.sixthusernameEdit,6,1)
        self.grid.addWidget(self.sixthdowloadButton,6, 2)
        # -------------------第七行---------------------
        self.seventhpasswdLabel = QLabel("qq密码")
        self.seventhpasswdEdit = QLineEdit()
        self.seventhemptyButton = QPushButton(u'清空', self)
        self.grid.addWidget(self.seventhpasswdLabel,7,0)
        self.grid.addWidget(self.seventhpasswdEdit,7,1)
        self.grid.addWidget(self.seventhemptyButton, 7, 2)
        # -------------------第八行---------------------
        self.eighthviderulLabel = QLabel("视频地址")
        self.eighthviderulEdit = QLineEdit()
        self.eighthdowloadButton = QPushButton(u'全流程自动', self)
        self.grid.addWidget(self.eighthviderulLabel,8,0)
        self.grid.addWidget(self.eighthviderulEdit,8,1)
        self.grid.addWidget(self.eighthdowloadButton, 8, 2)
        # -------------------第九行---------------------
        self.ninthcookieLabel = QLabel("cookie")
        self.ninthcookieEdit = QLineEdit()
        self.ninthcopyButton = QPushButton(u'复制视频', self)
        self.grid.addWidget(self.ninthcookieLabel,9,0)
        self.grid.addWidget(self.ninthcookieEdit,9,1)
        self.grid.addWidget(self.ninthcopyButton, 9, 2)
        # -------------------第十行---------------------
        self.tenthcoordinatesButton = QPushButton(u'获取坐标', self)
        self.grid.addWidget(self.tenthcoordinatesButton, 10, 2)

        # 点击事件
        self.firstequlistButton.clicked.connect(self.handle_Manual)
        self.secondbeginaccountButton.clicked.connect(self.handle_Manual)
        self.thirdopenchromeButton.clicked.connect(self.handle_Manual)
        self.fourthfillButton.clicked.connect(self.handle_Manual)
        self.fiveupdatacookieButton.clicked.connect(self.handle_Manual)
        self.sixthdowloadButton.clicked.connect(self.handle_Manual)
        self.seventhemptyButton.clicked.connect(self.handle_Manual)
        self.eighthdowloadButton.clicked.connect(self.handle_Manual)
        self.ninthcopyButton.clicked.connect(self.handle_Manual)
        self.tenthcoordinatesButton.clicked.connect(self.handle_Manual)

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
        # 账号
        self.sixthusernameEdit.setText(array[1])
        _username = self.sixthusernameEdit.text()
        # 密码
        self.seventhpasswdEdit.setText(array[2])
        _password = self.seventhpasswdEdit.text()
        # 下载的地址
        self.eighthviderulEdit.setText(array[3])
    # 手动点击事件
    def handle_Manual(self):
        sender = self.sender()
        clickevent = sender.text()
        global _homeurl, _header, _uid , _currencookie ,_browser ,_wait,_chromedriver ,_waterfall ,_slm ,_qList

        if clickevent == u'0.读取目录文件（一套课程点击一遍）':
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
        elif clickevent == u'1.获取账号密码网页':
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
        elif clickevent == u'2.打开浏览器':
            # get直接返回，不再等待界面加载完成
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["pageLoadStrategy"] = "none"
            # # Mac系统
            # _browser = webdriver.Chrome()
            # windows系统
            _chromedriver = "C:\chromedriver.exe"  # 这里写本地的chromedriver 的所在路径
            # os.environ["webdriver.Chrome.driver"] = chromedriver  # 调用chrome浏览器
            _browser = webdriver.Chrome(_chromedriver)
            _wait = WebDriverWait(_browser, 50, 0.5)
            _homeurl = self.eighthviderulEdit.text()
            _browser.get(_homeurl)
        elif clickevent == u'3.手动填入QQ和密码':
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
        elif clickevent == u'4.手动更新cookie':

            _browser.get(self.eighthviderulEdit.text())
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
            self.ninthcookieEdit.setText(_currencookie)
        elif clickevent == u'5.手动开始下载':
            _homeurl = self.eighthviderulEdit.text()
            _header = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
                'Cookie': _currencookie}
            # 开始下载
            manual_main.dowloadbegin()
            _browser.quit()
            # reply = QMessageBox.information(self, '下载成功', '下载成功')
        elif clickevent == u'清空':
            self.secondbeginEdit.setText('0')
            self.thirdQQEdit.setText('0')
            self.fourthcopyxEdit.setText('')
            self.fivecopyyEdit.setText('')
            self.sixthusernameEdit.setText('')
            self.seventhpasswdEdit.setText('')
            self.eighthviderulEdit.setText('')
            self.ninthcookieEdit.setText('')
            _slm.setStringList([])  # 将数据设置到model
        elif clickevent == u'全流程自动':
            _homeurl = self.eighthviderulEdit.text()
            # get直接返回，不再等待界面加载完成
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["pageLoadStrategy"] = "none"
            # Mac系统
            _browser = webdriver.Chrome()
            # windows系统
            # _chromedriver = "C:\chromedriver.exe"  # 这里写本地的chromedriver 的所在路径
            # # os.environ["webdriver.Chrome.driver"] = chromedriver  # 调用chrome浏览器
            # _browser = webdriver.Chrome(_chromedriver)
            _wait = WebDriverWait(_browser, 50, 0.5)
            _browser.get(_homeurl)
            # 开始下载
            automatic_main.automatic_dowloadbegin()
        elif clickevent == u'复制视频':
            # 右击该坐标点
            pyautogui.leftClick(int(self.fourthcopyxEdit.text()), int(self.fivecopyyEdit.text()))
            pyautogui.hotkey('ctrl', 'c')
        elif clickevent == u'获取坐标':
             #右击获取坐标点
             pyautogui.rightClick(int(self.fourthcopyxEdit.text()), int(self.fivecopyyEdit.text()))

# 手动下载函数
class Manual_main():

    global _homeurl, _header, _uid , _currencookie ,_browser ,_wait ,_chromedriver ,_username ,_password

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
            # 1.创建目录
            self.mkdir(saveRootDirPath + '/' + titleName)
            datadict = {}
            datadict['cookid'] = 'cookie'
            datadict['homeurl'] = _homeurl
            datadict['videourl'] = url
            datadict['title'] = titleName
            with open(saveRootDirPath + '/' + titleName + '/' + 'datalist.json', "w", encoding='utf-8') as json_file:
                json.dump(datadict, json_file)

            # outputFp = open(saveRootDidatadictrPath + '/' + titleName + '.mp4', "wb+")
            # outputFp.write(response.content)
            # print('下载完成')

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
        # 1.创建目录
        self.mkdir(saveRootDirPath + '/' + info["title"])
        datadict = {}
        datadict['cookid'] = _currencookie + 'uid=' + str(info["seed_const"])
        datadict['homeurl'] = _homeurl
        datadict['videourl'] = ''
        datadict['title'] = info["title"]
        with open(saveRootDirPath + '/' + info["title"] + '/' + 'datalist.json', "w", encoding='utf-8') as json_file:
            json.dump(datadict, json_file)
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
    def get_m3u8Key(self,m3u8, vid,titleNmae):

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

        outputFp = open(saveRootDirPath + '/' + titleNmae + '/' + 'key.key', "wb+")
        outputFp.write(m3u8key)

        with open(saveRootDirPath + '/' + titleNmae + '/' + 'm3u8.txt', "w", encoding='utf-8') as json_file:
            json.dump(m3u8content, json_file)
        return {'m3u8key': m3u8key, 'm3u8content': m3u8content}

    # 5-1请求token
    def get_playsafe_token(self,_vid):
        # // 保利威视自定义参数存视频id和专辑id, 随机对应id
        _url = 'https://www.yiihuu.com/polyv/polyv_get_token.php?vid=' + _vid
        _content = self.urlget(_url, _header).strip()
        return _content


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
            return 0

        # 5.请求m3u8key
        self.get_m3u8Key(vinfo["m3u8"], vid,vinfo["title"],)

        return 0
# 自动下载
class Automatic_main():

    global _homeurl, _header, _uid, _currencookie, _browser, _wait, _chromedriver, _username, _password

    def automatic_dowloadbegin(self):

        # 打开登录按钮
        login_btn = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_u-login"]/div/a[1]')))
        login_btn.click()


        # 切换登陆弹框
        J_iframe = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_iframe"]')))
        _browser.switch_to.frame(J_iframe)

        # 等待时间
        time.sleep(random.random() * 3)

        # 点击QQ登陆按钮
        loginQQ_btn = _wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/ul/li[1]/a')))
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
                ptlogin_iframe = _wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ptlogin_iframe"]')))
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

        return 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 页面布局
    mainview =mainView()
    mainview.show()
    # 手动下载函数
    manual_main = Manual_main()
    # 自动下载函数
    automatic_main = Automatic_main()

    sys.exit(app.exec_())