#!/usr/bin/env python
#coding=utf8

import re
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


db_connection = MySQLdb.connect(host='localhost', port=3306, user='gp', passwd='1222222', db='weibo_users_db', charset='utf8')


def is_user_in_db(uid):
    try:
        count = db_connection.cursor().execute('select uid from user where uid="'+uid+'"')
        if count > 0:
            return True
    except:
        return False
    return False


def add_user_to_db(uid, nick, follows, fans):
    if re.match(r'\d+', follows) and re.match(r'\d+', fans):
        try:
            sql = "insert into user(uid, nick, follows, fans, create_time) values(%s, %s, %s, %s, NOW())"
            param = (uid, nick, int(follows), int(fans))
            db_connection.cursor().execute(sql, param)
            db_connection.commit()
            print '>>>[DB insert user]', uid, nick, follows, fans
            return True
        except Exception, e:
            print '>>>[Error: DB insert user]', uid, nick, follows, fans, e
    return False


def update_user_db_follows(uid):
    try:
        cursor = db_connection.cursor()
        count = cursor.execute('select * from relation where source="'+uid+'"')
        sql = 'update user set db_follows=%s where uid=%s'
        param = (count, uid)
        cursor.execute(sql, param)
        db_connection.commit()
        print '>>>[DB update user]', uid, 'db_follows=',count
        return True
    except Exception, e:
        print '>>>[Error: DB insert user]', uid, 'db_follows=', e
    return False


def query_user(uid):
    try:
        cursor = db_connection.cursor()
        count = cursor.execute('select * from user where uid="'+uid+'"')
        if count > 0:
            return cursor.fetchall()[0]
        return None
    except Exception, e:
        print '>>>[Error: DB query user]', uid, e
        return None


def search_user(keyword):
    try:
        cursor = db_connection.cursor()
        count = cursor.execute('select * from user where uid like "%'+keyword+'%" or nick like "%'+keyword+'%"')
        return cursor.fetchall()
    except Exception, e:
        print '>>>[Error: DB search_user]', keyword, e
        return None


def get_none_crawl_user():
    try:
        cursor = db_connection.cursor()
        count = cursor.execute('select * from user where db_follows=0 order by create_time ASC')
        if count > 100:
            return cursor.fetchmany(100)
        return cursor.fetchall()
    except Exception, e:
        print '>>>[Error: DB get_none_crawl_user]', e
        return None


def is_relation_in_db(target, source):
    try:
        count = db_connection.cursor().execute('select * from relation where source="'+source+'" and target="'+target+'"')
        if count > 0:
            return True
    except:
        return False
    return False


def add_relation_to_db(source, target):
    if re.match(r'\d+', source) and re.match(r'\d+', target):
        try:
            sql = 'insert into relation values(%s, %s)'
            param = (source, target)
            db_connection.cursor().execute(sql, param)
            db_connection.commit()
            print '>>>[DB insert relation]', source, target
            return True
        except Exception, e:
            print '>>>[Error: DB insert relation]', source, target, e
    return False
              

def query_relation(source, target):
    try:
        cursor = db_connection.cursor()
        count = cursor.execute('select * from relation where source="'+source+'" and target="'+target+'"')
        if count > 0:
            return cursor.fetchall()[0]
        return None
    except Exception, e:
        print '>>>[Error: DB query relation]', source, target, e
        return None


def query_follows(uid):
    try:
        cursor = db_connection.cursor()
        count = cursor.execute('select * from user where uid in (select target from relation where source="'+uid+'")')
        if count > 0:
            return cursor.fetchall()
    except Exception, e:
        raise