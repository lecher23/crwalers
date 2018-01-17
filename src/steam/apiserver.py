# coding: utf-8

import sys
import json
import logging
import tornado.ioloop
import tornado.web
import tornado.gen
from steam import SteamOnlineNumber
from tornado.httpclient import AsyncHTTPClient

online_info = None


class ApiHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        start = int(self.get_argument('i', 0))
        size = int(self.get_argument('n', 10))
        self.write(json.dumps({
            "err": 0,
            "data": [
                {
                    "name": name,
                    "cur": current,
                    "top": top
                } for name, current, top in online_info[start:start + size]]}, ensure_ascii=False))


@tornado.gen.coroutine
def timer():
    son = SteamOnlineNumber()
    result = yield AsyncHTTPClient().fetch(son.page_url)
    if result.code != 200:
        logging.warning('bad status code %s from: %s', result.code, son.page_url)
    else:
        global online_info
        online_info = son.do(result.body)


def main():
    ioloop = tornado.ioloop.IOLoop.current()

    app = tornado.web.Application([(r'/api/steam/v1', ApiHandler)])
    app.listen(int(sys.argv[1]))

    ioloop.add_callback(timer)
    pc = tornado.ioloop.PeriodicCallback(timer, 5 * 60 * 1000)
    pc.start()

    ioloop.start()


if __name__ == '__main__':
    main()
