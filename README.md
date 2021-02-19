# IPTV-M3U-Checker 直播源批量检测程序

## 简介

Python初学者，能力有限，还请见谅。

针对目前`个人使用`的痛点，实现直播源`自动化定时检测`，便于及时替换失效源。一般不会出现大规模失效，除非同一域名/ip挂了，那么替换即可。如果是需要初次检测某一（大量）直播源，请使用其他工具。

本项目改自<a href="https://github.com/AlexKwan1981/iptv-m3u8-checker" target="_blank">AlexKwan1981/iptv-m3u8-checker</a>，感谢！

增加了<a href="https://ding-doc.dingtalk.com/doc#/serverapi2/krgddi" target="_blank">钉钉群机器人</a>，可以配合定时任务，实现直播源的定时检测与通知，使用`Office Web Viewer`展示测试结果。

增加了直播源连接速度测试（占用资源和时间可能较长，默认关闭），参考项目<a href="https://github.com/chaichunyang/m3u-tester" target="_blank">chaichunyang/m3u-tester</a>，感谢！

基于个人能力和`.m3u`文件自身标签的原因，暂时删除了对`.m3u`文件的支持（原项目也不完全支持），目前仅支持`.txt`直播源的检测。（有许多在线工具/软件能较好地将`.m3u`转为`.txt`）

### 主要功能
对直播源进行批量检测，并通过钉钉群机器人及时反馈检测结果。
- 将待检测的直播源文件放置到`playlists/`文件夹下：  
  - 支持在线直链（如`raw.githubusercontent.com`，`gitee.com/*/raw/`等，可添加多个），自动下载至`playlists/`文件夹，文件名相同则直接覆盖（类似自动更新）
  - 支持多个本地文件
  - 目前仅支持`.txt`格式，详见playlists文件下的demo示例
- 直播源检测
  - 对每个连接进行测试，同时记录当前网络对该连接的延迟（参考<a href="https://github.com/EvilCult/iptv-m3u-maker" target="_blank">EvilCult/iptv-m3u-maker</a>）  
  - 支持测试有效直播源的连接速度
  - 将失效的直播源以文本形式通过钉钉群机器人通知
  <img src="https://ae01.alicdn.com/kf/Ud43b3682d4494d45a0248eace0178187E.jpg" height = "300" alt="钉钉群通知展示" align=center />
  
  - 通过`DataFrame.to_excel()`在`output/`目录下生成全部测试结果的Excel 预览，以链接形式通过钉钉群机器人发送
  <img src="https://ae01.alicdn.com/kf/U080f091db1d24cc788b72b65efef7b64H.jpg" height = "400" alt="钉钉群通知展示" align=center />
  
  - 生成的文件名以`测试时间+token`命名，防止直播源泄露

## 使用方法

本项目基于 **python3.7** 进行开发 

- 模块安装 Requirements
```
pip3 install pandas
pip3 install requests
pip3 install DingtalkChatbot
pip3 install openpyxl

* 国内可以使用-i参数加快下载速度
如：pip3 install DingtalkChatbot -i https://pypi.tuna.tsinghua.edu.cn/simple
```

- 钉钉群机器人配置

  - 群设置->智能群助手->添加机器人->添加机器人->自定义->添加
  - 获得`secret`
  <img src="https://ae01.alicdn.com/kf/Uafc4e58d1f1746d5ae834f3e0bc38227i.jpg" height = "400" alt="secret" align=center />
  
  - 获得`webhook`
  <img src="https://ae01.alicdn.com/kf/U78defb7a5d954af5ae962d4b40b81d34D.jpg" height = "400" alt="secret" align=center />

- 主要参数  
  - `webhook`：填入钉钉群自定义机器人的token
  ```
  修改main.py第23行
  webhook = 'https://oapi.dingtalk.com/robot/send?access_token=这里填写自己钉钉群自定义机器人的token'
  ```
  - `secret`：创建机器人勾选“加签”选项所设置的密钥
  ```
  修改main.py第24行
  secret = 'SEC11b9...这里填写自己的加密设置密钥'  # 创建机器人勾选“加签”选项时使用
  ```
  - `SpeedTest`：是否开启直播源连接速度测试，默认关闭（开启可能增加耗时与资源占用）
  ```
  修改main.py第29行
  SpeedTest = True # default False
  ```
  - `your_domain`：生成的excel文件所在服务器域名/ip
  ```
  修改main.py第31行 注意添加 http / https
  your_domain = 'https://list.domain.com'

  如果没有服务器 / 不需要通知，请将your_domain置为空值
  your_domain = ''
  ```
  - `playlist_file` = 'playlists/' 
  直播源源文件存放路径
  - `delay_threshold` = 5000  
  响应延迟阈值，单位毫秒，超过这个阈值则认为直播源质量较差
- 运行
```
只检测本地文件：python3 main.py
检测直链文件：python3 main.py https://raw.githubusercontent.com.txt https://gitee.com/a/b/raw.txt http://c.txt

也可配合crontab等定时执行

* 检测直链时，自动下载至playlists/，而后检测该目录下所有文件
```

## 注意事项

使用Nginx或Apache等，请注意增加对除了`.xlsx`外文件的访问权限，以免数据丢失

nginx可使用如下配置
```
location ~ \.(py|pyc|txt|sqlite3)$ {
      deny all;
} 
```

## 待优化内容
- 增加对telegram bot的支持（争取
- 部分直播源测速问题
- 代码优化
- ……
