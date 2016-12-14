# -*- coding:utf-8 -*-


from bs4 import BeautifulSoup
import urllib2
import urllib
import time
from mail import send
import random
import config
from prices import *
import re


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


targets = [
    u'中关村',
    u'知春里',
    u'知春路',
    u'海淀黄庄',
    u'人大',
    u'双清路',
    u'清华',
]


def find_house(url, history_list):
    req = gen_req(url)
    r = urllib2.urlopen(req).read()
    soup = BeautifulSoup(r, "html.parser")
    # print soup.prettify()
    trs = soup.find_all('tr', class_='')
    for tr in trs:
        title_a = tr.findChild('a', class_='')
        link = title_a['href']
        text = str(title_a)
        if 'title' in text:
            m = re.search('title=\"((.|\n)*)\"', text)
            if not m:
                continue
            title = m.group(1)
            for target in targets:
                if target.encode('utf8') in title:
                    id_str = re.search('.*topic/(.*)/', link)
                    if id_str:
                        id_int = int(id_str.group(1))
                        if id_int in history_list:
                            break
                        print title
                        print link
                        history_list.append(id_int)
                        print '-------------------------------------------------------'
                    else:
                        print link


    return history_list


def main():
    while True:
        try:
            history_list = []
            with open('house_history.txt') as f:
                for line in f:
                    history_list.append(int(line))

            for i in range(0, 40):
                nl = find_house(target_url_head + str(i*25), history_list)

                print 'Finished Page', i

                with open('house_history.txt', 'w') as f:
                    if nl:
                        for line in nl:
                            print >>f, line

                time.sleep(random.randint(1, 3))
        except Exception as e:
            print e

        time.sleep(random.randint(10, 20))


if __name__ == '__main__':
    main()
