# -*- coding:utf-8 -*-

import pandas as pd


raw_1155 = '''
G530=100
G540=110
G620=110
G630=130
G640=140
G1620=160
I3-2100=300
I3-2120=310
I3-2130=310
I3-3220=370
I3-3240=380
I5-2300=480
I5-2320=500
I5-2400=530
I5-3470=660
'''

raw_1150 = '''
G3258=280
i3-4130=570
i3-4150=585
i3-4160=605
i3-4170=615
'''

raw_amd = '''
X4 631=50
X4 641=60
X4 651=70
X4 620=140
X4 630=150
X4 635=150
X4 640=170
X4 645=175
X4 740=160
X4 750=170
X4 955=180
X4 965=210
1055T=310
1100T=700
FX 4300=255
FX 6100=300
FX 6200=340
FX 6300=360
FX 8100=470
FX 8120=510
FX 8150=520
FX 8320=580
FX 8350=750
'''

raw_gpu = '''
'''

raw_kbd = '''
樱桃 茶轴=140
樱桃 青轴=140
'''

raw_phone = '''
魅族 mx2=140
魅族 mx3=220
魅蓝=270
'''


def get_618_phone_price():
    df = pd.read_csv('./resources/phone-price-19618.csv',
                     index_col=0, header=0, encoding='gbk')
    return df


def get_mid_end_phones():
    df = pd.read_csv('./resources/mid-end-phones.txt', sep=',',
                     index_col=None, header=None, encoding='utf8')
    return df

def get_835():
    df = pd.read_csv('./resources/snapdragon-835.txt', sep=',',
                     index_col=None, header=None, encoding='utf8')
    return df



def main():
    get_618_phone_price()


if __name__ == '__main__':
    main()

