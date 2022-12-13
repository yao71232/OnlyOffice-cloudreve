此项目从https://git.fynn.vip/fynn/onlyoffice-cloudreve搬运

## 推荐环境 Linux Python3.11

### 安装
`mkdir -p /python&&cd /python`

`wget https://git.fynn.vip/fynn/onlyoffice-cloudreve/-/archive/master/onlyoffice-cloudreve-master.zip`
- **或者使用git克隆**

`git clone https://git.fynn.vip/fynn/onlyoffice-cloudreve.git`
#### 进入目录
```
unzip onlyoffice-cloudreve-master.zip&&mv onlyoffice-cloudreve-master onlyoffice-cloudreve
cd onlyoffice-cloudreve
```
- **或者**

`cd onlyoffice-cloudreve`

#### 修改main.py
`else:
        filename = url.split("/")[-1]`
`if scheme == "http":
        host = "onlyoffice的ip:端口"`

#### 安装第三方库
`pip3 install -r requirements.txt`

#### 启动脚本
`sanic main:app --host=0.0.0.0 --port=8000`

#### 创建服务
`vim /usr/lib/systemd/system/onlyoffice.service`

```
[Unit]
Description=OnlyOffice Server

[Service]
Type=simple
WorkingDirectory=/python/onlyoffice-cloudreve/
ExecStart=/usr/bin/python3 -m sanic main:app --host=0.0.0.0 --port=8000
Restart=always
TimeoutSec=0

[Install]
WantedBy=multi-user.target

```
#### 启动服务并设置开机自启
```
systemctl daemon-reload
systemctl start onlyoffice
systemctl enable onlyoffice
```
### 查看服务状态
`systemctl status onlyoffice`
