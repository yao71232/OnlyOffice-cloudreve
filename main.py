#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File    : main.py
from urllib.parse import unquote
from re import findall
from sanic import Sanic
from sanic.response import file
from ext import render_template
from sanic_cors import CORS
from urllib3 import PoolManager

app = Sanic("office")
CORS(app)
client = PoolManager(100, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*",
    'Connection': 'close'
})


@app.route("/")
@app.route("/index.html")
def index(request):
    try:
        scheme = request.headers["X-Scheme"]
    except:
        scheme = request.scheme
    return render_template("index.html", scheme=scheme)


@app.route("/favicon.ico")
def favicon(request):
    return file("./favicon.ico")


@app.route("/<name:([a-z]{4})\.html>", methods=["GET"])
async def view(request, name):
    try:
        scheme = request.headers["X-Scheme"]
    except:
        scheme = request.scheme
    url = request.args.get("src")
    if not url:
        return render_template("index.html", scheme=scheme)
    if not findall(r"^https?:/{2}\w.+$", url):
        msg = "请使用标准url 示例: \\r\\nhttps://office.fynn.vip/view.html?src={$src} \\r\\n请求协议http和https都支持，请根据自己的网站设置同源协议"
        return render_template("msg.html", msg=msg)
    url = unquote(url)
    suffix = url.split(".")[-1]
    suffixs = ["docx", "doc", "pptx", "ppt", "docm", "xlsx", "xls", "xlsm", "xltx", "xltm", "xlsb", "xlam", "pptm",
               "ppsx", "ppsm", "rtf", "mdb", "pdf", "wps", "et", "dps", "csv", "odp", "odt", "ods", "docxf", "epub",
               "fb2", "html", "oform", "ott", "txt", "xml", "xps"]
    if suffix.lower() not in suffixs:
        try:
            resp = client.request("HEAD", url)
            if resp.status != 200:
                resp = client.request("GET", url)
        except:
            return render_template("msg.html", msg=f'请提供可访问url链接\\r\\n请确认{url}外网是否可以访问')
        try:
            resp = resp.headers["Content-Disposition"]
        except:
            return render_template("msg.html",
                                   msg=f'请确认是否是office支持的文件，如果本平台无法加载office\\r\\n请访问https://blog.fynn.vip联系作者')
        filename = unquote(findall(r"filename=\"(.*?)\"", resp)[0])
        suffix = filename.split(".")[-1]
        if suffix not in suffixs:
            return render_template("msg.html", msg=f"不支持的文件,请使用以下扩展名文件\\r\\n{' .'.join(suffixs)}")
    else:
        filename = url.split("/")[-1]
    if scheme == "http":
        host = "http://office.fynn.top:8080"
    elif scheme == "https":
        host = "https://office.fynn.top:8443"
    else:
        return f"不支持的协议{scheme}"

    return render_template(f"{name}.html", host=host, suffix=suffix, filename=filename, url=url)


# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=8000, debug=False, auto_reload=True)
