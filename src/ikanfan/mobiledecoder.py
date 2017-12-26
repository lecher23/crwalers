# coding: utf-8
import re
import requests
from bs4 import BeautifulSoup

PARTS = [
    '''<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>
<title>player</title>
<style type="text/css">body,html,div{background-color:#000;padding: 0;margin: 0;width:100%;height:100%;color:#aaa;}</style>
</head>
<body>
<div id="player"></div>
<script type="text/javascript" src="ckplayer.js"></script>
<script src="https://cdn.bootcss.com/jquery/2.2.4/jquery.min.js"></script>
<script type="text/javascript">''',
    None,
    '''
        function GetQueryString(name){
        var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if(r!=null)return  unescape(r[2]); return null;
    }
	function nextxia(){
        var nextPage = GetQueryString('nextPage');
        var userlink = GetQueryString('userlink');
        if(nextPage != null && nextPage != ''){
            window.location.href = nextPage;
        }else{
            alert('最后一集了,点击确定,返回首页');
            window.location.href = userlink.split('ac')[0];
        }
    }
    function playerstop(){
        nextxia();
        return false;
    };
</script>
</body>
</html>'''
]


class MobileDecoder(object):
    def __init__(self):
        self.domain = 'http://m.ikanfan.com'
        self.api_domain = 'https://www.ikanfan.cn'
        self.get_script_ptn = re.compile(r"\$\.getScript\('(.*?)'\)")
        self.video_api_ptn = re.compile(r"\{\s*url:\s*'(.*?)',")

    def run(self, cur_page_path, next_page_path, video_type, video_id, hd="3"):
        ss = requests.session()
        cur_page_url = self.domain + cur_page_path
        headers = {
            "referer": cur_page_url, "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}
        params = 'type={}&vid={}&nextPage={}&hd={}&userlink={}'.format(
            video_type, video_id, self.domain + next_page_path, hd, cur_page_url)
        target_url = self.api_domain + '/api/play.php?' + params
        print 'requests: ', target_url
        r = ss.get(target_url, headers=headers)
        # html = BeautifulSoup(r.content, 'html5lib')
        script = self.get_script_ptn.findall(r.content)
        if script:
            parse_path = script[0]
            parse_url = self.api_domain + parse_path
            headers['refer'] = target_url
            r = ss.get(parse_url, headers=headers)
            with open('web/test.html', 'w') as f:
                f.write(PARTS[0])
                f.write(r.content)
                f.write(PARTS[2])

    def get_iqiyi_data(self, html, headers, session):
        video_api_ret = self.video_api_ptn.findall(html)
        if video_api_ret:
            video_api = video_api_ret[0]
            headers.pop('refer')
            iqiyi_url = 'https:' + video_api
            iqiyi_url = iqiyi_url.replace('callback=?', 'callback=tmtsCallback')
            r = session.get(iqiyi_url, headers=headers)
            print r.content


if __name__ == '__main__':
    md = MobileDecoder()
    md.run('/ac/33557/0-10.html', '/ac/33557/0-11.html', 'iqiyi', '860917500_dc0dd43fde7f4323e29a1e8de19443b1')
