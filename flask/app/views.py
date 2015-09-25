from flask import jsonify

from app import app
from cassandra.cluster import Cluster
from elasticsearch import Elasticsearch
from flask import render_template, request
import hashlib
from struct import *
import json
from time import gmtime, strftime

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
   return render_template("home.html", title = title, user = user)



# find similar artworks
@app.route('/similar', methods=['POST'])
def img_similar_post():
	req = request.form['artwork_id'] #sim test: 538f6428c9dc24d3d700052c
	art_id = ""
	if not req:
		art_id = "538f6428c9dc24d3d700052c"		
	stmt_2 = "SELECT * FROM artwork_sim WHERE WHERE id_1 in %s"
	response_2 = cs_session.execute(stmt_2, parameters=[art_id])
	response_list_2 = []
	for val in response_2:
		response_list_2.append(val)
	jsonresponse_2 = [{"art_id": x.id_1, "similary": x.id_2, "pin_count": x.sim_count} for x in response_list_2]
	return render_template("imgtrenddisplay.html",output=jsonresponse_2)


@app.route("/trend")
def img_trend():
   return render_template("imgtrend.html")

# search keywords in image title
@app.route('/trend', methods=['POST'])
def img_trend_post():
	req = request.form['artwork_id'] #test: 538f6428c9dc24d3d700052c
	art_id = req
	if not req:
		art_id = "538f6428c9dc24d3d700052c"	
	current_time = gmtime()
	to_date = strftime("%Y-%m-%d %H:%M:%S", current_time)
	stmt = "SELECT art_id, pin_count, event_time FROM artwork_count WHERE art_id = %s AND event_time < %s ORDER BY event_time DESC"
	response = cs_session.execute(stmt, parameters=[art_id, to_date])
	response_list = []
	for val in response:
		response_list.append(val)
	jsonresponse = [{"art_id": x.art_id, "event_time": x.event_time, "pin_count": x.pin_count} for x in response_list]

	## Get the similar Art too
	stmt_2 = "SELECT * FROM artwork_sim WHERE id_1 in (%s)"
	response_2 = cs_session.execute(stmt_2, parameters=[art_id])
	response_list_2 = []
	for val in response_2:
		response_list_2.append(val)
	jsonresponse_2 = [{"art_id": x.id_1, "similary": x.id_2, "pin_count": x.sim_count} for x in response_list_2]

	## End of similar Art
	return render_template("imgtrenddisplay.html",output=jsonresponse,output_2=jsonresponse_2)


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



@app.route("/search")
def search():
   return render_template("imgsearch.html")

# search keywords in image title
@app.route('/search', methods=['POST'])
def img_name_post():
	keywords = request.form['keywords']
	res = es.search(index = INDEX_NAME, q='title:'+keywords, body={"query": {"match_all": {}}}) 
	pids = [ [ r['_source']['artwork_id'], r['_source']['title'], r['_source']['image_link'], r['_source']['collecting_institution'], int(r['_source']['pined_count']) ] for r in res['hits']['hits']]
	pids.sort(reverse=True)
	jsonresponse = [{"artwork_id": p[0], "title": p[1], "collecting_institution": p[3], "pinned_count": int(p[4]), "image_link": p[2]} for p in pids]
	return render_template("imgdisply.html",output=jsonresponse)

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