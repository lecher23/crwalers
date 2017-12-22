# coding: utf-8

import logging
import requests
from bs4 import BeautifulSoup
from model import ComicEntry, PlayerEntry

HOST = "http://www.ikanfan.com"
HEADERS = {
    'Referer': 'http://www.ikanfan.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}


class IKanFanCrawler(object):
    def __init__(self):
        self.comics = []
        self.session = requests.session()

    def _get(self, url):
        r = self.session.get(url, headers=HEADERS)
        return BeautifulSoup(r.content, 'html5lib')

    def get_category(self):
        h = self._get(HOST)
        nav_div = h.body.find('div', {'class': 'wp mcid'})
        category = {}
        for a in nav_div.children:
            if a['href'].find('index') < 0:
                continue
            category[a.text] = a['href']
        return category

    def get_comic_list(self, category, path):
        h = self._get(HOST + path)
        comics_div = h.find('div', {'id': 'contents'})
        for a in comics_div.children:
            entry = ComicEntry()
            entry.comic_id = a['data-id']
            entry.page_path = a['href']
            entry.name = a['title']
            entry.cover = a.div.img['data-original']
            entry.tag = a.p.text
            entry.category = category
            logging.warning('get comic %s done.', entry.name)
            self.comics.append(entry)

    def run(self):
        category = self.get_category()
        for name, path in category.items():
            url = HOST + path
            logging.warning('crawl %s: %s', name, url)
            pass
