#coding = utf-8
import urllib.request
import urllib.parse
import http.cookiejar

def xxx():
    #访问网址
    response = urllib.request.urlopen("http://www.baidu.com")
    print(response.read().decode('utf-8'))

    #访问post请求
    post_dic = {'word':'hello'}
    data = bytes(urllib.parse.urlencode(post_dic),encoding='utf-8')
    print(data)  #b'word=hello'
    response = urllib.request.urlopen("http://httpbin.org/post",data = data)
    print(response.read().decode('utf-8'))

    #设置超时时间
    try:
        response = urllib.request.urlopen("http://httpbin.org/post",data = data,timeout=0.1)
        print(response.read().decode('utf-8'))
    except urllib.error.URLError:
        print("访问超时")

    #状态码 响应头
    response = urllib.request.urlopen("http://www.baidu.com")
    print(response.status)     #200
    print(response.getheaders())
    print(response.getheader('Server'))
    
    #Request
    request = urllib.request.Request("http://python.org")
    response = urllib.request.urlopen(request)
    print(request)
    print(response.read().decode('utf-8'))

    #headers
    url = "http://httpbin.org/post"
    headers = {
            'User-Agent':'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)',
            "Host":"httpbin.org"
    }
    dict = {
            'name':'Germey'
    }
    data = bytes(urllib.parse.urlencode(dict),encoding='utf-8')
    req = urllib.request.Request(url = url,data = data,headers=headers,method = 'POST')
    print(req )
    response = urllib.request.urlopen(req)
    print(response.read().decode('utf-8'))

    #代理
    proxy_hander = urllib.request.ProxyHandler({
        'http':"http://127.0.0.1:1080",
        'http':"http://127.0.0.1:1080",
    })
    opener = urllib.request.build_opener(proxy_hander)
    response = opener.open("http://www.google.com")
    print(response.read().decode('utf-8'))
    
    
    #Cookie
    cookie = http.cookiejar.CookieJar()
    hander = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(hander)
    response = opener.open("http://www.baidu.com")
    for item in cookie:
        print(item.name+'='+item.value)
        
    #Cookie保存
    filename = "cookie.txt"
    cookie = http.cookiejar.MozillaCookieJar(filename)
    hander = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(hander)
    response = opener.open("http://www.baidu.com")
    cookie.save(ignore_discard=True,ignore_expires=True)

    #Cookie保存2
    filename = "cookie.txt"
    cookie = http.cookiejar.LWPCookieJar(filename)
    hander = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(hander)
    response = opener.open("http://www.baidu.com")
    cookie.save(ignore_discard=True,ignore_expires=True)


cookie = http.cookiejar.MozillaCookieJar()
cookie.load("cookie.txt",ignore_discard=True,ignore_expires=True)
hander = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(hander)
response = opener.open("http://www.baidu.com")
with open("1.html",'wb') as fp:
    fp.write(response.read())
# print(response.read().decode('utf-8'))














