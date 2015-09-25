from flask import jsonify

from app import app
from cassandra.cluster import Cluster
from elasticsearch import Elasticsearch
from flask import render_template
import hashlib
from struct import *
import json

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'artsy'
TYPE_NAME = 'artworks'
ID_FIELD = 'id'
es = Elasticsearch(hosts = [ES_HOST])

cs_cluster = Cluster(['172.31.11.233','172.31.11.231','172.31.11.232'])
cs_session = cs_cluster.connect('art_pin_log')
	

# APIs offered by flask

@app.route("/")
@app.route("/index")  
def index():
   user = { 'nickname': 'Miguel' } # fake user
   title = "Artmosphere"
   return render_template("base.html", title = title, user = user)


# given date, view art's pinned_count
@app.route('/cs/<art_id>') #test: 515b683f94714cb2e3000131
def get_count(art_id):
        stmt = "SELECT art_id, pin_count,event_time FROM artwork_count WHERE art_id = %s"
        response = cs_session.execute(stmt, parameters=[art_id])
        response_list = []
        for val in response:
             response_list.append(val)
        jsonresponse = [{"Art ID": x.art_id, "Event Time": x.event_time, "Count": x.pin_count} for x in response_list]
        return jsonify(pin_total=jsonresponse)



# given date, view art's pinned_count
@app.route('/cs/<art_id>/<from_date>/<to_date>') #works: 515b683f94714cb2e3000131/2015-09-25T02:01:30+0000/2015-09-25T02:04:00+0000
def get_timed_count(art_id, from_date, to_date):
        stmt = "SELECT art_id, pin_count,event_time FROM artwork_count WHERE art_id = %s AND event_time > %s AND event_time < %s"
        response = cs_session.execute(stmt, parameters=[art_id, from_date, to_date])
        response_list = []
        for val in response:
             response_list.append(val)
        jsonresponse = [{"Art ID": x.art_id, "Event Time": x.event_time, "Count": x.pin_count} for x in response_list]
        return jsonify(art_id=jsonresponse)


# given a keyword, return all matches
@app.route('/es/title/<keywords>')
def return_name(keywords):
	res = es.search(index = INDEX_NAME, q='title:'+keywords, body={"query": {"match_all": {}}}) 
	pids = [ [ r['_source']['artwork_id'], r['_source']['title'], r['_source']['image_link'], r['_source']['collecting_institution'], int(r['_source']['pined_count']) ] for r in res['hits']['hits']]
	pids.sort(reverse=True)
	matched_pics = {}
	count = 0

	for p in pids:
		matched_pics['%04d'%count] = {
			"artwork_id": p[0],
			"title": p[1],
			"collecting_institution": p[3],
			"pinned_count": int(p[4]),
			"Image_link": p[2]
		}

		count += 1
	return json.dumps(matched_pics, indent=2)
	# retrieve the photo info from hbase

# return top 20 in the database for view
@app.route('/es/all/')
def return_all():
	res = es.search(index = INDEX_NAME, size = 50, body={"query": {"match_all": {}}})
	pids = [ [ r['_source']['artwork_id'], r['_source']['title'], r['_source']['image_link'], r['_source']['collecting_institution'], int(r['_source']['pined_count']) ] for r in res['hits']['hits']]
	pids.sort(reverse=True)
	matched_pics = {}
	count = 0

	for p in pids:
		matched_pics['%04d'%count] = {
			"artwork_id": p[0],
			"title": p[1],
			"collecting_institution": p[3],
			"pinned_count": int(p[4]),
			"Image_link": p[2]
		}

		count += 1
	return json.dumps(matched_pics, indent=2)


if __name__ == '__main__':
	"Are we in the __main__ scope? Start test server."
	app.run(host='0.0.0.0',port=5000,debug=True)