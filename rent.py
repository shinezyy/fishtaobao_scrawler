# -*- coding:utf-8 -*-


from bs4 import BeautifulSoup
import urllib2
import urllib
import time
from mail import send
import random
import config
from prices import *


mail_sender = 'diamondzyy@163.com'
mail_receiver = 'diamondzyy@sina.cn'
target_url_head = 'https://www.douban.com/group/26926/discussion?start='


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


def find_house(url, history_list):
    req = gen_req(url)
    r = urllib2.urlopen(req).read()
    soup = BeautifulSoup(r, "html.parser")
    # print soup.prettify()
    trs = soup.find_all('tr', class_='')
    for tr in trs:
        title_a = tr.findChild('a', class_='')
        text = str(title_a)
        if 'title' in text:
            print text.split('title=')[1]
            print '-------------------------------------------------------'


def fish_scrawler(url, expected_price, history_list):
    req = gen_req(url)
    r = urllib2.urlopen(req).read()
    soup = BeautifulSoup(r, "html.parser")
    # print soup.prettify()
    lis = soup.find_all('li', class_='item-info-wrapper item-idle clearfix')
    item_list = []
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
        if link_to_id(link) in history_list:
            continue

        black = False
        for word in black_list:
            if word in title:
                black = True
                break
        if black:
            continue

        item_list.append(link_to_id(link))
        print '\t\t--->', title,
        print '\t\t--->', link
        if not config.Testing:
            send(mail_sender, mail_receiver, title+'\n'+link)
    return item_list





def main():
    find_house(target_url_head+'0', [])
    '''
    while True:
        print '-------------------------------------------------------'
        if config.Testing:
            time.sleep(1)
        else:
            time.sleep(300)
            '''



if __name__ == '__main__':
    main()
