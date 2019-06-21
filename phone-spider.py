# -*- coding:utf-8 -*-


from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import time
from mail import send
import random
import config
from prices import *
import sys


mail_sender = 'diamondzyy@163.com'
# mail_receiver = 'diamondzyy@sina.cn'

target_url = 'https://s.2.taobao.com/list/list?q={}' \
             '&search_type=item&&st_edtime=1&app=shopsearch'


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
    '换',
    '关联',
    '坏',
    '收',
    '尸体',
    '华为',
    '求购',
    '主板',
    '计算器',
    '壳',
    '膜',
    '充电器',
    '快充',
    '券',
    '非',
    '云拍',
    '太容易',
    '宫中号',
    '拆机',
    '总成',
    '王者荣耀',
    '王者',
    'cos',
    '预约',
    '专柜',
    '参加活动',
    '红包',
    '上海电信',
    '解锁工具',
    '官方旗舰店正品',
    '苹果',
    '步步高正品',
    '电信套餐',
    '荣耀V9',
    '小米平板',
    '床垫',
    '分期',
    '原装屏幕',
    '别着急拍',
    '是否有货',
    '漏液',
]

black_nick_list = [
    't_',
    'tb',
]


def spec_pattern_gen():
    mem_size = [4, 6, 8]
    flash_size = [32, 64, 128, 256]
    units = ['', 'g', 'gb', 'G', 'GB']
    connector = [' ', '+', '加']
    for mem in mem_size:
        for flash in flash_size:
            for u in units:
                for c in connector:
                    p = f'{mem}{u}{c}{flash}{u}'
                    yield p, mem, flash


def spec_reformat(mem, flash):
    return f'{mem}+{flash}'


def extract_spec(title: str, desc: str):
    for p, m, f in spec_pattern_gen():
        if p in title or p in desc:
            # print(p, title, desc)
            return m, f
    return 0, 0


def get_lowest_price(s: pd.Series):
    specs = ['4+64', '6+64', '6+128', '8+128', '8+256']
    for spec in specs:
        if not pd.isna(s[spec]):
            return s[spec]


def get_items(url):
    req = gen_req(url)
    r = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(r, "html.parser")
    # print(soup.prettify())
    divs = soup.find_all('div', class_='item-block item-idle sh-roundbox')
    # print(divs)
    items = []
    for div in divs:
        print('#', end='')
        # print(div)

        a_s = div.findChildren('a', target='_blank', title=None)
        link = None
        for a in a_s:
            link = a['href']
            # print(link)
            if 'iphone' in link or 'mobile' in link:
                continue

        title_a = div.findChild('a', href=link)
        title = title_a['title']

        seller_a = div.findChild('div', class_='seller-avatar').findChild('a')
        seller = seller_a['title']  # type: str
        # print(seller_a)
        # print(seller)

        desc_div = div.findChild('div', class_='item-brief-desc')
        desc = desc_div.contents[0]

        black_flag = False

        for nick in black_nick_list:
            if seller.startswith(nick):  # bots
                black_flag = True
                print(f'skip bot: {seller}')
                break

        for word in black_list:
            if word in title or word in desc:
                black_flag = True
                break

        if black_flag:
            continue

        mem, flash = extract_spec(title, desc)
        mem_flash = spec_reformat(mem, flash)

        price_div = div.findChild('div', class_='item-price price-block')
        # print(price_div)
        price = float(str(price_div.contents[0].contents[1].contents[0]))

        # print(title)
        # print(desc)
        # print(price)
        # print(spec_reformat(mem, flash))

        items.append((link_to_id(link), 'https:' + link, mem_flash, price, title, desc, seller))
    print('')
    return items


scrawl_fish = True


def main():
    phones = get_618_phone_price()

    while scrawl_fish:
        while True:
            history_list = []
            # read history
            with open('history.txt') as f:
                for line in f:
                    history_list.append(int(line))
            for k in phones:
                new_list = []
                col = phones[k] # type: pd.Series
                if pd.isna(col['name']):
                    continue
                item = urllib.parse.quote(col['name'].encode('gbk'))
                print('正在爬取', k, 'Escaped:', item)
                print(target_url.format(item))
                items = get_items(target_url.format(item))
                # print(items)
                for item_id, link, spec, price, title, desc, seller in items:
                    flag = False
                    if item_id in history_list:
                        continue
                    new_list.append(item_id)
                    # print('col[spec]', col[spec])
                    # print('get_lowest_price', get_lowest_price(col))
                    if spec == '0+0' or spec not in col.keys():
                        if float(get_lowest_price(col)) * config.discount >= price >= \
                                float(get_lowest_price(col)) * config.lowest_discount:
                            flag = True
                        else:
                            flag = False
                    else:
                        if float(col[spec]) * config.discount >= price >= float(col[spec]) * config.lowest_discount:
                            flag = True
                        else:
                            flag = False
                    if price > config.max_price:
                        flag = False

                    if flag:
                        info = f'{k}\n{seller}\n{spec}\n{price}\n{link}\n{title}\n{desc}'
                        if config.Testing:
                            print(info)
                        else:
                            send(mail_sender, mail_sender, f'{seller} {k}=={title}={price}', info)

                if config.Testing:
                    time.sleep(1)
                else:
                    time.sleep(random.randint(3, 15))

                if len(new_list):
                    with open('history.txt', 'a') as f:
                        for line in new_list:
                            print(line, file=f)
            break
        # except Exception as e:
        #     print(e)

        print('=======================================================')
        if config.Testing:
            time.sleep(2)
        else:
            time.sleep(random.randint(200, 300))


if __name__ == '__main__':
    main()
