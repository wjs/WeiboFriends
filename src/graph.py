#!/usr/bin/env python
#coding=utf8

from random import randint
import sys
import os
import db
import weibo_crawl

reload(sys)
sys.setdefaultencoding('utf-8')


def delete_file_in_folder(src):
    '''delete files in folder'''
    if os.path.isfile(src):
        try:
            os.remove(src)
        except:
            pass
    elif os.path.isdir(src):
        for item in os.listdir(src):
            itemsrc = os.path.join(src, item)
            delete_file_in_folder(itemsrc) 


def genarate_graph(uid):
	self = db.query_user(uid)
	text = '{\n\t"nodes":[\n\t\t{"name":"' + self[1]+'","group":0, "uid":"'+self[0]+'", "follows":'+str(self[2])+', "fans":'+str(self[3])+' },\n\t\t'
	follows = db.query_follows(uid)
	if follows:
		for row in follows:
			text += '{"name":"'+row[1]+'","group":1, "uid":"'+row[0]+'", "follows":'+str(row[2])+', "fans":'+str(row[3])+' },\n\t\t'
		text = text[:-4] + '\n\t],\n\t"links":[\n\t\t'
		for i in range(1, len(follows)+1):
		    text += '{"source":'+str(i)+',"target":0,"value":'+str(randint(2, 20))+'},\n\t\t'
	else:
		text = text[:-4] + '\n\t],\n\t"links":[\n\t\t\t'
	text = text[:-4] + '\n\t]\n}'

	delete_file_in_folder('static/data')
	f = open('static/data/'+uid+'.json', 'w')
	f.write(text)
	f.close()
	print 'genarate json file ok'
	return True


def genarate_graph_from_web(username, pwd):
	selfUid = weibo_crawl.get_self_weibo_relation(username, pwd)
	if selfUid and db.is_user_in_db(selfUid):
		return genarate_graph(selfUid);
	return False