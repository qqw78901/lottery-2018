# 2018年会标签云抽奖页面


## 环境部署

1. 下载并安装[python3](https://www.python.org/ftp/python/3.6.4/python-3.6.4.exe)。
2. 获取源代码 `git clone http://code.yy.com/luoning/lottery-2018.git`
3. `cd lottery-2018`
4. 安装pyenv虚拟环境 `python3 -m venv`
5. 激活并使用虚拟环境 `venv/Scripts/activate.bat` (非windows使用 `source venv/bin/activate`)
6. 安装依赖环境 `pip install -r requirements.txt`
7. 运行程序 `python3 run.py`
8. 使用浏览器打开 <http://127.0.0.1:8080> 即可看到欢迎页



## 关于

- 前端：JQuery, TagCanvas （zuowenqi@yy.com）
- 后台：python3, bottle, tinydb （luoning@yy.com）


#fork

- 前端抽奖标签云原来用的是一套开源的标签云插件，效果不够炫
- luckily，开发完成的最后一天，看到张云龙当天提交的标签云效果，于是标签效果直接取用他那一套了，tagcanvas.js就是从他那里fork过来的，

