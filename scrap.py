# -*- coding:utf-8 -*-


from bs4 import BeautifulSoup
import urllib2
import urllib
import re
from mail import send


mail_sender = 'diamondzyy@163.com'
mail_receiver = '1058149101@qq.com'
target_url_head = 'https://s.2.taobao.com/list/list.htm?q='
target_url_tail = '&search_type=item&app=shopsearch'

test = True


def gen_req(url):
    req = urllib2.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)'
            ' AppleWebKit/537.36 (KHTML, like Gecko)'
            ' Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    return req


def scrap_page(url, expected_price):
    req = gen_req(url)
    r = urllib2.urlopen(req).read()
    soup = BeautifulSoup(r, "html.parser")
    # print soup.prettify()
    lis = soup.find_all('li', class_='item-info-wrapper item-idle clearfix')
    for li in lis:
        # print li
        price_div = li.findChild('div', class_="item-price price-block")
        price_em = price_div.findChild('em')
        price = float(str(price_em).lstrip('<em>').rstrip('</em>'))

        if price > expected_price:
            continue

        a = li.findChild('a')
        link = 'http:' + a['href']
        title = unicode(a.findChild('img')['alt'])
        if test:
            print title
            print link
        else:
            send(mail_sender, mail_receiver, title+'\n'+link)


expected_prices = dict()
expected_prices['fx4300'] = 240
expected_prices['fx6300'] = 320
expected_prices['樱桃茶轴'] = 120
expected_prices['樱桃青轴'] = 120


for k in expected_prices:
    item = urllib.quote(k.decode('utf-8').encode('gbk'))
    print k, item
    print target_url_head+item+target_url_tail
    scrap_page(target_url_head+k+target_url_tail, expected_prices[k])
