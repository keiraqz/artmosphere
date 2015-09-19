#!/usr/bin/python
from flask import Flask, request, json
import flask
# import happybase
from elasticsearch import Elasticsearch
import hashlib
from struct import *
app = Flask(__name__)

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'pinterest'
TYPE_NAME = 'pins'
ID_FIELD = 'pin_id'


es = Elasticsearch(hosts = [ES_HOST])
# POOL = happybase.ConnectionPool(size=30, host="c0tl.com")

#retrieve all the photos
# def get_row_prefix(uid, timestamp=None):
# 	prefix = hashlib.md5(str(uid)).digest()
# 	if timestamp:
# 		prefix += str(timestamp)
# 	print "Prefix:",prefix
# 	return prefix
	

# APIs offered by flask

@app.route("/")
@app.route("/index")  
def hello(): 
    return "What a wonderful life!"


# given a keyword, return all matches
@app.route('/names/<keywords>')
def return_name(keywords):
	res = es.search(index = INDEX_NAME, q='description:'+keywords, body={"query": {"match_all": {}}}) 
	pids = [ [ int(r['_source']['pin_id']), r['_source']['description'], r['_id'], r['_source']['image_link'] ] for r in res['hits']['hits']]
	pids.sort(reverse=True)
	# list of 
	# like, view, pid, distance, lat, lon
	matched_pins = {}
	count = 0
	# with POOL.connection() as connection:
	# 	ptbl = connection.table('photos')
	for p in pids:
		matched_pins['%04d'%count] = {
			"P_id": int(p[0]),
			"Description": p[1],
			"Image_link": p[2]
		}
		# rowkey = hashlib.md5(str(p[2])).digest()
		# result['%04d'%count]['photo'] = json.loads( ptbl.row(rowkey)['p:dump'] )['data']['photo']
		count += 1
	return json.dumps(matched_pins)
	# retrieve the photo info from hbase

# return top 20 in the database for view
@app.route('/all/')
def return_all():
	res = es.search(index = INDEX_NAME, size = 20, body={"query": {"match_all": {}}})
	pids = [ [ int(r['_source']['pin_id']), r['_source']['description'], r['_id'], r['_source']['image_link'] ] for r in res['hits']['hits']]
	pids.sort(reverse=True)
	# list of 
	# like, view, pid, distance, lat, lon
	matches = {}
	count = 0
	# with POOL.connection() as connection:
	# 	ptbl = connection.table('photos')
	for p in pids:
		matches['%04d'%count] = {
			"P_id": int(p[0]),
			"Description": p[1],
			"Image_link": p[2]
		}
		# rowkey = hashlib.md5(str(p[2])).digest()
		# result['%04d'%count]['photo'] = json.loads( ptbl.row(rowkey)['p:dump'] )['data']['photo']
		count += 1
	return json.dumps(matches)


# # given a hashtag, return the photos linked with that
# @app.route('/tag/', methods=['POST'])
# def tag():
# 	tagname=request.form['name']
# 	count=request.form['num']
# 	rowkey = "%016d"%int(count) + hashlib.md5(tagname).digest()
# 	connection = happybase.Connection(hbasehost)
# 	tag_tbl = connection.table('top_tags')
# 	return tag_tbl.row(rowkey)['p:dump']

# # given a photo id, return the detailed information


# # return the most popular hashtags
# @app.route('/top_tags')
# def trending_hashtags():
# 	connection = happybase.Connection(hbasehost)
# 	tag_tbl = connection.table('top_tags')
# 	tag_dict = {}
# 	pairs = []
# 	for key, data in tag_tbl.scan():
# 		pairs.append([key, data])
# 	for i in reversed(range(len(pairs))):
# 		try:
# 			key, data = pairs[len(pairs) - i -1]
# 			tag_dict['%04d'%i] = {
# 				"count": int(key[:16]),
# 				"tag": data["p:tag"]
# 				}
# 		except Exception as e:
# 			return str(e)
# 	return json.dumps(tag_dict)

# # given a user name, return all the uids with username matching that pattern
# @app.route('/user/<username>')
# def names(username):
# 	return 'User %s' % username


if __name__ == '__main__':
	"Are we in the __main__ scope? Start test server."
	app.run(host='0.0.0.0',port=5000,debug=True)