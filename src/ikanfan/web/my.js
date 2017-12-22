noLogin = 'yes';
function checkcookie() {
    return document.cookie.indexOf("auth=") >= 0 ? !0 : !1
}
function Play(a, b) {
    var c = !1;
    html = "", a.indexOf("@@") > 0 && (data = a.split("@@"), b = data[1], a = data[0], c = "free" === data[2] ? !0 : !1), -1 != a.indexOf(".html") || -1 != a.indexOf(".shtml") || -1 != a.indexOf(".htm") ? "47ks" === b ? (localStorage.ckplayer = 1, html = Player.jiexiUrl(Player.jxUrl(a, b, c, NextWebPage, Sid), 495)) : "flvsp" === b ? (localStorage.ckplayer = 1, html = Player.jiexiUrl(Player.jxUrl(a, b, c, NextWebPage, Sid), 495)) : "full" === b ? (localStorage.ckplayer = 1, html = Player.jiexiUrl(a, 495)) : (localStorage.ckplayer = 0, Player.HTML(a)) : -1 != a.indexOf(".mp4") ? (localStorage.ckplayer = 0, Player.H5(a)) : (playStyle = (Player.isMobile() ? !0 : checkcookie() ? !0 : !1) || c || "ck" === data[2] || -1 != window.location.search.indexOf("99496.com") || "play" === noLogin || "acku" === b || "sina" === b || "letvsaas" === b || "mmsid" === b || "huya" === b || "mgtv" === b || "qqmtv" === b || "ppbox" === b || "kankan" === b || "toutiao" === b || "weibo" === b || "miaopai" === b || "56" === b || "1905" === b || "17173" === b || "meipai" === b || "kuaishou" === b || "file" === b || "bilibilick" === b || "kuvod" === b || 2 === a.split(",").length && "tudou" === b ? !0 : !1, "bilibili" === b || 1 === parseInt(data[2]) || "vip" === noLogin || "acfun" === b ? Player.isJump(a, b) : playStyle && 1 !== parseInt(data[2]) && "vip" != noLogin ? (localStorage.ckplayer = 1, html = Player.jiexiUrl(Player.jxUrl(a, b, c, NextWebPage, Sid), 495)) : Player.isJump(a, b)), html && $(".playerbox").html(html), Player.isMobile() || ($(".play-box").height(parseInt(localStorage.ckplayer) ? h - 40 : h), listHeight())
}
function listHeight() {
    pv.indexOf(".mp4") > 0 ? $(".tab-main").height(h - 142) : parseInt(localStorage.ckplayer) ? $(".tab-main").height(h - 150) : $(".tab-main").height(h - 110)
}
function closefull() {
    $(".play-box").removeClass("full"), $(".webexit").remove(), $(".gbtn").show(), $("#cs_right_bottom, #ft_couplet_right, #ft_couplet_left").show(), $("body,#tudou,#tudou2,#iqiyi,#flashBox,#mp4,#ckplayer").attr("style", ""), $("#tudoudiv").css({
        overflow: "hidden",
        height: h + "px"
    }), $(".play-box").css("height", parseInt(localStorage.ckplayer) ? h - 40 : h), listHeight(), localStorage.isOpen = 0
}
function openfull() {
    $(".play-box").addClass("full"), $(".gbtn").hide(), $("#cs_right_bottom, #ft_couplet_right, #ft_couplet_left").hide(), $("body").css("overflow", "hidden").append('<span class="webexit">退出全屏</span>'), $("#flashBox,#iqiyi,#mp4,#ckplayer").css({
        position: "absolute",
        height: "100%",
        "z-index": 99
    }), $("#tudoudiv,.play-box").attr("style", ""), listHeight(), localStorage.isOpen = 1
}
function closefull() {
    $(".play-box").removeClass("full"), $(".webexit").remove(), $(".gbtn").show(), $("#cs_right_bottom, #ft_couplet_right, #ft_couplet_left").show(), $("body,#tudou,#tudou2,#iqiyi,#flashBox,#mp4,#ckplayer").attr("style", ""), $("#tudoudiv").css({
        overflow: "hidden",
        height: h + "px"
    }), $(".play-box").css("height", parseInt(localStorage.ckplayer) ? h - 40 : h), listHeight(), localStorage.isOpen = 0
}
function openfull() {
    $(".play-box").addClass("full"), $(".gbtn").hide(), $("#cs_right_bottom, #ft_couplet_right, #ft_couplet_left").hide(), $("body").css("overflow", "hidden").append('<span class="webexit">退出全屏</span>'), $("#flashBox,#iqiyi,#mp4,#ckplayer").css({
        position: "absolute",
        height: "100%",
        "z-index": 99
    }), $("#tudoudiv,.play-box").attr("style", ""), listHeight(), localStorage.isOpen = 1
}
function listHeight() {
    pv.indexOf(".mp4") > 0 ? $(".tab-main").height(h - 142) : parseInt(localStorage.ckplayer) ? $(".tab-main").height(h - 150) : $(".tab-main").height(h - 110)
}
var Player, html = "", purl = "", pvars = "", data = [], vid = "", h = 535, pv = playConfig.pv,
    playname = playConfig.playname, playJx = playConfig.ckUrl, NextWebPage = playConfig.NextWebPage;
localStorage.ckplayer = 0, Player = {
    isMobile: function () {
        var a = navigator.userAgent, b = a.match(/(iPad).*OS\s([\d_]+)/), c = !b && a.match(/(iPhone\sOS)\s([\d_]+)/),
            d = a.match(/(Android)\s+([\d.]+)/), e = c || d;
        return e ? !0 : !1
    }, ck: function (a, b, c) {
        return c || "tudou" === a ? "https://api.flvsp.com/?type=" + a + "&vid=" + b : "flvsp" === a ? "https://api.flvsp.com/?url=" + b : "47ks" === a ? "https://api.47ks.com/webcloud/?v=&url=" + b : playJx + a + "&vid=" + b
    }, rePlayUrl: function (a, b, c) {
        var f, d = "", e = "";
        switch (-1 != a.indexOf("@@") && (data = a.split("@@"), b = data[1], a = data[0]), b) {
            case"tudou":
                data = a.split(","), f = data.length, 1 === f ? (d = a, e = "youku") : 2 === f ? (d = data[0], e = "tudou") : 3 === f && (d = data[2], e = "youku");
                break;
            case"youku":
                data = a.split(","), e = "youku", d = 3 === data.length ? data[2] : a;
                break;
            case"letv":
                data = a.split(","), e = 1 === data.length ? "letv" : "letvcloud", d = 1 === data.length ? a : data[1] + ":" + data[0];
                break;
            case"letvyun":
                data = a.split(","), e = "letvcloud", d = data[1] + ":" + data[0];
                break;
            case"iqiyi":
                e = "iqiyi", d = -1 != a.indexOf("&tvid=") ? a.split("&tvid=")[1] + "," + a.split("&tvid=")[0] : a;
                break;
            case"sohu":
                data = a.split("_"), d = 2 === data.length ? data[0] : a, e = 2 === data.length ? "mysohu" : b;
                break;
            case"pptv":
                data = a.split(","), d = 2 === data.length ? data[0] : a, e = b;
                break;
            case"acfun":
                data = -1 != a.indexOf("ab") ? a.split("ab")[1].split(",") : a.split(","), d = 2 === data.length ? "http://www.acfun.cn/v/" + (-1 != a.indexOf("ab") ? "ab" : "ac") + data[0] + "_" + data[1] : "http://www.acfun.cn/v/" + (-1 != a.indexOf("ab") ? "ab" + data[0] + "_1" : "ac" + a), e = b;
                break;
            default:
                d = a, e = b
        }
        return this.ck(e, d, c)
    }, isJump: function (a, b) {
        switch (b) {
            case"youku":
                this.youku(a);
                break;
            case"tudou":
                this.tudou(a);
                break;
            case"iqiyi":
                this.iqiyi(a);
                break;
            case"viqiyi":
                this.iqiyi(a);
                break;
            case"letv":
                this.letv(a);
                break;
            case"letvyun":
                this.letv(a);
                break;
            case"sohu":
                this.sohu(a);
                break;
            case"pptv":
                this.pptv(a);
                break;
            case"qq":
                this.qq(a);
                break;
            case"bilibili":
                this.bilibili(a);
                break;
            case"acfun":
                this.acfun(a)
        }
    }, HTML: function (a) {
        html = this.isMobile() ? '<a class="html" target="_blank" href="' + a + '">点击播放</a>' : '<div class="explaywrap" style="height:' + h + 'px;"><a target="_blank" href="' + a + '">亲，请点我播放</a><p>对不起<br>该视频需要跳转播放<br>请点击上面的按钮哦</p></div>'
    }, H5: function (a) {
        html = this.isMobile() ? '<div class="js-media-player"><video webkit-playsinline class="playheight" autoplay controls src="' + a + '"></video></div>' : '<div class="js-media-player"><video id="mp4" width="100%" height="' + h + '" autoplay controls src="' + a + '"></video></div>'
    }, ykUrl: function (a) {
        return "http://player.youku.com/embed/" + a + "?client_id=08fa721d0f5abf37&autoplay=true"
    }, jiexiUrl: function (a, b) {
        return html = Player.isMobile() ? '<iframe class="playheight" style="height: ' + (-1 != window.location.href.indexOf("article") ? "19.333rem" : "3.6rem") + '" src="' + a + '" frameborder="0" scrolling=no allowfullscreen id="ckplayer"></iframe>' : '<iframe src="' + a + '" width="100%" height="' + b + '" frameborder="0" scrolling=no allowfullscreen id="ckplayer"></iframe>'
    }, jxUrl: function (a, b, c, d, e) {
        return jiexiUrl = Player.rePlayUrl(a, b, c) + (-1 != Player.rePlayUrl(a, b, c).indexOf("flvsp") ? "&next=" : "&nextPage=") + (1 === parseInt(e) ? "0" !== d ? window.location.origin + d : "" : "") + "&hd=3&userlink=" + window.location.href
    }, tdUrl: function (a) {
        this.isMobile() ? purl = "http://www.tudou.com/programs/view/html5embed.action?type=0&code=" + a + "&lcode=&resourceId=0_06_05_99" : html = '<embed width="100%" height="100%" id="youku" src="http://www.tudou.com/v/' + a + '/&withRecommendList=false&videoClickNavigate=false&withSearchBar=false&withRecommendList=false/v.swf&totalTime=1&autoPlay=true" wmode="transparent" flashvars="" allowfullscreen="true" type="application/x-shockwave-flash">'
    }, iframe: function (a) {
        html = this.isMobile() ? '<iframe class="playheight" src="' + a + '" frameborder="0" scrolling=no allowfullscreen></iframe>' : '<iframe src="' + a + '" width="100%" scrolling="no" height="' + h + '" frameborder="0" scrolling=no allowfullscreen id="ckplayer"></iframe>'
    }, flash: function (a, b) {
        html = '<object id="flashBox" height="' + h + '" style="visibility:visible;" width="100%" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"><param value="' + a + '"><param value="high" name="quality"><param value="never" name="allowScriptAccess"><param value="true" name="allowFullScreen"><param value="' + b + '" name="flashvars"><param value="transparent" name="wmode"><embed id="flashBox" height="' + h + '" allowscriptaccess="never" style="visibility:visible;" pluginspage="http://get.adobe.com/cn/flashplayer/" flashvars="' + b + '" width="100%" allowfullscreen="true" quality="high" src="' + a + '" type="application/x-shockwave-flash" wmode="transparent"></object>'
    }, tudou: function (a) {
        data = a.split(",");
        var b = data.length;
        1 === b ? this.youku(a) : 2 === b ? this.tdUrl(data[1]) : b >= 3 && this.youku(data[2])
    }, youku: function (a) {
        data = a.split(","), this.iframe(this.ykUrl(3 === data.length ? data[2] : a))
    }, iqiyi: function (a) {
        var e, b = this.isMobile() ? "&tvid=" : "&tvId=", c = "", d = this;
        a.indexOf(",") > 0 ? (data = a.split(","), vid = data[1] + b + data[0], c = data[0]) : a.indexOf("&tvid=") > 0 ? (data = a.split("&tvid="), vid = data[0] + b + data[1], c = data[1]) : a.indexOf("_") > 0 && (data = a.split("_"), vid = data[1] + b + data[0], c = data[0]), "vip" === noLogin ? (e = "//www.ikanfan.cn/api/iqiyi-id.php?pid=" + c, $.getJSON(e, function (a) {
            d.HTML(a.data.videoUrl), $(".playerbox").html(html)
        })) : this.isMobile() ? (purl = "http://m.iqiyi.com/shareplay.html?vid=" + vid + "&coop=coop_117_9949&cid=qc_105102_300452&bd=1&autoplay=1&fullscreen=1", this.iframe(purl)) : (purl = "http://www.iqiyi.com/common/flashplayer/20170406/1556f98c2359.swf?menu=false&autoplay=true&cid=qc_100001_100100&flashP2PCoreUrl=http://www.iqiyi.com/common/flashplayer/20170406/15562a1b82aa.swf&=undefined&&definitionID=" + vid + "&isPurchase=0&cnId=4&coop=ugc_openapi_wanyouwang&cid=qc_100001_300089&bd=1&autoChainPlay=1&showRecommend=0&source=&purl=&autoplay=true", pvars = "", this.flash(purl, pvars))
    }, letv: function (a) {
        data = a.split(",");
        var b = data.length;
        this.isMobile() ? (1 == b ? purl = "http://minisite.letv.com/tuiguang/index.shtml?vid=" + a + "&ark=76&continuration=0&isPlayerAd=0&auto_play=1&autoplay=1&light=0&extend=0" : 2 == b && (purl = "http://yuntv.letv.com/bcloud.html?uu=" + data[0] + "&vu=" + data[1] + "&auto_play=1&gpcflag=1&width=100%&height=100%"), this.iframe(purl)) : (1 == b ? (purl = "http://player.hz.letv.com/hzplayer.swf/open", pvars = "ark=76&autoplay=1&loadingUrl=undefined&vid=" + a + "&continuration=0&preload=1&autoMute=0&forceCallback=1&barrage=0&camera=0&isHttps=0&p1=1&p2=10&forceCDN=1&lan=cn&region=cn&callbackJs=vjs_callback_148427711492037&hostnamestr=letv") : 2 == b && (purl = "http://yuntv.letv.com/bcloud.swf?uu=" + data[0] + "&vu=" + data[1] + "&auto_play=1&gpcflag=1?" + pvars, pvars = "MMControl=false&MMout=false"), this.flash(purl, pvars))
    }, sohu: function (a) {
        var b, c, d;
        a.indexOf("_") > 0 ? (data = a.split("_"), purl = this.isMobile() ? "http://tv.sohu.com/upload/static/play/iplay.html?&bid=" + data[0] + "&autoplay=true&h5=true&src=11510001&lqd=24352&dlBanner=true&hotVideo=true" : "http://share.vrs.sohu.com/my/v.swf&topBar=0&id=" + data[0] + "&skinNum=1&showRecommend=0&autoplay=true&api_key=b24ab6248dace426097bb7b35df84c7c&sogouBtn=0", this.isMobile() ? this.iframe(purl) : this.flash(purl, pvars)) : (b = (new Date).getTime(), c = Math.floor(3.268 * b), d = Math.floor(2.5 * a), purl = this.isMobile() ? "http://hot.vrs.sohu.com/ipad" + a + "_" + c + "_" + d + ".m3u8?plat=null&prod=app" : "http://share.vrs.sohu.com/" + a + "/v.swf&skinNum=1&topBar=0&showRecommend=0&autoplay=true&api_key=b24ab6248dace426097bb7b35df84c7c&sogouBtn=0", this.isMobile() ? this.H5(purl) : this.flash(purl, pvars))
    }, pptv: function (a) {
        data = a.split(","), this.isMobile() ? (purl = "http://m.pptv.com/show/" + data[0] + ".html?rcc_src=P5", this.HTML(purl)) : (purl = "http://player.pptv.com/iframe/index.html?ctx=o=v_share#id=" + data[0], html = '<iframe id="flashBox" src="' + purl + '" allowtransparency="true" width="100%" height="' + h + '" scrolling="no" frameborder="0" ></iframe>')
    }, qq: function (a) {
        this.isMobile() ? (purl = "http://v.qq.com/iframe/player.html?vid=" + a + "&tiny=0&auto=1", this.iframe(purl)) : (purl = "https://imgcache.qq.com/tencentvideo_v1/playerv3/TPout.swf", pvars = "vid=" + a + "&tpid=0&showend=1&showcfg=1&searchbar=1&shownext=1&list=2&autoplay=0&bullet=0&showlogo=0&searchpanel=0&showend=0&showcfg=0&autoplay=1&follow=0&clientbar=0", this.flash(purl, pvars))
    }, bilibili: function (a) {
        data = a.split(","), purl = 2 === data.length ? "http://www.bilibili.com/video/av" + data[0] + "/index" + data[1] + ".html" : "http://www.bilibili.com/video/av" + a + "/", this.HTML(purl)
    }, acfun: function (a) {
        var b, c;
        -1 != a.indexOf("ab") ? (data = a.split("ab"), b = data[1].split(","), vid = 2 === b.length ? b[0] + "_" + b[1] : data[1]) : (data = a.split(","), c = data.length, vid = 2 == c ? data[0] + "_" + data[1] : a), this.isMobile() ? (purl = "http://m.acfun.cn/v/?" + (-1 != a.indexOf("ab") ? "ab" : "ac") + "=" + vid, this.HTML(purl)) : (purl = "http://www.acfun.cn/v/" + (-1 != a.indexOf("ab") ? "ab" : "ac") + vid, this.HTML(purl))
    }
}, playname && "" != playname && pv && "" != pv ? Play(pv, playname) : window.location.href = window.location.origin, Player.isMobile() || ($(document).on("click", ".webexit,.websize,.webfullbtn", function () {
    $(".play-box").hasClass("full") ? closefull() : openfull()
}), $(document).on("dblclick", ".playbg", function () {
    $(".play-box").hasClass("full") ? closefull() : openfull()
}), $(document).keydown(function (a) {
    var b = a.keyCode ? a.keyCode : a.which;
    (27 == b || 96 == b) && closefull()
}), $(function () {
    -1 != window.location.href.indexOf("/ac/") && 1 === parseInt(localStorage.isOpen) && openfull(), listHeight();
    var a = null;
    $(".play-box").hover(function () {
        clearTimeout(a), $(".webexit").show()
    }, function () {
        a = setTimeout(function () {
            $(".webexit").hide()
        }, 3e3)
    })
}));