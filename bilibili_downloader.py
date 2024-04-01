import os
import time
import random
import re
import sys
import subprocess
from threading import Thread

import requests
import json
import pickle
import qrcode
from lxml import etree
from PIL import Image
from PySide6.QtWidgets import QHBoxLayout, QTableWidgetItem, QApplication, QMainWindow, QTextBrowser
from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QImage, QPixmap
from ui_main import Ui_Form


class signals(QObject):
    text_print = Signal(QTextBrowser, str)
    text_clear = Signal(QTextBrowser)
    video_list_signal = Signal(dict)

    def __init__(self):
        super().__init__()


sign = signals()


class bilibili_Download(QMainWindow):

    def __init__(self):

        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.login.clicked.connect(self.thread_login)
        self.ui.add_url.clicked.connect(self.thread_add_analyze_url)
        self.ui.download.clicked.connect(self.start_download)
        self.ui.remain_file.clicked.connect(self.remain_file)
        self.ui.openinexplorer.clicked.connect(self.openinexplorer)

        self.table = self.ui.video_list
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 445)
        self.table.setColumnWidth(2, 155)

        sign.text_print.connect(self.printToGui)
        sign.text_clear.connect(self.clearGui)
        sign.video_list_signal.connect(self.input_video_info)

        self.remainfile = False
        self.islogin = False
        self.session = requests.session()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.29',
            'origin': 'https://www.bilibili.com'
        }
        os.makedirs("Bilibili_Output", exist_ok=True)
        self.cookies_dict = self.get_cookies_dict()

        self.cid_url = "https://api.bilibili.com/x/player/pagelist?bvid="
        self.download_list = []
        self.videoCount = -1
        self.mergeQueue = []

        self.thread_merge_video()

    def remain_file(self):
        if self.ui.remain_file.isChecked():
            self.remainfile = True

    def printToGui(self, fb, text):
        fb.append(str(text))
        fb.ensureCursorVisible()

    def clearGui(self, fb):
        fb.clear()

    def isBilibiliUrl(self, url) -> bool:
        '''
        判断是否为B站地址
        :param url: 用户输入的地址
        :return: bool
        '''
        if 'bilibili' in url:
            return True
        else:
            return False  # 非哔哩哔哩链接

    def get_bv_num(self, url):
        try:
            bv = url[url.index("bilibili"):url.index("?")].replace("bilibili.com/video/", "").replace("/", "")
            return bv
        except Exception as e:
            if 'substring' in str(e):
                return None

    def url_bv_ep_detect(self, url):
        if 'video' in url:
            return 'bv'
        elif 'bangumi' in url:
            return 'ep'
        else:
            return None

    def input_video_info(self, dic):
        '''

        :param dic: {'aid', 'bvid','cid', 'epid','name','title','mode','url','num'}
        :return: None
        '''
        row = len(self.download_list) - 1
        sign.text_print.emit(self.ui.info, "[info]导入成功:" + str(dic))
        table = self.table
        layout = QHBoxLayout()
        layout.addWidget(table)
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem('Y'))
        name = str(dic['name'])
        title = str(dic['title'])
        table.setItem(row, 1, QTableWidgetItem(name))
        table.setItem(row, 2, QTableWidgetItem(title))
        self.setLayout(layout)

    @property
    def add_analyze_url(self):
        url = self.ui.video_url_input.toPlainText()

        print(url)
        if self.isBilibiliUrl(url) == False:
            return False  # 非哔哩哔哩链接
        self.headers['referer'] = url
        if self.url_bv_ep_detect(url) is None:
            return False
        if self.url_bv_ep_detect(url) == 'bv':
            bv = self.get_bv_num(url)
            if bv == None:
                sign.text_print.emit(self.ui.info, "[Error]未检测到bv号")
                return None
            cid_url = "https://api.bilibili.com/x/player/pagelist?bvid=" + bv + "&jsonp=jsonp"

            data = self.session.get(cid_url, headers=self.headers).text
            data = json.loads(data)

            avid_url = 'https://api.bilibili.com/x/web-interface/view?cid='
            tree = etree.HTML(self.session.get(url, headers=self.headers).text)
            title = tree.xpath('//*[@id="viewbox_report"]/div[1]/div/h1/text()')[0]

            for i_num in range(0, len(data['data']), 1):
                i = data['data'][i_num]
                avid = \
                    json.loads(
                        self.session.get(avid_url + str(i['cid']) + "&bvid=" + bv, headers=self.headers).text)[
                        'data'][
                        'aid']

                dic = {'aid': avid, 'bvid': bv, 'cid': i['cid'], 'epid': "", 'name': i['part'],
                       'title': title, 'num': i_num
                       }
                dic['mode'] = 'bv'
                dic['url'] = 'http://www.bilibili.com/video/' + str(bv) + "/"
                self.download_list.append(dic)
                sign.video_list_signal.emit(dic)

        if self.url_bv_ep_detect(url) == 'ep':
            data = self.session.get(url, headers=self.headers, cookies=self.cookies_dict).text

            tree = etree.HTML(data)
            ep_data = tree.xpath('//*[@id="__NEXT_DATA__"]/text()')[0]
            ep_data = json.loads(ep_data)
            for i_num in range(0, len(
                    ep_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['seasonInfo'][
                        'mediaInfo'][
                        'episodes']), 1):
                i = ep_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['seasonInfo'][
                    'mediaInfo'][
                    'episodes'][i_num]
                dic = {'aid': i['aid'], 'bvid': i['bvid'], 'cid': i['cid'], 'epid': i['ep_id'],
                       'name': i['playerEpTitle'],
                       'title':
                           ep_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data'][
                               'seasonInfo']['mediaInfo'][
                               'title'], 'num': i_num}
                dic['mode'] = 'ep'
                dic['url'] = 'https://www.bilibili.com/bangumi/play/ep' + str(i['ep_id'])

                self.download_list.append(dic)
                sign.video_list_signal.emit(dic)

    def thread_add_analyze_url(self):
        thread = Thread(target=self.add_analyze_url)
        thread.start()
        self.ui.video_url_input.setText('')

    def start_download(self):
        self.videoCount = len(self.download_list)
        for i in self.download_list:
            self.thread_start_download(i)

    def download(self, dic):
        quality1 = self.ui.quality.currentText()
        params = {
            'avid': dic['aid'],
            'cid': dic['cid'],
            'qn': 80,
            'fnval': '4048'
        }
        if dic['mode'] == 'bv':
            params['bvid'] = dic['bvid']

        playurl = 'https://api.bilibili.com/x/player/wbi/playurl'

        self.headers['referer'] = dic['url'].encode("utf-8").decode("latin1")
        video_name = dic['name']
        sign.text_print.emit(self.ui.info, "[Download]正在下载：" + str(video_name))
        content = self.session.get(playurl, params=params, headers=self.headers, cookies=self.cookies_dict,
                                   timeout=10).content
        js = json.loads(content)

        # quality_num=1
        if quality1 in js['data']['accept_description']:
            quality_num = js['data']['accept_description'].index(quality1)
        else:
            quality_num = 0

        quality = js['data']['accept_quality'][quality_num]
        audio_url = js['data']['dash']['audio'][0]['baseUrl']
        video_url = js['data']['dash']['video'][0]['baseUrl']
        num = js['data']['dash']['video'][0]['id']
        for i in js['data']['dash']['video']:
            if i['id'] == quality:
                num = i['id']
                video_url = i['baseUrl']

                sign.text_print.emit(self.ui.info, "[Download]正在下载：" + js['data']['accept_description'][
                    quality_num] + "...")
                break
        if self.islogin == False:
            sign.text_print.emit(self.ui.info, "[Download]未登录，默认下载360P" + "...")
            sign.text_print.emit(self.ui.info, "[Download]正在下载：" + '360P' + "...")

        try:
            sign.text_print.emit(self.ui.info, "[Download]正在下载视频")
            video_data = self.session.get(video_url, headers=self.headers, timeout=10).content
            sign.text_print.emit(self.ui.info, "[Download]正在下载音频")

            audio_data = self.session.get(audio_url, headers=self.headers, timeout=10).content
        except requests.exceptions.ConnectionError as e:
            if '远程主机强迫关闭了一个现有的连接' in e:
                sign.text_print.emit(self.ui.info, "[Error]请求频次过多，请稍后再试试")

        path = str(self.validateTitle(dic['title']))[0:32].replace(" ", '').replace(".", "")
        os.makedirs("./Bilibili_Output/" + path, exist_ok=True)
        with open('./Bilibili_Output/' + path + '/' + str(dic['num']) + "_video.mp4", "wb") as f:
            f.write(video_data)
            f.close()
            sign.text_print.emit(self.ui.info, "[Download]视频文件下载完成")

        with open('./Bilibili_Output/' + path + '/' + str(dic['num']) + "_audio.mp4", "wb") as f:
            f.write(audio_data)
            f.close()
            sign.text_print.emit(self.ui.info, "[Download]音频文件下载完成")
        sign.text_print.emit(self.ui.info, "[Download]已添加至合并音视频队列,等待合并...")

        file_location = os.getcwd()

        video_name = self.validateTitle(str(video_name)).replace(" ", "").replace("_", "")
        quality_name = str(js['data']['accept_description'][quality_num]).replace(" ", "")
        outfile_name = file_location + "/Bilibili_Output/" + path + "/" + video_name + "_" + quality_name + '.mp4'
        if os.path.exists(outfile_name):
            os.remove(outfile_name)
        mergetask = {
            'outfile_name': str(outfile_name),
            'file_location': file_location,
            'path': path,
            'bvid': str(dic['bvid']),
            'title': str(dic['title']),
            'num': str(dic['num'])
        }
        self.mergeQueue.append(mergetask)

    def thread_start_download(self, dic):

        thread = Thread(target=self.download, args=(dic,))
        thread.start()

    def detectmergeQueue(self):
        while 1:
            if self.videoCount == 0:
                sign.text_print.emit(self.ui.info, "[info]全部音视频合成任务已结束...")

                break
            elif len(self.mergeQueue) == 0:
                time.sleep(0.5)
            else:
                try:
                    self.merge_video(self.mergeQueue[0])
                except Exception as e:
                    print(e)
                self.mergeQueue.pop(0)
                self.videoCount -= 1

    def merge_video(self, mergetask):
        '''
        合并音视频 单线程阻塞
        :param mergetask：{
                'outfile_name':输出文件名,
                'file_location':音视频地址,mergetask['title']
                'path':合并路径,
                'bvid':视频bvid,
                'title':视频名.
                'num':视频编号
            }
        '''
        GPUAccelsParam = '-hwaccel auto'
        sign.text_print.emit(self.ui.info, "[Download]正在合并：" + mergetask['outfile_name'])
        subprocess.call(
            mergetask[
                'file_location'] + '/ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe ' + GPUAccelsParam + ' -i ' +
            mergetask['file_location'] + "/Bilibili_Output/" + mergetask['path'] + '/' + str(
                mergetask['num']) + "_video.mp4"
            + ' -i ' + mergetask['file_location'] + '/Bilibili_Output/' + mergetask['path'] + '/' + str(
                mergetask['num']) + "_audio.mp4" + ' -strict -2 -f mp4 '
            + mergetask['outfile_name'], shell=True)
        if not self.remainfile:
            os.remove(mergetask['file_location'] + "/Bilibili_Output/" + mergetask['path'] + '/' + str(
                mergetask['num']) + "_video.mp4")
            os.remove(mergetask['file_location'] + '/Bilibili_Output/' + mergetask['path'] + '/' + str(
                mergetask['num']) + "_audio.mp4")

        sign.text_print.emit(self.ui.info, "[Download]音视频合并成功:" + str(mergetask['outfile_name']))

    def thread_merge_video(self):
        thread = Thread(target=self.detectmergeQueue)
        thread.start()

    def get_cookies_dict(self):
        if os.path.exists("./Bilibili_Output/cookies.pkl"):
            cookies = pickle.load(open("./Bilibili_Output/cookies.pkl", "rb"))

            try:
                if cookies['SESSDATA'] != "":
                    self.islogin = True
                    sign.text_print.emit(self.ui.info, "[info]已登录")
            except Exception as e:
                print(e)
                self.islogin = False
                sign.text_print.emit(self.ui.info, "[info]当前未登录，登录享高清画质")

        else:
            self.islogin = False
            cookies = self.get_cookies()  # 返回未登录
            sign.text_print.emit(self.ui.info, "[info]当前未登录，登录享高清画质")
        return cookies

    def get_ep_video_url(self, url):

        headers = {
            'referer': url,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.29',
            'origin': 'https://www.bilibili.com'
        }

        data = self.session.get(url, headers=headers, cookies=self.cookies_dict).text
        tree = etree.HTML(data)
        ep_data = tree.xpath('//*[@id="__NEXT_DATA__"]/text()')[0]
        '''''with open("ep_url.json", "w", encoding='utf-8') as f:
            f.write(ep_data)
            f.close()
        ep_data = json.loads(ep_data)'''
        ep_list = []
        for i in ep_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['mediaInfo'][
            'episodes']:
            ep = {'aid': i['aid'], 'bvid': i['bvid'], 'cid': i['cid'], 'epid': i['ep_id'], 'name': i['share_copy'],
                  'title': ep_data['props']['pageProps']['dehydratedState']['queries'][0]['state']['data']['mediaInfo'][
                      'title']}
            ep_list.append(ep)

        return ep_list

    def validateTitle(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|【】!?；.：。，？！%……（）、·\[\]~']"
        new_title = re.sub(rstr, "_", title)
        return new_title

    def openinexplorer(self):
        path = str(os.getcwd() + r"\\Bilibili_Output\\")
        os.startfile(path)

    
    def login(self):

        qrcode_key = self.get_qrcode()
        cookies = self.detect_state(qrcode_key)
        if cookies != "":
            self.cookies_dict.update(cookies)
            pickle.dump(self.cookies_dict, open("./Bilibili_Output/" + "cookies.pkl", "wb"))
            return cookies
        else:
            sign.text_print.emit(self.ui.info, "[info]获取Cookies失败，点击登录按钮重试")
            
    def thread_login(self):
        thread = Thread(target=self.login)
        thread.start()

    def get_qrcode(self):
        data = self.session.get(
            'https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header',
            headers=self.headers).text
        content = json.loads(data)
        qrcode_key = content['data']['qrcode_key']
        img = qrcode.make(content['data']['url'])
        img.save('qrcode.png')
        img = Image.open("qrcode.png")
        img = img.resize((181, 181))
        img.save('qrcode.png')
        frame = QImage('qrcode.png')
        pix = QPixmap.fromImage(frame)
        scene = self.ui.qrcode  # 创建场景
        scene.setPixmap(pix)

        return qrcode_key

    def detect_state(self, qrcode_key):
        url = ''
        while True:
            sign.text_clear.emit(self.ui.state)
            data = self.session.get(
                'https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key=' + qrcode_key + '&source=main-fe-header',
                headers=self.headers)
            content = json.loads(data.text)
            message = content['data']['message']

            if content['data']['url'] != '':
                dic = requests.utils.dict_from_cookiejar(data.cookies)
                sign.text_print.emit(self.ui.state, "登录成功")
                return dic
            sign.text_print.emit(self.ui.state, message)
            if message == '二维码已失效':
                qrcode_key = self.get_qrcode()

            time.sleep(2)

    def make_cookies(self):
        def o(e):
            emilisecond = int(e) + 1
            t = str(hex(emilisecond)).replace("0x", "").upper()
            return str(t)

        def a(e):
            t = ""
            for i in range(0, e, 1):
                t = str(t) + o(16 * random.random())
            return s(t, e)

        def s(e, t):
            r = ""
            if len(e) < t:
                for i in range(0, t - len(e), 1):
                    r += "0"
            return r + e

        def get_uuid():
            e = a(8)
            t = a(4)
            r = a(4)
            n = a(4)
            o = a(12)
            i = int(time.time() * 1000)
            return e + "-" + t + "-" + r + "-" + n + "-" + o + s(str(i % 100000), 5) + "infoc"

        b_lsid = a(8) + "_" + o(time.time() * 1000)

        _uuid = get_uuid()
        dic = {'b_lsid': b_lsid, '_uuid': _uuid}
        return dic

    def get_cookies(self):
        # get buvid3 b_nut b_ut
        cookie_dict = {}
        data = self.session.get("http://www.bilibili.com", headers=self.headers)
        cookies = requests.utils.dict_from_cookiejar(data.cookies)
        cookie_dict['buvid3'] = cookies['buvid3']
        cookie_dict['b_nut'] = cookies['b_nut']
        cookie_dict['b_ut'] = cookies['b_ut']

        # get
        data = self.session.get('https://api.bilibili.com/x/frontend/finger/spi', headers=self.headers).text
        # cookies = requests.utils.dict_from_cookiejar(data.cookies)
        dic = json.loads(data)
        cookie_dict['buvid3'] = dic['data']['b_3']
        cookie_dict['buvid4'] = dic['data']['b_4']

        dic = self.make_cookies()
        cookie_dict['b_lsid'] = dic['b_lsid']
        cookie_dict['_uuid'] = dic['_uuid']

        cookie_dict['home_feed_column'] = '4'
        cookie_dict['browser_resolution'] = '1067-616'
        cookie_dict['header_theme_version'] = 'CLOSE'
        cookie_dict['CURRENT_FNVAL'] = '4048'
        rpdid = '''|(k|~YuJl|Y|0J'uYm|Rlmlml'''
        cookie_dict['rpdid'] = rpdid
        cookie_dict['PVID'] = '2'

        return cookie_dict


app = QApplication([])
bd = bilibili_Download()
bd.show()
app.exec()
sys.exit(app.exec())

'https://www.bilibili.com/bangumi/play/ep199612?theme=movie'
