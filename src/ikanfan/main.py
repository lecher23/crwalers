# coding: utf-8

import json
import random
import logging
import requests
from bs4 import BeautifulSoup
from model import ComicEntry, PlayerEntry, IKanFanDB

HOST = "http://www.ikanfan.com"
INFO_URL = "http://www.ikanfan.com/index.php?s=home-search-pop&q={}&timestamp={}"
HEADERS = {
    'Referer': 'http://www.ikanfan.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}


class IKanFanCrawler(object):
    PAGE_WANTED = 10

    def __init__(self):
        self.comics = []
        self.session = requests.session()
        self.db = IKanFanDB('data/ikanfan.db')

    def run(self):
        category_list = self.get_category()
        for category_name, path in category_list.items():
            for i in range(self.PAGE_WANTED):
                comics = self.get_comic_list(category_name, path, i)
                for comic in comics:
                    self.get_comic_introduce(comic)
                    self.get_video_list(comic)
                    self.process_player_param(comic)
                    self.db.save_comic(comic)
                self.comics.extend(comics)

    def get_category(self):
        h = self._get(HOST)
        nav_div = h.body.find('div', {'class': 'wp mcid'})
        category = {}
        for a in nav_div.children:
            if a['href'].find('index') < 0:
                continue
            category[a.text] = a['href']
        return category

    def get_comic_list(self, category, path, page_idx):
        if page_idx:
            tmp = path.rfind('.')
            path = path[:tmp] + str(page_idx + 1) + path[tmp:]
        h = self._get(HOST + path)
        comics_div = h.find('div', {'id': 'contents'})
        entries = []
        for a in comics_div.children:
            entry = ComicEntry()
            entry.comic_id = a['data-id']
            entry.page_path = a['href']
            entry.name = a['title']
            entry.cover = a.div.img['data-original']
            entry.tag = a.p.text
            entry.category = category
            logging.warning('get comic %s done.', entry.name)
            entries.append(entry)
        return entries

    def get_comic_introduce(self, entry):
        url = INFO_URL.format(entry.comic_id, random.random())
        r = requests.get(url)
        obj = json.loads(r.content)
        if obj['status'] == 1:
            data = obj['data'][0]
            entry.introduce = data['content']
            entry.score = int(float(data['gold']) * 10)

    def get_video_list(self, entry):
        h = self._get(HOST + entry.page_path)
        list_div = h.find('div', {'id': 'playlist'})
        for div in list_div.find_all('div', {'class': 'd-play-box'}):
            player_name = div['id']
            logging.warning('get player list for %s', player_name)
            a_list_div = div.find('div', {'class': 'd-player-list clearfix looplist'})
            entries = []
            for a in a_list_div.children:
                player_entry = PlayerEntry()
                player_entry.path = a['href']
                player_entry.title = a['title']
                player_entry.idx = a.text
                player_entry.player_type = player_name
                player_entry.comic_id = entry.comic_id
                entries.append(player_entry)
            entry.players[player_name] = entries

    def process_player_param(self, entry):
        for player_entries in entry.players.values():
            for player_entry in player_entries:
                self.get_play_config(player_entry)

    def get_play_config(self, player_entry):
        h = self._get(HOST + player_entry.path)
        play_cfg_div = h.find('div', {'class': 'fl playerbox iframe'})
        player_entry.config_str = play_cfg_div.script.text

    def _get(self, url):
        logging.warning('crawl %s', url)
        r = self.session.get(url, headers=HEADERS)
        return BeautifulSoup(r.content, 'html5lib')


if __name__ == "__main__":
    tool = IKanFanCrawler()
    tool.run()
