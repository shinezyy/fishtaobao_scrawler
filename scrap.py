# -*- coding:utf-8 -*-


from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import time
from mail import send
import random
import config
from prices import *


mail_sender = 'diamondzyy@163.com'
mail_receiver = 'diamondzyy@sina.cn'

target_url_head= 'https://s.2.taobao.com/list/list?q='

target_url_tail = '&search_type=item&app=shopsearch'


def gen_req(url):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)'
            ' AppleWebKit/537.36 (KHTML, like Gecko)'
            ' Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    return req


def link_to_id(link):
    return int(link.split('id=')[1])


black_list = [
    '手机',
    '关联',
    '坏',
    '收',
    '尸体',
    '华为',
    '求购',
    '主板',
    '计算器',
    '转卖',
]


def fish_scrawler(url, expected_price, history_list):
    req = gen_req(url)
    r = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(r, "html.parser")
    print(soup.prettify())
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
        title = str(a.findChild('img')['alt'])
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
        print('\t\t--->', title, end=' ')
        print('\t\t--->', link)
        if not config.Testing:
            send(mail_sender, mail_receiver, title+'\n'+link)
    return item_list


expected_prices = dict()


def preproc_price():
    prices_1155 = raw_1155.split('\n')
    prices_1150 = raw_1150.split('\n')
    prices_amd = raw_amd.split('\n')
    prices_gpu = raw_gpu.split('\n')
    prices_phone = raw_phone.split('\n')
    prices_kbd = raw_kbd.split('\n')
    prices = prices_1155 + prices_1150 + prices_amd + prices_gpu + \
        prices_phone + prices_kbd
    for line in prices:
        if not len(line):
            continue
        item, price = line.lstrip(' ').rstrip(' ').split('=')
        item = item.replace(' ', '+')
        item = item.replace('-', '+')
        price = int(price) - config.delta_price
        print(item, price)
        expected_prices[item] = price


scrawl_fish = True


def main():
    preproc_price()
    while scrawl_fish:
        try:
            history_list = []
            # read history
            with open('history.txt') as f:
                for line in f:
                    history_list.append(int(line))
            for k in expected_prices:
                print(k)
                item = urllib.parse.quote(k.encode('gbk'))
                print('正在爬取', k, 'Escaped:', item, 'Expected Price:', expected_prices[k])
                if config.Testing:
                    print(target_url_head + item + target_url_tail)
                new_list = fish_scrawler(target_url_head + item + target_url_tail,
                                         expected_prices[k], history_list)
                time.sleep(random.randint(1, 3))
                if new_list:
                    with open('history.txt', 'a') as f:
                        for line in new_list:
                            print(line, file=f)
        except Exception as e:
            print(e)

        print('-------------------------------------------------------')
        if config.Testing:
            time.sleep(1)
        else:
            time.sleep(300)

    # gz_board_scrawler(gz_url, [])
    # gz_thread(gz_url, 0)


if __name__ == '__main__':
    main()
