#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2020/06/26 17:20
# @Author  : An Ju
# @Email   : juan_0525@outlook.com
# @File    : tools.py


import urllib.request
import urllib.parse
import urllib.error
import socket
import time
import os

socket.setdefaulttimeout(5.0)

class Tools (object) :

    def __init__ (self) :
        pass

    def del_file(self,path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                del_file(c_path)
            else:
                os.remove(c_path)

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
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            return True

    def chkPlayable (self, url) :
        try:
            startTime = int(round(time.time() * 1000))
            code = urllib.request.urlopen(url).getcode()
            if code == 200 :
                endTime = int(round(time.time() * 1000))
                useTime = endTime - startTime
                return int(useTime)
            else:
                return 0
        except:
            return 0
