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
def index():
    return render_template('index.html')


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


@app.route('/change_graph', methods=['GET'])
def change_graph():
	uid = request.args.get('uid')
	json = '{isSucceed:'
	user = db.query_user(uid)
	if user:
		if graph.genarate_graph(uid):
			json += 'true, uid:"'+uid+'", nick:"'+user[1]+'", follows:"'+str(user[2])+'", fans:"'+str(user[3])+'", db_follows:"'+str(user[4])+'", db_fans:"'+str(user[5])+'"}'
			return json
	json += 'false, uid:"' + uid + '"}'
	return json


@app.route('/graph', methods=['GET'])
def get_graph():
	uid = request.args.get('uid')
	return render_template('graph.html', uid=uid)


@app.route('/login', methods=['POST'])
def login():
	username = request.form['username']
	pwd = request.form['pwd']
	graph.genarate_graph_from_web(username, pwd)
	return render_template('index.html')

@app.route('/autocrawl', methods=['POST'])
def autocrawl():
	username = request.form['username']
	pwd = request.form['pwd']
	weibo_crawl.auto_crawl(username, pwd)
	return render_template('index.html')


if __name__ == '__main__':
	app.run(port=8080, debug=True)
