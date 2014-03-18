#!/usr/bin/env python
#coding=utf8

import os
import sys
import urllib
import urllib2
import cookielib
import base64
import re
import hashlib
import json
import rsa
import binascii
import db


reload(sys)
sys.setdefaultencoding('utf-8')


def crawl_by_uid(uid, username, pwd):
    if login(username, pwd):
        print 'Login WEIBO succeeded'
    else:
        print 'Login WEIBO failed'
        return None

    get_weibo_relation(uid)



def auto_crawl(username, pwd):
    if login(username, pwd):
        print 'Login WEIBO succeeded'
    else:
        print 'Login WEIBO failed'
        return None

    users = db.get_none_crawl_user()
    if users:
        for user in users:
            get_weibo_relation(user[0])


def get_self_weibo_relation(username, pwd):
    if login(username, pwd):
        print 'Login WEIBO succeeded'
    else:
        print 'Login WEIBO failed'
        return None

    #测试读取数据，下面的URL，可以换成任意的地址，都能把内容读取下来
    url = 'http://weibo.com'
    u = urllib2.urlopen(url)
    redirectUrl = u.geturl()
    match = re.compile(u'/\d+/')
    searchResult = re.search(match, redirectUrl)
    selfUid = searchResult.group(0)[1:-1]

    req = urllib2.Request(url='http://weibo.com/'+selfUid+'/myfollow',)
    result = urllib2.urlopen(req)
    text = result.read().decode('utf-8')
    # text = result.read()

    # 为了拿到自己的 昵称 总关注数目 总粉丝数
    match = re.compile(u'class="gn_name" target="_top" title="[\s\S]*?"')
    searchResult = re.search(match, text)
    selfNick = searchResult.group(0)[37:-1]

    match = re.compile(u'全部关注\(\d+\)')
    searchResult = re.search(match, text)
    follows = searchResult.group(0)[5:-1]

    match = re.compile(u'粉丝\(\d+\)')
    searchResult = re.search(match, text)
    fans = searchResult.group(0)[3:-1]

    # 把自己加到数据库中
    db.add_user_to_db(selfUid, selfNick, follows, fans)

    match = re.compile(u'uid=\d+')
    rawlv2 = re.findall(match, text)
    uidList = {}.fromkeys(rawlv2).keys()
    uidList.remove('uid='+selfUid)

    currentPageNum = 1
    while len(uidList) < int(follows):
        print currentPageNum, len(uidList)
        match = re.compile(u'下一页')
        rawlv2 = re.findall(match, text)
        result = {}.fromkeys(rawlv2).keys()
        if len(result) > 0:
            currentPageNum += 1
            req = urllib2.Request(url='http://weibo.com/'+selfUid+'/myfollow?t=1&page='+str(currentPageNum),)
            result = urllib2.urlopen(req)
            text = result.read().decode('utf-8')

            match = re.compile(u'uid=\d+')
            rawlv2 = re.findall(match, text)
            uidList += {}.fromkeys(rawlv2).keys()
            uidList.remove('uid='+selfUid)
        else: break

    print 'len(uidList)=',len(uidList)
    uidList = get_real_uid_list(uidList)
    if len(uidList) > 0:
        for uid in uidList:
            db.add_relation_to_db(selfUid, uid)
            get_userinfo(uid)
    # 更新自己的 db_follows
    db.update_user_db_follows(selfUid)


def get_userinfo(uid):
    if not db.is_user_in_db(uid):
        req = urllib2.Request(url='http://weibo.com/'+uid+'/follow',)
        result = urllib2.urlopen(req)
        try:
            text = result.read().decode('utf-8')
            match = re.compile(u'<title>[\s\S]*?的微博')
            searchResult = re.search(match, text)
            nick = searchResult.group(0)[7:-3].encode('utf-8')
            # rawlv2 = re.findall(match, text)
            # result = {}.fromkeys(rawlv2).keys()
            # nick = result[0][7:-3].encode('utf-8')

            # 为了拿到总关注数目 和 总粉丝数
            # 匹配 <strong node-type=\"follow\">455<\/strong>\r\n\t\t\t<span>关注 <\/span>\r\n\t\t<\/a>\r\n\t<\/li>\r\n\t<li class=\"follower S_line1\">\r\n\t\t<a class=\"S_func1\" name=\"place\" href=\"\/p\/1005051867684872\/follow?relate=fans&from=100505&wvr=5&mod=headfans\">\r\n\t\t\t<strong node-type=\"fans\">760<\/strong>\r\n\t\t\t<span>粉丝
            match = re.compile(u'<strong[\s\S]*?>粉丝')
            searchResult = re.search(match, text)
            result = searchResult.group(0).encode('utf-8').split('>')
            # rawlv2 = re.findall(match, text)
            # result = {}.fromkeys(rawlv2).keys()[0].encode('utf-8').split('>')
            follows = result[1].split('<')[0]
            fans = result[9].split('<')[0]

            if re.match(r'\d+', fans):
                return db.add_user_to_db(uid, nick, follows, fans)
            else:
                # 有些页面匹配也会出错，先不往数据库中插数据
                print '>>>[Error: get_userinfo]', uid, nick, follows, fans
                # print {}.fromkeys(rawlv2).keys()[0].encode('utf-8')
        except Exception, e:
            # 企业版的比较特殊
            print '>>>[Error: get_userinfo]', uid, e
    return False


def get_weibo_relation(uid):
    if not db.is_user_in_db(uid):
        get_userinfo(uid)

    user = db.query_user(uid)
    if user:
        print user
        try:
            totalFollowsNum = l[2]

            req = urllib2.Request(url='http://weibo.com/'+uid+'/follow',)
            result = urllib2.urlopen(req)
            text = result.read().decode('utf-8')
            match = re.compile(u'uid=\d+')
            rawlv2 = re.findall(match, text)
            uidList = {}.fromkeys(rawlv2).keys()

            currentPageNum = 1
            print currentPageNum, 'uidList=', len(uidList)
            while len(uidList) < totalFollowsNum:
                match = re.compile(u'下一页')
                rawlv2 = re.findall(match, text)
                result = {}.fromkeys(rawlv2).keys()
                if len(result) > 0:
                    req = urllib2.Request(url='http://weibo.com/'+uid+'/follow?page='+str(currentPageNum),)
                    result = urllib2.urlopen(req)
                    text = result.read().decode('utf-8')

                    match = re.compile(u'uid=\d+')
                    rawlv2 = re.findall(match, text)
                    uidList += {}.fromkeys(rawlv2).keys()
                    uidList.remove('uid='+uid)
                    # print currentPageNum, 'len(uidList)=',len(uidList)
                currentPageNum += 1
                print currentPageNum, 'uidList=', len(uidList)
                if currentPageNum > 10: 
                    break

            print 'len(uidList)=',len(uidList)
            uidList = get_real_uid_list(uidList)
            if len(uidList) > 0:
                for u in uidList:
                    db.add_relation_to_db(uid, u)
                    get_userinfo(u)
            # 更新自己的 db_follows
            db.update_user_db_follows(uid)
        except Exception, e:
            print '>>>[Error: get_weibo_relation]', uid, e
        


def get_real_uid_list(uidList):
    for i in range(0, len(uidList)-1):
        uidList[i] = uidList[i][4:]
    return uidList




def get_prelogin_status(username):
    """
    Perform prelogin action, get prelogin status, including servertime, nonce, rsakv, etc.
    """
    #prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&client=ssologin.js(v1.4.5)'
    prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=' + get_user(username) + \
     '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.5)';
    data = urllib2.urlopen(prelogin_url).read()
    p = re.compile('\((.*)\)')
    
    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        rsakv = data['rsakv']
        return servertime, nonce, rsakv
    except:
        print 'Getting prelogin status met error!'
        return None


def login(username, pwd):
    """"
        Login with use name, password and cookies.
        (1) If cookie file exists then try to load cookies;
        (2) If no cookies found then do login
    """
    cookie_file = 'weibo_login_cookies.dat'
    #If cookie file exists then try to load cookies
    if os.path.exists(cookie_file):
        try:
            cookie_jar  = cookielib.LWPCookieJar(cookie_file)
            cookie_jar.load(ignore_discard=True, ignore_expires=True)
            loaded = 1
        except cookielib.LoadError:
            loaded = 0
            print 'Loading cookies error'
        
        #install loaded cookies for urllib2
        if loaded:
            cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
            opener         = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            print 'Loading cookies success'
            return 1
        else:
            return do_login(username, pwd, cookie_file)
    
    else:   #If no cookies found
        return do_login(username, pwd, cookie_file)


def do_login(username,pwd,cookie_file):
    """"
    Perform login action with use name, password and saving cookies.
    @param username: login user name
    @param pwd: login password
    @param cookie_file: file name where to save cookies when login succeeded 
    """
    #POST data per LOGIN WEIBO, these fields can be captured using httpfox extension in FIrefox
    login_data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'pagerefer':'',
        'vsnf': '1',
        'su': '',
        'service': 'miniblog',
        'servertime': '',
        'nonce': '',
        'pwencode': 'rsa2',
        'rsakv': '',
        'sp': '',
        'encoding': 'UTF-8',
        'prelt': '45',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
        }

    cookie_jar2     = cookielib.LWPCookieJar()
    cookie_support2 = urllib2.HTTPCookieProcessor(cookie_jar2)
    opener2         = urllib2.build_opener(cookie_support2, urllib2.HTTPHandler)
    urllib2.install_opener(opener2)
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.5)'
    try:
        servertime, nonce, rsakv = get_prelogin_status(username)
    except:
        return
    
    #Fill POST data
    login_data['servertime'] = servertime
    login_data['nonce'] = nonce
    login_data['su'] = get_user(username)
    login_data['sp'] = get_pwd_rsa(pwd, servertime, nonce)
    login_data['rsakv'] = rsakv
    login_data = urllib.urlencode(login_data)
    http_headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    req_login  = urllib2.Request(
        url = login_url,
        data = login_data,
        headers = http_headers
    )
    result = urllib2.urlopen(req_login)
    text = result.read()
    p = re.compile('location\.replace\(\"(.*?)\"\)')
    
    try:
        #Search login redirection URL
        login_url = p.search(text).group(1)
        
        data = urllib2.urlopen(login_url).read()
        
        #Verify login feedback, check whether result is TRUE
        patt_feedback = 'feedBackUrlCallBack\((.*)\)'
        p = re.compile(patt_feedback, re.MULTILINE)
        
        feedback = p.search(data).group(1)
        
        feedback_json = json.loads(feedback)
        if feedback_json['result']:
            cookie_jar2.save(cookie_file,ignore_discard=True, ignore_expires=True)
            return 1
        else:
            return 0
    except:
        return 0


def get_pwd_wsse(pwd, servertime, nonce):
    """
        Get wsse encrypted password
    """
    pwd1 = hashlib.sha1(pwd).hexdigest()
    pwd2 = hashlib.sha1(pwd1).hexdigest()
    pwd3_ = pwd2 + servertime + nonce
    pwd3 = hashlib.sha1(pwd3_).hexdigest()
    return pwd3


def get_pwd_rsa(pwd, servertime, nonce):
    """
        Get rsa2 encrypted password, using RSA module from https://pypi.python.org/pypi/rsa/3.1.1, documents can be accessed at 
        http://stuvel.eu/files/python-rsa-doc/index.html
    """
    #n, n parameter of RSA public key, which is published by WEIBO.COM
    #hardcoded here but you can also find it from values return from prelogin status above
    weibo_rsa_n = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
    
    #e, exponent parameter of RSA public key, WEIBO uses 0x10001, which is 65537 in Decimal
    weibo_rsa_e = 65537
   
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)
    
    #construct WEIBO RSA Publickey using n and e above, note that n is a hex string
    key = rsa.PublicKey(int(weibo_rsa_n, 16), weibo_rsa_e)
    
    #get encrypted password
    encropy_pwd = rsa.encrypt(message, key)

    #trun back encrypted password binaries to hex string
    return binascii.b2a_hex(encropy_pwd)


def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username