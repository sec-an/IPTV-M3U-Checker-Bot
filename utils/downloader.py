#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2020/06/27 00:50
# @Author  : An Ju
# @Email   : juan_0525@outlook.com
# @File    : downloader.py

import time
from urllib.request import urlopen


class Downloader:
    def __init__(self, url):
        self.url = url
        self.startTime = time.time()
        self.receive = 0
        self.endTime = None

    def getSpeed(self):
        if self.endTime and self.receive != -1:
            return self.receive / (self.endTime - self.startTime)
        else:
            return -1


def getStreamUrl(m3u8):
    urls = []
    try:
        prefix = m3u8[0:m3u8.rindex('/') + 1]
        with urlopen(m3u8, timeout=2) as resp:
            top = False
            second = False
            firstLine = False
            for line in resp:
                line = line.decode('utf-8')
                line = line.strip()
                # 不是M3U文件，默认当做资源流
                if firstLine and not '#EXTM3U' == line:
                    urls.append(m3u8)
                    firstLine = False
                    break
                if top:
                    # 递归
                    if not line.lower().startswith('http'):
                        line = prefix + line
                    urls += getStreamUrl(line)
                    top = False
                if second:
                    # 资源流
                    if not line.lower().startswith('http'):
                        line = prefix + line
                    urls.append(line)
                    second = False
                if line.startswith('#EXT-X-STREAM-INF:'):
                    top = True
                if line.startswith('#EXTINF:'):
                    second = True
            resp.close()
    except BaseException as e:
        print('get stream url failed! %s' % e)
    return urls


def downloadTester(downloader: Downloader):
    chunck_size = 10240
    try:
        resp = urlopen(downloader.url, timeout=2)
        # max 5s
        while time.time() - downloader.startTime < 5:
            chunk = resp.read(chunck_size)
            if not chunk:
                break
            downloader.receive = downloader.receive + len(chunk)
        resp.close()
    except BaseException as e:
        print("downloadTester got an error %s" % e)
        downloader.receive = -1
    downloader.endTime = time.time()


def start(url):
    stream_urls = []
    if url.lower().endswith('.flv'):
        stream_urls.append(url)
    else:
        stream_urls = getStreamUrl(url)
    # 速度默认-1
    speed = -1
    if len(stream_urls) > 0:
        stream = stream_urls[0]
        downloader = Downloader(stream)
        downloadTester(downloader)
        speed = downloader.getSpeed()
    return speed
