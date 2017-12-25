# coding: utf-8

import os
import time
import datetime
import signal
import pickle
import json
import random
import logging
import requests
import threading
from bs4 import BeautifulSoup
from model import ComicEntry, PlayerEntry, IKanFanDB
from concurrent.futures import ThreadPoolExecutor

HOST = "http://www.ikanfan.com"
INFO_URL = "http://www.ikanfan.com/index.php?s=home-search-pop&q={}&timestamp={}"
HEADERS = {
    'Referer': 'http://www.ikanfan.com/',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}


def init_logging_config(log_path):
    from logging import root
    root.handlers = []
    logging.basicConfig(
        filename=log_path,
        filemode='w',
        format='%(asctime)s[%(levelname)s][%(filename)s:%(lineno)d]<%(thread)d>:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )


class IKanFanCrawler(object):
    PAGE_WANTED = 10

    def __init__(self):
        self.comics = []
        self.session = requests.session()
        self.db = IKanFanDB('data/ikanfan.{}.db'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
        self._processed = set()
        self._lock = threading.Lock()
        self._progress_file = 'data/ikanfan.his'
        self.stop = False

    def run(self):
        if os.path.exists(self._progress_file):
            with open(self._progress_file, 'rb') as f:
                self._processed = pickle.loads(f.read())
                logging.info('processed info: %s', self._processed)
        category_list = self.get_category()
        with ThreadPoolExecutor(len(category_list)) as thread_pool:
            for category_name, path in category_list.items():
                thread_pool.submit(self.do_category_task, category_name, path)
        with open(self._progress_file, 'wb') as f:
            f.write(pickle.dumps(self._processed))

    def do_category_task(self, category_name, path):
        logging.info('start task: %s(%s)', category_name, path)
        page_processed = 0
        task_session = requests.session()
        while page_processed < self.PAGE_WANTED and path and not self.stop:
            unified_tag = '{}-{}'.format(category_name.encode('utf-8'), path)
            if unified_tag in self._processed:
                logging.warning('%s processed, jump!', unified_tag)
                continue
            comics, path = self.get_comic_list(category_name, path, task_session)
            for comic in comics:
                if self.stop:
                    logging.info('end task: %s(%s)', category_name, path)
                    return True
                try:
                    self.get_comic_introduce(comic, task_session)
                    self.get_video_list(comic, task_session)
                    self.process_player_param(comic, task_session)
                except:
                    logging.warning('get comic info: %s failed.', comic.comic_id)
                else:
                    self.db.save_comic(comic)
            with self._lock:
                self._processed.add(unified_tag)
            page_processed += 1
        logging.info('end task: %s(%s)', category_name, path)
        return True

    def get_category(self):
        h = self._get(HOST)
        nav_div = h.body.find('div', {'class': 'wp mcid'})
        category = {}
        for a in nav_div.children:
            if a['href'].find('index') < 0:
                continue
            category[a.text] = a['href']
        return category

    def get_comic_list(self, category, path, session):
        entries = []
        next_path = False
        try:
            h = self._get(HOST + path, session)
            comics_div = h.find('div', {'id': 'contents'})
            for a in comics_div.children:
                entry = ComicEntry()
                entry.comic_id = a['data-id']
                entry.page_path = a['href']
                entry.name = a['title']
                entry.cover = a.div.img['data-original']
                entry.tag = a.p.text
                entry.category = category
                logging.info('get comic %s done.', entry.name)
                entries.append(entry)
            page_ul = h.find('ul', {'class': 'pagination'})
            for li in page_ul.find_all('li'):
                if 'active' in li.get('class', []):
                    next_path = True
                    continue
                if next_path:
                    a = getattr(li, 'a', None)
                    next_path = None
                    if a and a.text.isdigit():
                        next_path = li.a['href']
                    break
        except:
            logging.warning('get comic list from %s with category %s failed', path, category)
        return entries, next_path

    def get_comic_introduce(self, entry, session):
        url = INFO_URL.format(entry.comic_id, random.random())
        r = session.get(url)
        obj = json.loads(r.content)
        if obj['status'] == 1:
            data = obj['data'][0]
            entry.introduce = data['content']
            entry.score = int(float(data['gold']) * 10)

    def get_video_list(self, entry, session):
        h = self._get(HOST + entry.page_path, session)
        list_div = h.find('div', {'id': 'playlist'})
        for div in list_div.find_all('div', {'class': 'd-play-box'}):
            player_name = div['id']
            logging.info('get player list for %s', player_name)
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

    def process_player_param(self, entry, session):
        for player_entries in entry.players.values():
            for player_entry in player_entries:
                self.get_play_config(player_entry, session)

    def get_play_config(self, player_entry, session):
        h = self._get(HOST + player_entry.path, session)
        play_cfg_div = h.find('div', {'class': 'fl playerbox iframe'})
        player_entry.config_str = play_cfg_div.script.text

    def shutdown(self):
        if not self.stop:
            print('prepare stop.')
            self.stop = True
        else:
            print('stopping...')

    def _get(self, url, session=None):
        if self.stop:
            raise RuntimeError('crawler already stopped.')
        logging.info('crawl %s', url)
        r = session.get(url, headers=HEADERS) if session else self.session.get(url, headers=HEADERS)
        return BeautifulSoup(r.content, 'html5lib')


if __name__ == "__main__":
    init_logging_config('/tmp/ikanfan.log')
    tool = IKanFanCrawler()
    signal.signal(signal.SIGINT, lambda sig, frame: tool.shutdown())
    print 'start crawler, you can press Ctrl + c  stop it.'
    tool.run()
