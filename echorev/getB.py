# 下载 geckodriver 后加入到PATH路径下
# pip install selenium

from selenium import webdriver # 从selenium导入webdriver
from selenium.webdriver.firefox.options import Options
f = open("./result.txt", "w+") # 这就是结果要存储的文件，在当前目录
origin_url = 'https://space.bilibili.com/486009552/video' # 这个 url 就是你要获取链接UP主的B站页面地址
tail_url = 15 # 这个 url 就是你要获取链接UP主的B站页面的页数
middle_url = '?tid=0&page='
url_list = []
for i in range(tail_url):
    url_list.append(origin_url+middle_url+str(i+1))

html = ''
for url in url_list:
    options = Options() # 浏览器选项
    options.add_argument("--headless")
    browser = webdriver.Firefox(options= options)
    browser.get(url) # 获取页面
    html= html + browser.page_source
    browser.close()

html=html.replace('href','\n')
html=html.replace('target','\n')
html=html.replace('''><''','')
html=html.replace('''=''','')
html=html.replace('''_''','')
html=html.replace('''blank''','')
html=html.replace('''title''','')
html=html.replace('''meta''','')
html=html.replace('''play''','')
html=html.replace('''class''','')
html=html.replace('''icon''','')
html=html.replace('''span''','')
html=html.replace('''></i>''','')
html=html.replace('''><i''','')
html=html.replace('''<''','')
html=html.replace('''>''','')
html_content = html.splitlines()
video_list = []
for i in html_content:
    if('''www.bilibili.com/video/BV''' in i):
        i=i.replace('"','\n')
        i=i.replace('''//''','''https://''')
        print(len(i))
        video_list.append(i)
video_str = ''.join(video_list)
video_str = ''.join([s for s in video_str.splitlines(True) if s.strip()])
tmp_list = video_str.splitlines()
print(len(tmp_list))
new_list = []
for i in tmp_list:
    if('''www.bilibili.com/video/BV''' in i):
        print(len(i))
        if i not in new_list:
            new_list.append(i)
            f.write(i+"\n")
result= ''.join(new_list)
print(result)
f.close()