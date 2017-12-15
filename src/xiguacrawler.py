# coding: utf-8

import sys
import time
import random
import base64
import traceback
import execjs
import json
import requests

'''
本爬虫的目标为西瓜(www.ixigua.com)主页的视频获取,
仅供学习研究.
'''

FAKE_HEADER = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari / 537.36'
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


class VideoInf(object):
    def __init__(self):
        self.title = None
        self.description = None
        self.tag = None
        self.author = None
        self.video_id = None
        self.watched_num = None
        self.access_url = None
        self.duration = None
        self.cover = None
        self.video_url = None

    def __repr__(self):
        raw = {
            'title': self.title,
            'desc': self.description,
            'author': self.author,
            'tag': self.tag,
            'id': self.video_id,
            'count': self.watched_num,
            'page': self.access_url,
            'time': self.duration,
            'cover': self.cover,
            'video': self.video_url
        }
        s = 'error'
        try:
            s = json.dumps(raw, ensure_ascii=False, indent=2).encode('utf-8')
        except:
            traceback.print_exc()
            sys.stderr.write(repr(raw))
        return s


class XiGuaCrawler(object):
    Category = ['video_new', 'subv_funny', 'subv_society', 'subv_comedy', 'subv_life', 'subv_movie',
                'subv_entertainment',
                'subv_cute', 'subv_game', 'subv_boutique', 'subv_broaden_view']

    def __init__(self):
        self.domain = 'https://www.ixigua.com'
        self.start_url = 'https://www.ixigua.com/api/pc/feed/' \
                         '?min_behot_time=0&category={}&utm_source=toutiao&widen=1&tadrequire=true' \
                         '&as=479BB4B7254C150&cp=7E0AC8874BB0985'
        self.next_url = 'https://www.ixigua.com/api/pc/feed/' \
                        '?max_behot_time={}&category={}&utm_source=toutiao&widen=1&tadrequire=true&' \
                        'as=479BB4B7254C150&cp=7E0AC8874BB0985'
        self.safe_host = 'https://ib.365yg.com'
        self.safe_path = '/video/urls/v/1/toutiao/mp4/'
        self.ctx = execjs.compile(JS_CODE)
        self.raw_content = []
        self.callback_prefix = 'tt_player'
        self.session = requests.session()
        self.existed_video_id = set()
        self.video_items = []
        self.video_num_required = 1500

    def run(self):
        for item in self.Category:
            sys.stderr.write(item + '\n')
            self._run(item)
        print crawler.video_items
        with open('xigua.txt', 'w') as f:
            f.write('\n'.join(self.raw_content))

    def _run(self, category):
        time.sleep(random.randint(1, 10) * 0.1)
        r = self.session.get(self.start_url.format(category), headers=FAKE_HEADER)
        try:
            self.raw_content.append(r.content)
            obj = json.loads(r.content)
            next_tag = obj['next']['max_behot_time']
            self.extract_video(obj['data'], category)
            for i in range(5):
                next_tag, continue_run = self.go_next(next_tag, category)
                if not continue_run or not next_tag:
                    break
        except:
            traceback.print_exc()

    def go_next(self, next_tag, category):
        '''
        :return: next tag, continue?
        '''
        time.sleep(random.randint(1, 5) * 0.1)
        r = None
        try:
            r = self.session.get(self.next_url.format(next_tag, category), headers=FAKE_HEADER)
            self.raw_content.append(r.content)
            obj = json.loads(r.content)
            next_tag = obj['next']['max_behot_time']
            return next_tag, self.extract_video(obj['data'], category)
        except:
            if r:
                print r.content
            traceback.print_exc()
            return None, True

    def extract_video(self, data, category):
        '''
        :return: continue? True/False
        '''
        for item in data:
            if item['has_video']:
                vi = VideoInf()
                vi.title = item['title']
                vi.description = item.get('abstract', '无')
                vi.tag = category
                vi.author = item['source']
                vi.video_id = item['video_id']
                vi.watched_num = item['video_play_count']
                vi.access_url = self.domain + item['source_url']
                vi.duration = item['video_duration_str']
                vi.cover = item['image_url']
                vi.video_url = self.request_for_real_video(vi.video_id)
                if vi.video_url.find('Expires') > 0 or vi.video_id in self.existed_video_id:
                    sys.stderr.write("video exist.\n" if vi.video_id in self.existed_video_id else
                                     "video url has expire time limit.\n")
                    continue
                if not vi.video_url:
                    sys.stderr.write('cannot get url.\n')
                    continue
                self.existed_video_id.add(vi.video_id)
                self.video_items.append(vi)
                sys.stderr.write(str(len(self.video_items)) + '\n')
                # if len(self.video_items) >= self.video_num_required:
                #     sys.stderr.write('num accessed.')
                #     return False
        return True

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


if __name__ == '__main__':
    crawler = XiGuaCrawler()
    crawler.run()
