#!/usr/bin/python3.7
# -*- coding: UTF-8 -*-
# @project :PythonStudy shikee
# @name :gan
# @Time :2021/1/28/10:28
#!/usr/bin/env python
#coding=utf8

import concurrent.futures
import time
import os, sys
import hashlib, binascii
import re, json, base64
from Crypto.Cipher import AES
import requests
from bs4 import BeautifulSoup
import re
import lxml
######################配置信息##########################
# 视频保存路径
saveRootDirPath = os.path.abspath('.') + "/output"
#######################################################
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
# 用户uid
_uid = ''
# url
_homeurl = ''
# 头部信息
_header = ''
# 标题
_titleName = ''
# =============================================================

BS = AES.block_size  # 这个等于16
mode = AES.MODE_CBC
pad = lambda s: s + (BS-len(s))*"\0"  # 用于补全key
# 用于补全下面的text，上面两个网址就是用以下形式补全的
pad_txt = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-s[-1]]

# get请求数据
def urlget(url,header) :
    response = requests.get(url, headers = header)
    return response.content.decode('utf-8')

# post请求数据
def urlpost(url, postdata, header) :
    response = requests.post(url, postdata, headers = header)
    return response.content.decode('utf-8')

# 0.创建本地存储目录
def mkdir(path):
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

        print (path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False

# 1.读取本地JSON数据,全局赋值
def reqeJson():
    with open(saveRootDirPath + "/content.json") as json_file:
        config = json.load(json_file)
        homeurl = config['url']
        header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            'Cookie': config['Cookie']}
        uid = config['uid']
    return {'homeurl':homeurl,'header':header,'uid':uid}

#2.请求vid
def getVid(url):
    if ('lib' in url):
        libvid = url[url.rindex('vid=') + 1:].replace('id=','')
        return libvid
    libvid = url[url.rindex('v_') + 1:].replace('_','').replace('.html','')
    return libvid

#3.请求videoid
def getVideoid(vid,url):
    if ('lib' in url):
        libvideo = 'https://www.yiihuu.com/get_yhdesigner_video_uri.php?video_type=xhtml&play_video_id=' + vid  + '&uid=' + _uid
        content = urlget(libvideo, _header).strip()
        info_enc = json.loads(content)
        subcon= info_enc["url"]
        if '.mp4' in subcon:
            dowloadMP4(subcon,url)
            return 0
            # sys.exit(0)
        subcontent = subcon[0:-14]
        return subcontent
    libvideo = 'https://www.yiihuu.com/get_video_uri.php?video_type=xhtml&play_video_id=' + vid
    content = urlget(libvideo, _header).strip()
    if '.mp4' in content:
        dowloadMP4(content,url)
        # sys.exit(0)
        return 0
    subcontent = content[0:-11]
    return subcontent

#3.当前是MP4，则下载完成够退出程序
def dowloadMP4(url,homeurl):
    # 获取标题
    req_obj = requests.get(homeurl)
    req_obj.encoding = req_obj.apparent_encoding
    soup = BeautifulSoup(req_obj.text, 'html.parser')
    # titleName = soup.find(attrs={"name": "keywords"})['content']
    response = requests.get(url,stream = True)
    if response.status_code == 200:
        outputFp = open(saveRootDirPath + '/' + _titleName + '.mp4', "wb+")
        outputFp.write(response.content)
        print('下载完成')
        return 0
#4.请求body
def vidinfo(g_videoid) :
    url = 'https://player.polyv.net/secure/' + g_videoid + '.json'
    content = urlget(url,_header).strip()
    if not content :
        return None
    info_enc = json.loads(content)
    if int(info_enc["code"]) != 200 :
        print(info_enc)
        return None
    body = info_enc["body"]
    # 4-1.解密返回的JSON数据
    info = json.loads(videoinfo_decrypt(g_videoid, body))
    return {"m3u8": info["hls"][-1], "seed_const": info["seed_const"],"title":info["title"]}


# 4-1.解密返回的JSON数据
def videoinfo_decrypt(vid, body) :
    # print("vid: " + _vid)
    hash = hashlib.md5()
    hash.update(vid.encode('utf-8'))
    str = hash.hexdigest()
    # print("vid md5: " + _str)
    key = str[0 : 16]
    iv = str[16 : ]
    # print("key: " + _key + " iv: " + _iv)
    body_raw = binascii.a2b_hex(body)
    cryptor = AES.new(key.encode('utf-8'), mode, iv.encode('utf-8'))
    ret = base64.b64decode(unpad(cryptor.decrypt(body_raw))).decode('utf-8')
    return ret

# 5.m3u8key文件获取
def get_m3u8Key(m3u8,vid):
    m3u8content = urlget(m3u8, _header)
    if not m3u8content:
        print("get m3u8(%s) error" % (m3u8))
        return 0
    rem = re.search(r'URI="([^"]+)"', m3u8content, re.M | re.I)
    if not rem:
        print("m3u8 key url not found")
        return 0
    # 5-1请求token
    m3u8keyurl = rem.group(1).strip() + "?token=" + get_playsafe_token(vid)
    m3u8keyurl = re.sub(r'://([^/]+)/', r'://\1/playsafe/', m3u8keyurl, 1, re.I)
    m3u8key = requests.get(m3u8keyurl).content

    return {'m3u8key':m3u8key,'m3u8content':m3u8content}

# 5-1请求token
def get_playsafe_token(_vid) :
    # // 保利威视自定义参数存视频id和专辑id, 随机对应id
    _url = 'https://www.yiihuu.com/polyv/polyv_get_token.php?vid=' + _vid
    _content = urlget(_url,_header).strip()
    return _content

# 6.解密key文件
def decode_key(seed_const, key_enc) :
    m = hashlib.md5()
    strseed_const = str(seed_const)
    seed_md5 = strseed_const.encode(encoding='utf-8')
    m.update(seed_md5)
    str_md5 = m.hexdigest()
    aeskey = str_md5[0: 16]
    aesiv = b'\x01\x02\x03\x05\x07\x0B\x0D\x11\x13\x17\x1D\x07\x05\x03\x02\x01'
    cryptor = AES.new(aeskey.encode('utf-8'), AES.MODE_CBC,aesiv)
    plain_text = (cryptor.decrypt(key_enc))
    ret = re.findall(b"[\s\S]{16}", plain_text)  # 就是这里需要做小小的改造，看仔细哦
    return ret


# 7.获取iv偏移量
def get_IV(m3u8contents,g_videoid):

    m3u8content = re.sub(r'URI="([^"]+)"', 'URI="%s"' %(g_videoid + ".key"), m3u8contents, 1, re.M | re.I)
    jiami = re.findall('#EXT-X-KEY:(.*)\n', m3u8content)
    iv = re.findall('IV=(.*)', jiami[0])[0]
    IVV = iv.replace('0x', '')[:16].encode()
    return {'iv':IVV,'m3u8content':m3u8content}


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
def download_one(url):
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
def mergeTs(tsFileDir, outputFilePath, cryptor, count):
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
def ffmpegConvertToMp4(inputFilePath, ouputFilePath):
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
def removeTsDir(tsFileDir):
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
def printProcessBar(sumCount, doneCount, width):
    precent = doneCount / sumCount
    useCount = int(precent * width)
    spaceCount = int(width - useCount)
    precent = precent*100
    print('\t{0}/{1} {2}{3} {4:.2f}%'.format(sumCount, doneCount, useCount*'■', spaceCount*'□', precent), file=sys.stdout, flush=True, end='\r')



def main(argc, argv,dictData) :

    url = dictData['url']
    title = dictData['title']
    # 2.请求vid
    vid = getVid(url)
    if not vid :
        print("get vid(%s) information error" %(vid))
        return 0

    # 3.请求videoid
    g_videoid = getVideoid(vid,url)
    if not g_videoid :
        print("get g_videoid(%s) information error" %(g_videoid))
        return 0

    # 4.请求body
    vinfo = vidinfo(g_videoid)
    if not vinfo :
        print("get vinfo(%s) information error" %(vinfo))
        return 0

    # 5.请求m3u8key
    m3u8keyDict = get_m3u8Key(vinfo["m3u8"],vid)
    m3u8key = m3u8keyDict['m3u8key']

    # 6.解密key
    if len(m3u8key) == 32 :
        print("key length is 32, decoding...")
        m3u8key = decode_key(vinfo["seed_const"], m3u8key)

    # 7.获取iv偏移量
    iv_dict =   get_IV(m3u8keyDict['m3u8content'],g_videoid)
    iv = iv_dict['iv']
    m3u8content = iv_dict['m3u8content']

    if not iv :
        print("get vinfo(%s) information error" %(iv))
        return 0
    cryptor = AES.new(m3u8key[0], AES.MODE_CBC, iv)  # 解密视频流

    # 8.多线程ts视频链接
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
    ffmpegConvertToMp4(cachePath + "/cache.flv", saveRootDirPath + "/" + title + ".mp4")

    # 11.删除ts文件
    removeTsDir(cachePath)

    return 0

if __name__ == "__main__" :

    # 0.创建本地存储目录
    mkdir(cachePath)
    # 1.读取本地JSON数据,全局赋值
    itemDict = reqeJson()
    _homeurl = itemDict['homeurl']
    _header = itemDict['header']
    _uid = itemDict['uid']

    soup = BeautifulSoup(open(saveRootDirPath + '/home.html', encoding="utf-8",), 'html.parser')
    title = str(soup.head.title)

    flag = False
    array = []
    if (title.find('翼狐设计学习库')>=0):
        flag = True
        # @lib
        html = soup.find_all('a', class_='f-toe w220')
        array = []
        for href in html:
            title = href.get('title')
            url = 'https:' + href.get('href')
            dict = {}
            dict['title'] = title
            dict['url'] = url
            array.append(dict)
    else:
        html = soup.find_all('li', class_='normal list_num')
        for href in html:
            eq_url = 'https:' +href.a.get('href')
            title = href.a.get('title')
            dict = {}
            dict['title'] = title
            dict['url'] = eq_url
            array.append(dict)

    for dictData in array:
       _titleName = dictData['title']
       main(len(sys.argv), sys.argv,dictData)

    # for dictData in range(len(array)):
    #
    #     if dictData >111:
    #         if dictData < 119:
    #           # print(dictData)
    #           _titleName = array[dictData]['title']
    #           main(len(sys.argv), sys.argv,array[dictData])

    # for dictData in range(len(array)):
    #         if dictData ==12:
    #           # print(dictData)
    #           _titleName = array[dictData]['title']
    #           main(len(sys.argv), sys.argv,array[dictData])




