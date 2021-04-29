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
        self.firstequlistButton = QPushButton(u'开始下载', self)
        self.grid.addWidget(self.firstequlistButton, 0, 0)
        # 点击事件
        self.firstequlistButton.clicked.connect(self.handle_Manual)
        # ---------------------------增加到主界面---------------------------
        mainview = QVBoxLayout()
        mainview.addLayout(self.grid)
        self.setLayout(mainview)


    # 手动点击事件
    def handle_Manual(self):
        sender = self.sender()
        clickevent = sender.text()
        global _homeurl, _header, _uid , _currencookie ,_browser ,_wait,_chromedriver ,_waterfall ,_slm ,_qList

        # 6.解密key文件
        def decode_key( seed_const, key_enc):
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
        def get_IV( m3u8contents, g_videoid):
            m3u8content = re.sub(r'URI="([^"]+)"', 'URI="%s"' % (g_videoid + ".key"), m3u8contents, 1, re.M | re.I)
            jiami = re.findall('#EXT-X-KEY:(.*)\n', m3u8content)
            iv = re.findall('IV=(.*)', jiami[0])[0]
            IVV = iv.replace('0x', '')[:16].encode()
            return {'iv': IVV, 'm3u8content': m3u8content}

        # 8.多线程ts视频链接
        def download_all(sites):
            # future列表中每个future完成的顺序，和它在列表中的顺序并不一定完全一致。
            # 到底哪个先完成、哪个后完成，取决于系统的调度和每个future的执行时间
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                to_do = []
                for site in sites:
                    # executor.submit返回future实例
                    future = executor.submit(download_one, site)
                    to_do.append(future)
                    # future.add_done_callback(over)
                # 在futures完成后打印结果
                for future in concurrent.futures.as_completed(to_do):
                    if future.exception() is not None:
                        print(future.exception())
                    else:
                        print(future.result())

        # 8-1.单线程ts视频链接
        def download_one( url):
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
                printProcessBar(sumCount, doneCount, 50)
                succeed = True
            print('Read {} from {}'.format(len(response.content), url))
            return f'download {len(response.content)} ok'

        # 9、合并ts
        def mergeTs( tsFileDir, outputFilePath, cryptor, count):
            global logFile
            outputFp = open(outputFilePath, "wb+")
            for index in range(count):
                printProcessBar(count, index + 1, 50)

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
        def ffmpegConvertToMp4( inputFilePath, ouputFilePath):
            global logFile
            if not os.path.exists(inputFilePath):
                print(inputFilePath + " 路径不存在！")
                return False
            cmd = r'ffmpeg -i "{0}" -vcodec copy -acodec copy "{1}"'.format(inputFilePath, ouputFilePath)
            if os.system(cmd) == 0:
                print(inputFilePath + "转换成功！")
                return True
            else:
                print(inputFilePath + "转换失败！")

                return False

        # 11.删除ts文件
        def removeTsDir( tsFileDir):
            # 先清空文件夹
            for root, dirs, files in os.walk(tsFileDir, topdown=False):

                for name in files:
                    os.remove(os.path.join(root, name))
                # for name in dirs:
                #     print('============')
                #     print(os.path.join(root, name))
                # os.rmdir(os.path.join(root, name))
            # os.rmdir(tsFileDir)
            return True

        # 8、模拟输出进度条
        def printProcessBar( sumCount, doneCount, width):
            precent = doneCount / sumCount
            useCount = int(precent * width)
            spaceCount = int(width - useCount)
            precent = precent * 100
            print('\t{0}/{1} {2}{3} {4:.2f}%'.format(sumCount, doneCount, useCount * '■', spaceCount * '□', precent),
                  file=sys.stdout, flush=True, end='\r')


        def reqeJsonsqq():
            with open(saveRootDirPath + "/" + "课时21：如何准备资产2" + "/" +"/datalist.json") as json_file:
                config = json.load(json_file)
                return config
        def reqeJsonkey():
            with open(saveRootDirPath + '/' + "课时21：如何准备资产2" + '/' + 'key.key', "rb") as json_file:
                return json_file.read()

        def reqeJsonm3u8():
            with open(saveRootDirPath + '/' + "课时21：如何准备资产2" + '/' + 'm3u8.txt',encoding='utf-8') as json_file:
                return json_file.read()

        if clickevent == u'开始下载':
            urlqq = reqeJsonsqq()['cookid'].split(';')[-1].replace('uid=', '')
            m3u8key = reqeJsonkey()
            # 解密key
            if len(m3u8key) == 32:
                print("key length is 32, decoding...")
                m3u8keys = decode_key(urlqq, m3u8key)
            m3u8 = reqeJsonm3u8()
            # 获取iv偏移量
            if len(m3u8) > 0:
                print("key length is 32, decoding...")
                iv_dict = get_IV(m3u8, '9215d654967e9ae76f538e7ef5cce013_1')
                iv = iv_dict['iv']
                m3u8content = iv_dict['m3u8content']

                print(iv)
            if not iv:
                print("get vinfo(%s) information error" % (iv))
                return 0

            cryptor = AES.new(m3u8keys[0], AES.MODE_CBC, iv)  # 解密视频流

            # # 8.多线程ts视频链接
            tslist = re.findall('EXTINF:(.*),\n(.*)\n#', m3u8content)
            newlist = []
            for i in tslist:
                newlist.append(i[1])
            start_time = time.perf_counter()
            download_all(newlist)
            end_time = time.perf_counter()
            print('Download {} sites in {} seconds'.format(len(newlist), end_time - start_time))

            # 9.合并ts
            if mergeTs(cachePath, cachePath + "/cache.flv", cryptor, len(newlist)):
                print("ts合并完成---------------------！")
            else:
                print("ts合并失败---------------------！")
                return False

            # 10.convert to mp4（调用了FFmpeg，将合并好的视频内容放置到一个mp4容器中）
            # _titlename
            # vinfo["title"]
            ffmpegConvertToMp4(cachePath + "/cache.flv", saveRootDirPath + "/" + '课时21：如何准备资产2' + ".mp4")

            # 11.删除ts文件
            removeTsDir(cachePath)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 页面布局
    mainview =mainView()
    mainview.show()

    sys.exit(app.exec_())