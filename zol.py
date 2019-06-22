from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import spider_common as c

url = 'http://detail.zol.com.cn/cell_phone_advSearch/subcate57_1_s7500-s7235-s6472-s7546-s7289-s7049-s6475-s7798-s7338-s7786-s6509-s5307-s7372-s2991_9_1__{}.html#showc'
s = set()
for page in range(1, 7):
    req = c.gen_req(url.format(page))
    r = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(r, "html.parser")
    # print(soup.prettify())

    ul = soup.findChild('ul', class_='result_list')  # type:BeautifulSoup
    for li in ul.findChildren('li', recursive=False):  # type:BeautifulSoup
        # print(li)
        dt = li.findChild('dt')  # type:BeautifulSoup
        name = dt.findChild('a').contents[0]
        name = name.split('（')[0]

        battery = None
        sub_lis = li.findChildren('li', recursive=True)  # type:[BeautifulSoup]
        for sub_li in sub_lis:
            if '电池容量' in sub_li.contents[0]:
                battery = sub_li.contents[0]
        battery = battery.split('：')[1].split('mAh')[0]
        if int(battery) > 3300:
            s.add(name)
for name in s:
    print(name)
