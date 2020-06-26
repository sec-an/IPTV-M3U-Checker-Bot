# IPTV-M3U-Checker 直播源批量检测程序

## 简介

Python初学者，能力有限，还请见谅。

本项目改自[AlexKwan1981 / iptv-m3u8-checker](https://github.com/AlexKwan1981/iptv-m3u8-checker "AlexKwan1981 / iptv-m3u8-checker")，感谢！

增加了[钉钉群机器人](https://ding-doc.dingtalk.com/doc#/serverapi2/krgddi)，可以配合定时任务，实现直播源的定时检测与通知。

基于个人能力和`.m3u`文件自身标签的原因，暂时删除了对`.m3u`文件的支持（原项目也不完全支持），目前仅支持`.txt`直播源的检测。（有许多在线工具/软件能较好地将`.m3u`转为`.txt`）

### 主要功能
对直播源进行批量检测，并通过钉钉群机器人及时反馈检测结果。
- 将待检测的直播源文件放置到playlists文件夹下：  
  - 支持在线直链（可添加多个），自动下载至playlists文件夹，文件名相同则直接覆盖（类似自动更新）
  - 支持多个本地文件
  - 目前仅支持`.txt`格式，详见playlists文件下的示例
- 直播源检测
  - 对每个连接进行测试, 同时记录当前网络对该连接的延迟（参考[EvilCult/iptv-m3u-maker](https://github.com/EvilCult/iptv-m3u-maker)）  
  - 将失效的直播源以文本形式通过钉钉群机器人通知
  - 通过DataFrame.to_html()在同目录下生成[html_demo](https://api.juan0110.top/IPTV-M3U-Checker/status.html)，以链接形式通过钉钉群机器人发送

## 使用方法

本项目基于 **python3.7** 进行开发 

- 模块安装 Requirements
```
pip3 install pandas
pip3 install requests
pip3 install DingtalkChatbot

* 国内可以使用-i参数加快下载速度
如：pip3 install DingtalkChatbot -i https://pypi.tuna.tsinghua.edu.cn/simple
```

- 主要参数  
  - webhook 填入钉钉群自定义机器人的token
  ```
  修改main.py第19行
  webhook = 'https://oapi.dingtalk.com/robot/send?access_token=这里填写自己钉钉群自定义机器人的token'
  ```
  - secret 创建机器人勾选“加签”选项所设置的密钥
  ```
  修改main.py第20行
  secret = 'SEC11b9...这里填写自己的加密设置密钥'  # 创建机器人勾选“加签”选项时使用
  ```
  - playlist_file = 'playlists/' 
  直播源源文件存放路径
  - delay_threshold = 5000  
  响应延迟阈值，单位毫秒，超过这个阈值则认为直播源质量较差
  - your_domain 如果有服务器，则填入域名/IP
  ```
  修改main.py第125行message_url
  xiaoding.send_link(title='直播源检测结束！', text='点击查看全部检测结果', message_url='https://your_domain/IPTV-M3U-Checker/status.html')

  如果没有/不需要，注释该行即可
  ```
- 运行
```
只检测本地文件：python3 main.py
检测直链文件：python3 main.py http://a.txt https://b.txt http://c.txt

* 检测直链时，自动下载至playlists/，而后检测该目录下所有文件
```

## 注意事项

使用Nginx或Apache等，请注意增加对除了status.html外文件的访问权限，以免数据丢失

## 待优化内容
- 生成html的界面美化
- 增加对telegram bot的支持（争取
- 增加直播源连接速度测试与展示
- ……
