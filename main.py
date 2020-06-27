#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2020/06/26 17:20
# @Author  : An Ju
# @Email   : juan_0525@outlook.com
# @File    : main.py

import utils.tools
import utils.db
import utils.downloader
import time
import os
import requests
import sys
import pandas as pd
import sqlite3
import secrets
from openpyxl.workbook import Workbook
from dingtalkchatbot.chatbot import DingtalkChatbot

# WebHook地址
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=这里填写自己钉钉群自定义机器人的token'
secret = 'SEC11b9...这里填写自己的加密设置密钥'  # 创建机器人勾选“加签”选项时使用
# 初始化机器人小丁
xiaoding = DingtalkChatbot(webhook, secret=secret)

# 是否需要测试连接速度 True or False
SpeedTest = False

# 在线预览文件域名 http / https
your_domain = 'https://list.domain.com'

'''
支持检测多个在线.txt文件
# python3 main.py http://a.txt https://b.txt http://c.txt
会保存到/playlists目录中，文件名自动截取为url中最后一个'/'后的所有字符，覆盖同名文件
'''
if len(sys.argv) > 1:
    for i in range(len(sys.argv) - 1):
        url = sys.argv[i + 1]
        name = url.split('/')[-1]
        path = "./playlists/%s" % (name)
        r = requests.get(url)
        r.encoding = 'utf-8'
        with open(path, "wb") as fp:
            fp.write(r.content)


class Iptv(object):
    playlist_file = 'playlists/'
    output_file = 'output/'
    delay_threshold = 5000  # 响应延迟阈值，单位毫秒。超过这个阈值则认为直播源质量较差

    def __init__(self):
        self.T = utils.tools.Tools()
        self.DB = utils.db.DataBase()
        self.now = time.strftime("%Y%m%d_%H%M%S", time.localtime())

    def getPlaylist(self):

        '''
        :return playList:
        #从playlist文件夹读取文件，反馈urlList。
        #目前仅支持txt格式:
        战旗柯南1,http://dlhls.cdn.zhanqi.tv/zqlive/69410_SgVxl.m3u8
        战旗柯南2,http://alhls.cdn.zhanqi.tv/zqlive/219628_O3y9l.m3u8
        '''
        playList = []
        # 读取文件
        path = os.listdir(self.playlist_file)
        for p in path:
            if os.path.isfile(self.playlist_file + p):
                with open(self.playlist_file + p, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total = len(lines)
                    for i in range(0, total):
                        line = lines[i].strip('\n')
                        item = line.split(',', 1)
                        if len(item) == 2:
                            data = {
                                'title': item[0],
                                'url': item[1],
                            }
                            playList.append(data)
        return playList

    def checkPlayList(self, playList):
        '''
        :return: True or False
        验证每一个直播源，记录所有的delay值，超过delay_threshold的记为delay_threshold。
        '''
        total = len(playList)
        if (total <= 0): return False
        for i in range(0, total):
            tmp_title = playList[i]['title']
            tmp_url = playList[i]['url']
            print('Checking[ %s / %s ]:%s' % (i, total, tmp_title))

            netstat = self.T.chkPlayable(tmp_url)
            if 0 < netstat < self.delay_threshold:
                speed = utils.downloader.start(tmp_url) / 1024 / 1024 if SpeedTest else 0
                data = {
                    'title': tmp_title,
                    'url': tmp_url,
                    'delay': netstat,
                    'speed': "%s Mb/s" % "{:.2f}".format(speed) if speed > 0 else "NaN"
                }
                self.addData(data)

            else:
                data = {
                    'title': tmp_title,
                    'url': tmp_url,
                    'delay': self.delay_threshold,
                    'speed': "NaN"
                }
                self.addData(data)

    def addData(self, data):
        self.DB.insert(data)

    @property
    def output(self):
        sql = "SELECT * FROM %s WHERE delay='5000' " % (self.DB.table)
        result = self.DB.query(sql)
        xiaoding.send_text(msg='共检测得 %s 个无效直播源！' % (len(result)), is_at_all=True)
        expired = ''
        for item in result:
            expired += str(item[0]) + '.' + str(item[1]) + ',' + str(item[2]) + '\n'
        xiaoding.send_text(msg=expired, is_at_all=True)
        conn = sqlite3.connect('./database/db.sqlite3')
        conn.cursor()
        sql_cmd = "SELECT * FROM %s" % (self.DB.table)
        df = pd.read_sql(sql_cmd, conn)

        def color_cell(cell):
            if cell == self.delay_threshold:
                return 'background-color: #DC143C'
            elif cell > 3000:
                return 'background-color: #FF1493'
            elif cell > 1000:
                return 'background-color: #FFFF00'
            elif cell > 500:
                return 'background-color: #90EE90'
            else:
                return 'background-color: #008000'
        self.T.mkdir(self.output_file)
        self.T.del_file(self.output_file)
        title = self.now + '_' + secrets.token_urlsafe(16)
        out = (
                df.style
                .set_properties(**{'text-align': 'center'})
                .applymap(color_cell, subset=['delay'])
                .to_excel("./%s/%s.xlsx" % (self.output_file, title), index=False)
        )
       
        if your_domain:
            xiaoding.send_link(title='直播源检测结束！', text='点击查看全部检测结果', message_url='https://view.officeapps.live.com/op/view.aspx?src=%s/IPTV-M3U-Checker-Bot/%s/%s.xlsx' % (your_domain, self.output_file, title))
        else:
            pass
        conn.close()


if __name__ == '__main__':
    iptv = Iptv()
    print('开始......')
    xiaoding.send_text(msg='直播源检测开始！', is_at_all=True)  # is_at_all @所有人
    iptv.checkPlayList(iptv.getPlaylist())
    iptv.output
    print('结束.....')
