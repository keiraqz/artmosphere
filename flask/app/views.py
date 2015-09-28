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
	

# Change tabs
@app.route("/")
@app.route("/index")  
def index():
   title = "Artmosphere"
   return render_template("home.html", title = title)

@app.route("/profile")  
def profile():
   title = "Artmosphere"
   return render_template("home.html", title = title)

@app.route("/map")  
def get_map():
   title = "Artmosphere"
   return render_template("map.html", title = title)


# find similar artworks 
@app.route('/map_get', methods=['GET'])
def get_map_data():
	current_time = ""
	if not current_time:
		timestamp = "2015-09-28" # for testing
	else:
		timestamp = current_time
		
	stmt = "SELECT * FROM art_geo_count WHERE event_time = %s"
		# event_time | code | count | location
	response = cs_session.execute(stmt, parameters=[timestamp])
	response_list = []
	for val in response:
		response_list.append(val)
	jsonresponse = [{"code": x.code, "name": x.location, "value": x.count} for x in response_list]
	# return render_template("map.html",output=jsonresponse)
	return jsonify(output=jsonresponse)


# find similar artworks
@app.route('/similar', methods=['POST'])
def img_similar_post():
	req = request.form['artwork_id'] #sim test: 538f6428c9dc24d3d700052c
	art_id = ""
	if not req:
		art_id = "538f6428c9dc24d3d700052c"		
	stmt_2 = "SELECT * FROM artwork_sim WHERE id_1 in %s"
	response_2 = cs_session.execute(stmt_2, parameters=[art_id])
	response_list_2 = []
	for val in response_2:
		response_list_2.append(val)
	jsonresponse_2 = [{"art_id": x.id_1, "similary": x.id_2, "pin_count": x.sim_count} for x in response_list_2]
	return render_template("imgtrenddisplay.html",output=jsonresponse_2)


@app.route("/trend")
def img_trend():
   return render_template("imgtrend.html")

# get image info
@app.route('/trend/<req>', methods=['GET'])
def img_trend_get(req):
	# req = request.form['artwork_id'] #test: 538f6428c9dc24d3d700052c
	art_id = req
	if not art_id:
		art_id = "538f6428c9dc24d3d700052c"

	## Get art info
	stmt_0 = "SELECT artwork_id,image_link, title, collecting_institution, pined_count, sold FROM artworks WHERE artwork_id = %s"
	response_0 = cs_session.execute(stmt_0, parameters=[art_id])
	response_list_0 = []
	for val in response_0:
		response_list_0.append(val)
	jsonresponse_0 = [{"id":x.artwork_id , "title": x.title,"image_link":x.image_link ,"collecting_institution": x.collecting_institution, "pined_count": x.pined_count, "sold":x.sold} for x in response_list_0]

	## Get the trend
	current_time = gmtime()
	to_date = strftime("%Y-%m-%d %H:%M:%S", current_time)
	stmt = "SELECT art_id, pin_count, event_time FROM artwork_count WHERE art_id = %s AND event_time < %s ORDER BY event_time DESC LIMIT 5 ALLOW FILTERING"
	response = cs_session.execute(stmt, parameters=[art_id, to_date])
	response_list = []
	for val in response:
		response_list.append(val)
	jsonresponse = [{"art_id": x.art_id, "event_time": x.event_time, "pin_count": x.pin_count} for x in response_list]

	## Get the similar Art too
	stmt_2 = "SELECT * FROM artwork_sim WHERE id_1 in (%s)"
	response_2 = cs_session.execute(stmt_2, parameters=[art_id])
	response_list_2 = []
	jsonresponse_2 = []
	if response_2:
		for val in response_2:
			temp_stmt = "SELECT artwork_id,image_link FROM artworks WHERE artwork_id = %s"
			temp_response = cs_session.execute(temp_stmt, parameters=[val.id_2])
			jsonresponse_2.append({"art_id": temp_response[0].artwork_id, "image_link": temp_response[0].image_link, "pin_count": val.sim_count})
	## End of similar Art

	## Get some art
	stmt_3 = "SELECT artwork_id,image_link,pined_count FROM artworks LIMIT 5 ALLOW FILTERING"
	response_3 = cs_session.execute(stmt_3)
	jsonresponse_3 = []
	if response_3:
		for val in response_3:
			jsonresponse_3.append({"art_id": val.artwork_id, "image_link": val.image_link, "pin_count": val.pined_count})

	return render_template("imgtrenddisplay.html",output_0=jsonresponse_0, output=jsonresponse,output_2=jsonresponse_2,output_3=jsonresponse_3)


# given date, view art's pinned_count
@app.route('/cs/<art_id>') #test: 515b683f94714cb2e3000131
def get_count(art_id):
	current_time = gmtime()
	to_date = strftime("%Y-%m-%d %H:%M:%S", current_time)
	stmt = "SELECT art_id, pin_count,event_time FROM artwork_count WHERE art_id = %s AND event_time < %s ORDER BY event_time DESC LIMIT 5 ALLOW FILTERING"
	response = cs_session.execute(stmt, parameters=[art_id,to_date])
	response_list = []
	for val in response:
		response_list.append(val)
	jsonresponse = [{"art_id": x.art_id, "event_time": x.event_time, "pin_count": x.pin_count} for x in response_list]
	return jsonify(output=jsonresponse)

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
	if not keywords:
		keywords = "water"
	res = es.search(index = INDEX_NAME, q='title:'+keywords, body={"query": {"match_all": {}}}) 
	pids = [ [ r['_source']['artwork_id'], r['_source']['title'], r['_source']['image_link'], r['_source']['collecting_institution'], int(r['_source']['pined_count']) ] for r in res['hits']['hits']]
	pids.sort(reverse=True)
	jsonresponse = [{"artwork_id": p[0], "title": p[1], "collecting_institution": p[3], "pinned_count": int(p[4]), "image_link": p[2]} for p in pids]
	return render_template("imgdisply.html",output=jsonresponse)

# search keywords in image title
@app.route('/collection')
def collection_dis():
	keywords = "sunrise"
	res = es.search(index = INDEX_NAME, q='title:'+keywords, body={"query": {"match_all": {}}}) 
	pids = [ [ r['_source']['artwork_id'], r['_source']['title'], r['_source']['image_link'], r['_source']['collecting_institution'], int(r['_source']['pined_count']) ] for r in res['hits']['hits']]
	pids.sort(reverse=True)
	jsonresponse = [{"artwork_id": p[0], "title": p[1], "collecting_institution": p[3], "pinned_count": int(p[4]), "image_link": p[2]} for p in pids]
	return render_template("collection.html",output=jsonresponse)

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