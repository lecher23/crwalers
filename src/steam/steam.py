# coding: utf-8

import datetime
import requests
from bs4 import BeautifulSoup


class SteamOnlineNumber(object):
    def __init__(self):
        self.page_url = "http://store.steampowered.com/stats/?l=schinese"

    def run(self, head_n):
        r = requests.get(self.page_url)
        game_stats = self.do(r.content)
        for name, current, top in game_stats[:head_n]:
            print u"{:45}: 当前 {}, 峰值 {}".format(name, current, top)

    def do(self, content):
        html = BeautifulSoup(content, 'html5lib')
        h2 = html.find("h2", {"class": "pageheader"})
        update_time = h2.span.text
        print self.parse_time(update_time)
        div = html.find('div', {'id': 'detailStats'})
        tbody = div.table.tbody
        game_stats = []
        for tr in tbody.find_all('tr'):
            item = [None] * 4
            for i, td in enumerate(tr.find_all('td')):
                if i >= len(item):
                    continue
                span = td.find('span')
                if span:
                    item[i] = span.text
                a = td.find('a')
                if a:
                    item[i] = a.text
            if item[3]:
                game_stats.append((item[3], self.convert_num(item[0]), self.convert_num(item[1])))
        return game_stats

    def convert_num(self, raw):
        raw = int(raw.replace(',', ''))
        wan = raw / 10000
        suffix = (raw % 10000) / 100
        return u'{:3}.{:<2}万'.format(wan, suffix)

    def parse_time(self, src):
        try:
            tmp = datetime.datetime.strptime(src.encode('utf-8'), '更新日期：%Y年%m月%d日下午%H:%M')
            tmp += datetime.timedelta(hours=12)
        except:
            tmp = datetime.datetime.strptime(src.encode('utf-8'), '更新日期：%Y年%m月%d日上午%H:%M')
        d = tmp + datetime.timedelta(hours=16)
        return d.strftime('%Y年%m月%d日 %H:%M')


if __name__ == '__main__':
    SteamOnlineNumber().run(int(raw_input('前多少的游戏?')))
