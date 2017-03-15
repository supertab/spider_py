# site: http://bj.5i5j.com/exchange/n
# 抓取数据：地点（et.海淀区), 面积, 居室, 方位, 楼层, 房价
# naming ：area，feet，rooms，direction，floor, price

import urllib.request as req
import time
import re
import random as rd

def house_info(url, num):
    eflag = 0
    userAgent = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    price, area, feet, rooms, direction, floor = [], [], [], [], [], []
    url += str(n)
    try:
        require = req.Request(url, headers = userAgent)
        response = req.urlopen(require)
        html = response.read().decode('utf-8')
        # list-info-l: 地点，面积，et
        # list-info-r: 单价，总价
        # 类型：页面内反复出现这些标签
        # info_l= re.findall(r'list-info-l">(.*?)publish', html, re.S)
        # info_r = re.findall(r'list-info-r">(.*?)万元</em>', html, re.S)
        temp= re.findall(r'list-info-l">(.*?)publish(.*?)list-info-r">(.*?)万元</em>', html, re.S)
        # temp = re.search(r'list-info-l">(.*?)</span></li>', html, re.S).groups()
        # split
        for h in temp:
            # 区域
            part_h = h[0].split()
            area.append( re.findall('change.*">(.*?)</a>',part_h[8])[0])
        # rooms, feet, dirct, floor
            others = re.findall('span>(.*?)</span',part_h[-5],re.S)
            # rooms
            rooms.append( int(others[0][0])+int(others[0][2]))
            # feet
            feet.append( float(others[1].split('平')[0]) )
            # direction
            direction.append(others[2])
            # floor
            floor.append(float(re.findall(r'/(.*)层', others[3])[0]))
            # price
            price.append(float(re.findall(r'>(.*)<em>',h[2])[0]))
# return info_l, info_r
    except:
        print('Err...')
        eflag =1

    return [ area, rooms, feet, direction, floor, price], eflag


url = 'http://bj.5i5j.com/exchange/n'
pageNum = 2 
house = []
attrNum = 6
for i in range(attrNum):
    house.append([])

for n in range(1,pageNum+1):
    print('loading page: %s...'%n)
    temp, err= house_info(url,n)
    if not err:
        # 合并list
        for index, attr in enumerate(temp):
            house[index].extend(attr)
    time.sleep(rd.randrange(5,12))


import dataSave as sav
sav.list2csv(house, 'houseInfo.csv')
