from flask import Flask, render_template, request, Response
import json
import sys
import db
import graph
import weibo_crawl

reload(sys)
sys.setdefaultencoding('utf-8')


app = Flask(__name__)


@app.route('/')
def index2():
    return render_template('index2.html')


@app.route('/search', methods=['GET'])
def search():
	result = db.search_user(request.args.get('keyword'))
	json_list = '['
	if result:
	    for i in range(len(result)):
	    	json_list += '{uid:"'+result[i][0]+'", nick:"'+result[i][1]+'", follows:"'+str(result[i][2])+'", fans:"'+str(result[i][3])+'", db_follows:"'+str(result[i][4])+'", db_fans:"'+str(result[i][5])+'"},'
        json_list = json_list[:-1]
	json_list += ']'
	return Response(json.dumps(json_list), mimetype='application/json')


# @app.route('/change_graph', methods=['GET'])
# def change_graph():
# 	uid = request.args.get('uid')
# 	json = '{isSucceed:'
# 	user = db.query_user(uid)
# 	if user:
# 		if graph.genarate_graph(uid):
# 			json += 'true, uid:"'+uid+'", nick:"'+user[1]+'", follows:"'+str(user[2])+'", fans:"'+str(user[3])+'", db_follows:"'+str(user[4])+'", db_fans:"'+str(user[5])+'"}'
# 			return json
# 	json += 'false, uid:"' + uid + '"}'
# 	return json


# @app.route('/graph', methods=['GET'])
# def get_graph():
# 	uid = request.args.get('uid')
# 	return render_template('graph2.html', uid=uid)
@app.route('/graph', methods=['GET'])
def get_graph():
	self_uid = request.args.get('uid')
	self = db.query_user(self_uid)
	nodes = '"nodes":[{"uid":' + self[0] + ', "nick":"' + self[1] + '", "follows":' + str(self[2]) + ', "fans":' + str(self[3]) + '},'
	links = '"links":['
	follows = db.query_follows(self_uid)
	if follows:
		for row in follows:
			nodes += '{"uid":' + row[0] + ', "nick":"' + row[1] + '", "follows":' + str(row[2]) + ', "fans":' + str(row[3]) + '},'
			links += '{"source":' + self_uid + ',"target":' + row[0] + '},'
		nodes = nodes[:-1] + ']'
		links = links[:-1] + ']'
	else:
		nodes = nodes[:-1] + ']'
		links += ']'
	
	return '{' + nodes + ', ' + links + '}'


# @app.route('/login', methods=['POST'])
# def login():
# 	username = request.form['username']
# 	pwd = request.form['pwd']
# 	graph.genarate_graph_from_web(username, pwd)
# 	return render_template('index2.html')

@app.route('/crawl', methods=['POST'])
def autocrawl():
	args = request.data.split('&')
	crawl_uid = args[0].split('=')[1]
	username = args[1].split('=')[1]
	pwd = args[2].split('=')[1]
	weibo_crawl.crawl_by_uid(crawl_uid, username, pwd)
	return ''


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
