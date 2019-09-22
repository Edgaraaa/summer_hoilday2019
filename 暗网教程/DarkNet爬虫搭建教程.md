# DarkNet爬虫搭建教程

> [暗网爬虫项目地址:https://github.com/aoii103/DarkNet_ChineseTrading.git](https://github.com/aoii103/DarkNet_ChineseTrading.git)
>
> 本项目给的安装教程是基于Mac OS的一个安装方式，但是其实在其他Linux系统上进行搭建，本次使用的是Ubuntu19.04进行的搭建

# 0x00 第一步当然是装一个Ubuntu19.04虚拟机

[虚拟机安装教程：https://www.cnblogs.com/feifanrensheng/articles/8644798.html](https://www.cnblogs.com/feifanrensheng/articles/8644798.html)

这一部分自理

# 0x01 安装所需软件

1. 安装git

   ```bash
   sudo apt install git
   # 最好还是用su权限吧，比较省事
   apt install git
   ```

2. 安装Tor

   > 这里就是有一点点区分了，这里的Tor指的是Tor代理网络，而不是Tor浏览器，所以不要搞错。

   ```bash
   apt install tor
   ```

   然后进行配置，其实要配置的东西挺少的

   ```bash
   vim /etc/tor/torrc
   ```

   在里面添加几句就行

   ```bash
    SOCKSPort 9150 					# socks5代理地址
    Socks5Proxy 127.0.0.1:1086 		# 科学上网代理地址(如已翻墙可不填)
    RunAsDaemon 1 					# 开启后台运行
    ControlPort 9151 				# 开启控制端口
   ```

   Tor配置完毕

3. 安装Mysql

   GitHub里面用的是Docker搭建的，这个是可以的，但是我感觉这个假如是自用的话，是可以直接安装在虚拟机上面，不会有啥大问题的。

   [https://blog.csdn.net/t544846450/article/details/93510065](https://blog.csdn.net/t544846450/article/details/93510065)

   这一部分也是自理

4. 安装redis

   这一部分也是安装在了虚拟机本机上，其实不怕安全性问题，毕竟自己用，要是怕安全问题可以，可以安装在Dockers上这个无可厚非

5. 安装python

   最好是python3.7足够了，要有pip3这个

   ```bash
   apt install python3
   apt install python3-pip
   ```

   这里也差不多了

6. 安装tesseract(我感觉也可以不要这个我们可以自己注册一个账号 修改数据库因为这个软件识别效率太差（对8起我花了一下午时间才搞对一次）)

   这个也是直接apt就可以了

   ```bash
   apt install tesseract-ocr
   ```

基本准备的差不多了

# 0x02 开始躺爬虫的坑了

我们第一件事克隆程序

```bash
git clone https://github.com/aoii103/DarkNet_ChineseTrading.git
```

第二件事

我们先看看文件是一个什么样

```bash
![1](C:\Users\lenovo\Desktop\暗网教程\1.png).
├── common.py
├── conf.py
├── cursor.py
├── darknet.ini
├── datas
├── grafana.sql
├── LICENSE
├── log.py
├── media
│   ├── captcha.png
│   ├── cookie.png
│   ├── darknet1.jpg
│   ├── DarkNet.png
│   ├── datalist.png
│   ├── datasdemo_1.png
│   ├── details.png
│   ├── flower.png
│   ├── grafana.png
│   ├── main.png
│   ├── mosaic.jpg
│   ├── newtg.png
│   ├── raw.jpg
│   ├── reg1_html2.png
│   ├── reg1_html.png
│   ├── reg1.png
│   ├── reg_res.png
│   ├── run.png
│   ├── telegram.png
│   ├── types.png
│   ├── usesocks5h.png
│   └── wikires_1.png
├── model.py
├── parser.py
├── __pycache__
│   ├── common.cpython-37.pyc
│   ├── conf.cpython-36.pyc
│   ├── conf.cpython-37.pyc
│   ├── cursor.cpython-37.pyc
│   ├── log.cpython-36.pyc
│   ├── log.cpython-37.pyc
│   ├── model.cpython-37.pyc
│   ├── parser.cpython-37.pyc
│   ├── task.cpython-36.pyc
│   └── task.cpython-37.pyc
├── README_en.md
├── README.md
├── requirements.txt
├── restart_task.sh
├── run.py
├── screen_shot
│   ├── 25566_0.png
│   ├── 26440_0.png
│   ├── 26634_0.png
│   ├── 26635_0.png
│   ├── 26636_0.png
│   ├── 26681_0.png
│   ├── 27435_0.png
│   ├── 27435_1.png
│   ├── 27876_0.png
│   ├── 28095_0.png
│   ├── 28227_0.png
│   ├── 28228_0.png
│   ├── 28476_0.png
│   ├── 29210_0.png
│   ├── 29700_0.png
│   ├── 29700_1.png
│   ├── 29700_2.png
│   ├── 29700_3.png
│   ├── 29787_0.png
│   ├── 29787_1.png
│   ├── 30004_0.png
│   ├── 30461_0.png
│   ├── 30575_0.png
│   ├── 30575_1.png
│   ├── 30575_2.png
│   ├── 30575_3.png
│   ├── 30685_0.png
│   ├── 30767_0.png
│   ├── 30767_1.png
│   ├── 30767_2.png
│   ├── 30767_3.png
│   ├── 30840_0.png
│   ├── 30841_0.png
│   ├── 30930_0.png
│   ├── 31259_0.png
│   ├── 31332_0.png
│   ├── 31332_1.png
│   ├── 31411_0.png
│   ├── 31411_1.png
│   ├── 31433_0.png
│   ├── 31437_0.png
│   ├── 31526_0.png
│   ├── 31577_0.png
│   ├── 31577_1.png
│   ├── 31577_2.png
│   ├── 31577_3.png
│   ├── 31647_0.png
│   ├── 31685_0.png
│   ├── 31721_0.png
│   ├── 31730_0.png
│   ├── 31735_0.png
│   ├── 31735_1.png
│   ├── 31742_0.png
│   ├── 31742_1.png
│   ├── 31758_0.png
│   ├── 31758_1.png
│   ├── 31761_0.png
│   ├── 31766_0.png
│   ├── 31776_0.png
│   ├── 31776_1.png
│   └── 31776_2.png
└── task.py
```

我们先设置一下```conf.py```文件来配置一下环境，

![1](https://github.com/Edgaraaa/summer_hoilday2019/blob/master/%E6%9A%97%E7%BD%91%E6%95%99%E7%A8%8B/1.png?raw=true)

主要设置这两边，创建数据库是python脚本自己会去做的，我们不需要去自己创建同名数据库的，因为自己创建还会造成编码不一致，然后乱码，就会躺一波坑(当时发现乱码，难受的一批)

之后其实就是把那个验证码识别的机器学习后的文件，拷贝到固定文件夹就可以跑了。

跑之前先跑tor网络和挂一个全局代理，这个是去暗网的标配

然后```python3 run.py```跑起来就可了，主要可能会碰见mysql链接不上，还有就是mysql的安全设置搞一下应该没有其他的坑了。



