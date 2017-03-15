import urllib.request as req
import time
import re
# 得到所有列表，有链接和没有链接的作标志
def get_url( url):
    html = req.urlopen(url).read().decode('utf-8')
    url_list = re.findall(r'platname">(.*?)</td>',html,re.S)[1:-3]
    # 建立字典，单位名为key，[]为value, 字典为无序的，在此不适合
    # company_dict = {}
    company_list = []
    for i in url_list:
        isfind = i.find('href') +1
        temp = ['']*10
        if isfind:
            (url, name) = re.search(r'href="(.*?)".*blank">(.*?)<',i).groups()
            temp[0] = name
            temp[1] = url
            company_list.append(temp)
        else:
            temp[0] = re.search(r'wrap">(.*?)<',i).groups()[0] 
            company_list.append(temp)
    # findall substring
    return company_list
def get_msg(url_list):
    userAgent = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    err_list = []
    res_list = []
    for url in url_list:
        if len(url[1]):
            require = req.Request(url[1], headers = userAgent)
            response = req.urlopen(require)
            html = response.read().decode('utf-8')
            temp = []
            try:
                # bq-box, 平均收益率，投资期限
                group1= re.search(r'"bq-box">(.*?)</div>.*平均收益率(.*?)</dd>.*投资期限(.*?)</dd>',html,re.S).groups()
                ch = group1[0]
                isfind = ch.find('tag1') +1
                if isfind:
                    temp.append( re.search(r'>(.*?)<',ch).groups()[0])
                else:
                    temp.append('none')
                temp.append(re.search(r'm>(.*?)<',group1[1]).groups()[0])
                temp.append(re.search(r'm>(.*?)<',group1[2]).groups()[0])
                # 银行存管，保障模式，风险准备金存管
                group2 = re.search(r'银行存管(.*?)</dd>.*保障模式(.*?)</dd>.*风险准备金存管(.*?)</dd>',html, re.S).groups()
                temp.append(group2[0].split()[3])
                temp.append(group2[1].split()[3])
                temp.append(re.search(r'p">(.*?)<',group2[2]).groups()[0])
                url[2:7] = temp[:]
                res_list.append(url)
                time.sleep(0.3)
            except:
                temp.clear()
                temp = ['-']*5
                url[2:7] = temp[:]
                res_list.append(url)
                time.sleep(0.3)
                continue
        else:
            res_list.append(url)
    # bqpattern = re.compile(r"bq-box>(.*)\/span")
# bqbox = bqpattern.search(html).groups()
    return res_list, err_list 
def list2csv(data, filename):
    #data 为二维数组
    temp_str = ''
    for each_list in data:
        for element in each_list:
            temp_str = temp_str+element+','
        temp_str += '\n'
    with open(filename, 'w') as f:
        f.write(temp_str)
url = 'file:///home/zooo/webdata/2016.html' # the path of download html
company_list= get_url(url)
data, err_list= get_msg(company_list)
