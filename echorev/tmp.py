from urllib import request
req = request.Request('https://www.zhihu.com')
req.add_header('User-Agent', 'Mozilla/6.0')
response =  request.urlopen(req)
# 获取状态码，如果是200表示成功
print(response.status)
# 读取网页内容
# print(response.read().decode('utf-8'))

#保存cookie的文件
import urllib.request
import http.cookiejar

filename = 'cookie.txt'
# 声明一个MozillaCookieJar对象实例（cookie）来保存cookie，后面写入文件
url = 'http://www.zhihu.com'
cookie = http.cookiejar.MozillaCookieJar(filename)
# 还是创建处理器
handler = urllib.request.HTTPCookieProcessor(cookie)
# 创建支持处理HTTP请求的opener对象
opener = urllib.request.build_opener(handler)
opener.open(url)
# 保存cookie到文件
cookie.save(ignore_discard=True, ignore_expires=True)
# ignore_discard表示即使cookie将被丢弃也将保存下来，ignore_expires表示如果该文件中cookie已经存在，则覆盖原文件写入

import urllib.request
import http.cookiejar

url = 'http://www.zhihu.com'
# 声明CookieJar对象实例来保存cookie
cookie = http.cookiejar.MozillaCookieJar()
# 从文件中读取内容到cookie变量中
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
# 处理器
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
print(opener.open(url).read())


import urllib.request
import http.cookiejar

# 自动记住cookie
url = 'http://www.zhihu.com'
# 声明cookiejar的对象,存放cookie的容器
cookie = http.cookiejar.CookieJar()  
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open(url)
# 获取状态码，如果是200表示成功
print(response.status)
# 读取网页内容
print(response.read().decode('utf-8'))

print("\n")
for item in cookie:
    print(item.name + '=' + item.value)
