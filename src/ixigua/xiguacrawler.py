# coding: utf-8

import sys
import time
import random
import base64
import traceback
import execjs
import json
import requests
from model import XiguaVideo, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

'''
本爬虫的目标为西瓜(www.ixigua.com)主页的视频获取,
仅供学习研究.
'''

FAKE_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/63.0.3239.132 Mobile '
                  'Safari/537.36',
    'Cookie': 'ga=GA1.2.823218264.1513223558; '
              'UM_distinctid=16053271a2c859-004ee0b19e4a99-1e291c08-1fa400-16053271a2de9c; '
              'tt_webid=6499645204017006093; _gid=GA1.2.1699261817.1516155589; '
              'csrftoken=51196fbec3ee4e394fda74b587b6b6d7; '
              '_ba=BA0.2-20171214-51225-RZ5Kc2AUchxxHtIgLAMo'
}

JS_CODE = '''function encodeURL(pathname, randomStr) {
  var n = function () {
    for (var t = 0, e = new Array(256), n = 0; 256 != n; ++n)t = n, t = 1 & t ? -306674912 ^ t >>> 1 : t >>> 1, t = 1 & t ? -306674912 ^ t >>> 1 : t >>> 1, t = 1 & t ? -306674912 ^ t >>> 1 : t >>> 1, t = 1 & t ? -306674912 ^ t >>> 1 : t >>> 1, t = 1 & t ? -306674912 ^ t >>> 1 : t >>> 1, t = 1 & t ? -306674912 ^ t >>> 1 : t >>> 1, t = 1 & t ? -306674912 ^ t >>> 1 : t >>> 1, t = 1 & t ? -306674912 ^ t >>> 1 : t >>> 1, e[n] = t;
  return "undefined" != typeof Int32Array ? new Int32Array(e) : e
  }(), o = function (t) {
    for (var e, o, r = -1, i = 0, a = t.length; i < a;)e = t.charCodeAt(i++), e < 128 ? r = r >>> 8 ^ n[255 & (r ^ e)] : e < 2048 ? (r = r >>> 8 ^ n[255 & (r ^ (192 | e >> 6 & 31))], r = r >>> 8 ^ n[255 & (r ^ (128 | 63 & e))]) : e >= 55296 && e < 57344 ? (e = (1023 & e) + 64, o = 1023 & t.charCodeAt(i++), r = r >>> 8 ^ n[255 & (r ^ (240 | e >> 8 & 7))], r = r >>> 8 ^ n[255 & (r ^ (128 | e >> 2 & 63))], r = r >>> 8 ^ n[255 & (r ^ (128 | o >> 6 & 15 | (3 & e) << 4))], r = r >>> 8 ^ n[255 & (r ^ (128 | 63 & o))]) : (r = r >>> 8 ^ n[255 & (r ^ (224 | e >> 12 & 15))], r = r >>> 8 ^ n[255 & (r ^ (128 | e >> 6 & 63))], r = r >>> 8 ^ n[255 & (r ^ (128 | 63 & e))]);
    return r ^ -1
    }, r = pathname + "?r=" + Math.random().toString(10).substring(2);
  "/" != r[0] && (r = "/" + r);
  var i = o(r) >>> 0;
  return r + "&s=" + i
}'''


class XiGuaCrawler(object):
    Category = ['video_new', 'subv_funny', 'subv_society', 'subv_comedy', 'subv_life', 'subv_movie',
                'subv_entertainment',
                'subv_cute', 'subv_game', 'subv_boutique', 'subv_broaden_view']

    def __init__(self):
        self.domain = 'https://m.ixigua.com'
        self.next_url = 'http://m.ixigua.com/list/?' \
                        'tag={}&ac=wap&count=20&format=json_raw&as=479BB4B7254C150&cp=7E0AC8874BB0985&max_behot_time={}'
        self.safe_host = 'https://ib.365yg.com'
        self.safe_path = '/video/urls/v/1/toutiao/mp4/'
        self.ctx = execjs.compile(JS_CODE)
        self.raw_content = []
        self.callback_prefix = 'tt_player'
        self.session = requests.session()
        self.existed_video_id = set()
        self.video_items = []
        self.video_num_required = 1500
        self.page_count = 5

        self.engine = create_engine(
            'mysql+mysqldb://licheng:Cg123456@192.168.0.253:3306/downline?charset=utf8', echo=False)
        self.sql_session = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(self.engine)
        self.enable_db = False

        self.fp = open('xg_resp.txt', 'w')

    def run(self):
        for item in self.Category:
            sys.stderr.write(item + '\n')
            self._run(item)
        with open('xigua.json', 'w') as f:
            f.write(str(self.video_items))

    def _run(self, category):
        time.sleep(random.randint(1, 10) * 0.1)
        url = self.next_url.format(category, 0)
        sys.stderr.write(url + '\n')
        r = self.session.get(url, headers=FAKE_HEADER)
        try:
            start_count = len(self.video_items)
            self.raw_content.append(r.content)
            print r.content
            obj = json.loads(r.content)
            # next_tag = obj['next']['max_behot_time']
            next_tag = self.extract_video(obj['data'], category)
            for i in range(self.page_count):
                next_tag = self.go_next(next_tag, category)
                if not next_tag:
                    break
            end_count = len(self.video_items)
            sys.stderr.write('%s count %s' % (category, end_count - start_count))
        except:
            traceback.print_exc()
            self.fp.write(r.content)

    def go_next(self, next_tag, category):
        '''
        :return: next tag, continue?
        '''
        time.sleep(random.randint(1, 5) * 0.1)
        r = None
        try:
            r = self.session.get(self.next_url.format(category, next_tag), headers=FAKE_HEADER)
            self.raw_content.append(r.content)
            obj = json.loads(r.content)
            return self.extract_video(obj['data'], category)
        except:
            if r:
                self.fp.write(r.content + '\n')
            traceback.print_exc()
            return None

    def extract_video(self, data, category):
        '''
        :return: continue? True/False
        '''
        max_behot_time = 0
        for item in data:
            if item['has_video']:
                vi = XiguaVideo()
                vi.title = item['title']
                vi.description = item.get('abstract', '无')
                vi.tag = category
                vi.author = item['source']
                vi.video_id = item['video_id']
                vi.comment_num = item['comment_count']
                vi.access_url = self.domain + item['source_url']
                vi.duration = item['video_duration']
                vi.cover = item['large_image_url']
                vi.video_url = self.request_for_real_video(vi.video_id)
                if vi.video_id in self.existed_video_id:
                    sys.stderr.write("video exist.\n")
                    continue
                if not vi.video_url:
                    sys.stderr.write('cannot get url.\n')
                    continue
                self.existed_video_id.add(vi.video_id)
                self.video_items.append(vi)
                self._save_item(vi)
                sys.stderr.write(str(len(self.video_items)) + '\n')
                max_behot_time = max(max_behot_time, item.get('behot_time', 0))
                # if len(self.video_items) >= self.video_num_required:
                #     sys.stderr.write('num accessed.')
                #     return False
        return max_behot_time

    def request_for_real_video(self, video_id):
        path = self.sign_url(self.safe_path + video_id)
        cb_suffix = self.random_callback()
        entrance = ''.join([self.safe_host, path, '&callback=', self.callback_prefix, cb_suffix])
        r = None
        try:
            r = requests.get(entrance, headers=FAKE_HEADER)
            body = r.content[len(self.callback_prefix) + len(cb_suffix) + 1: -1]
            obj = json.loads(body)
            for k, v in obj['data']['video_list'].items():
                video_url = v['main_url']
                return base64.b64decode(video_url)
        except:
            traceback.print_exc()
            if r:
                print r.content
            return None

    def sign_url(self, ipt):
        return self.ctx.call('encodeURL', ipt)

    @staticmethod
    def random_callback():
        return ''.join([chr(random.randint(ord('a'), ord('z') + 1)) for _ in range(5)])

    def _save_item(self, item):
        if not self.enable_db:
            return
        try:
            self.sql_session.add(item)
            self.sql_session.flush()
            self.sql_session.commit()
        except:
            traceback.print_exc()
            self.sql_session.rollback()

    def __del__(self):
        self.fp.close()


if __name__ == '__main__':
    crawler = XiGuaCrawler()
    crawler.run()
    # print crawler.request_for_real_video('3dd5aadc36d44abdb11e3cd1cc86259b')
