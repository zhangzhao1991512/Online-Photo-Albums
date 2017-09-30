from flask import *
import MySQLdb
import MySQLdb.cursors
#from extensions import db

import extensions
db = extensions.connect_to_database()


cur = db.cursor()
cur1 = db.cursor()

picAPI = Blueprint('picAPI', __name__, template_folder='templates')

@picAPI.route('/api/v1/pic/<picid>', methods=['GET', 'PUT'])
def pic_api(picid):
	if request.method == 'GET':
		cur.execute("SELECT picid FROM Photo WHERE picid = %s", [picid])
		r = cur.fetchall()
		if not r:
			response = json.jsonify(errors=[{"message": "The requested resource could not be found"}])
			response.status_code = 404
			return response

		cur.execute("SELECT albumid FROM Contain WHERE picid = '" + picid +"'")
		res = cur.fetchall()
		albumid = str (res[0]['albumid'])

		cur.execute("SELECT format FROM Photo WHERE picid = '" + picid + "'")
		res1 = cur.fetchall()
		form = str (res1[0]['format'])

		cur.execute("SELECT picid FROM Contain WHERE albumid = " + albumid + " order by sequencenum")
		res2 = cur.fetchall()

		if 'username' not in session:
			cur.execute("SELECT A.access FROM Album A, Contain C WHERE C.albumid = A.albumid AND C.picid = '" + picid + "'")
                        access = str (cur.fetchall()[0]['access'])
                        if access == 'private':
				response = json.jsonify(errors=[{"message": "You do not have the necessary credentials for the resource"}])
				response.status_code = 401
				return response
#			else:
#				#!!!!!!!!!!!!!!!
		else:
			cur.execute("SELECT A.albumid FROM Album A, Contain C WHERE C.picid = '" + picid +"' AND ((A.access = 'public' AND A.albumid = C.albumid) OR (A.username = '" + session['username']+ "' AND A.albumid = C.albumid)) UNION SELECT A1.albumid FROM AlbumAccess A1, Contain C1 WHERE username = '" + session['username'] + "' AND A1.albumid = C1.albumid AND C1.picid ='" + picid +"'")
                        access_albums = cur.fetchall()
                        if not access_albums:
				response = json.jsonify(errors=[{"message": "You do not have the necessary permissions for the resource"}])
				response.status_code = 403
				return response
		
		#-----------------------Otherwise, the pic can be accessed (following code)---------------------------

		cur.execute("SELECT COUNT(picid) FROM Contain where albumid = " + albumid)
		countres = cur.fetchall()
		count = int (countres[0]['COUNT(picid)'])
		count = count - 1;
		first_id = str (res2[0]['picid'])
		if first_id == picid:
			prev = False
		else:
			prev = True

		last_id = str (res2[count]['picid'])
		if last_id == picid:
			nex = False
		else:
			nex = True
		index = 0
		i = 0
		while (i < count+1):
			if picid == str(res2[i]['picid']):
				index = i
			i = i + 1
		
		prev_picid = ""
		next_picid = ""
		if (prev):
			prev_picid = res2[index-1]['picid']
		if (nex):
			next_picid = res2[index+1]['picid']

		cur.execute("SELECT caption FROM Contain WHERE picid = '" + picid +"'")
		caption = str(cur.fetchall()[0]['caption'])
		
		cur.execute("SELECT A.access FROM Album A, Contain C WHERE C.albumid = A.albumid AND C.picid = '" + picid + "'")
		access = str (cur.fetchall()[0]['access'])

		response = json.jsonify({"albumid": albumid, "caption": caption, "format": form, "next": next_picid, "picid": picid, "prev": prev_picid})
		response.status_code = 200
		return response

	#---------For Update--------
	if request.method == 'PUT':
		try:
			albumid = request.get_json()['albumid']
			caption = request.get_json()['caption']
			form = request.get_json()['format']
			next_picid = request.get_json()['next']
			picid = request.get_json()['picid']
			prev_picid = request.get_json()['prev']
		except KeyError:
			error_info = "You did not provide the necessary fields"
			response = json.jsonify(errors=[{"message": error_info}])
			response.status_code = 422
			return response			

		cur1.execute("SELECT picid FROM Photo WHERE picid = %s", [u])
		r = cur1.fetchall()
		if not r:
			response = json.jsonify(errors=[{"message": "The requested resource could not be found"}])
			response.status_code = 404
			return response

		if 'username' not in session:
			cur1.execute("SELECT A.access FROM Album A, Contain C WHERE C.albumid = A.albumid AND C.picid = '" + picid + "'")
			access = str (cur1.fetchall()[0]['access'])
			if access == 'private':
				response = json.jsonify(errors=[{"message": "You do not have the necessary credentials for the resource"}])
				response.status_code = 401
				return response
		else:
			cur1.execute("SELECT A.albumid FROM Album A, Contain C WHERE C.picid = '" + picid +"' AND ((A.access = 'public' AND A.albumid = C.albumid) OR (A.username = '" + session['username']+ "' AND A.albumid = C.albumid)) UNION SELECT A1.albumid FROM AlbumAccess A1, Contain C1 WHERE username = '" + session['username'] + "' AND A1.albumid = C1.albumid AND C1.picid ='" + picid +"'")
			access_albums = cur1.fetchall()
			if not access_albums:
				response = json.jsonify(errors=[{"message": "You do not have the necessary permissions for the resource"}])
				response.status_code = 403
				return response

		cur1.execute("SELECT albumid FROM Contain WHERE picid = '" + picid +"'")
                res = cur1.fetchall()
                wow_albumid = str (res[0]['albumid'])

                cur1.execute("SELECT format FROM Photo WHERE picid = '" + picid + "'")
                res1 = cur1.fetchall()
                wow_form = str (res1[0]['format'])

		cur1.execute("SELECT COUNT(picid) FROM Contain where albumid = " + wow_albumid)
		counters = cur1.fetchall()
		count = int (counters[0]['COUNT(picid)'])
		count = count - 1;

		cur1.execute("SELECT picid FROM Contain WHERE albumid = " + wow_albumid + " order by sequencenum")
		res2 = cur1.fetchall()

		first_id = str (res2[0]['picid'])
		if first_id == picid:
			wow_prev = False
		else:
			wow_prev = True

		last_id = str (res2[count]['picid'])
		if last_id == picid:
			wow_nex = False
                else:
                        wow_nex = True
                index = 0
                i = 0
                while (i < count+1):
                        if picid == str(res2[i]['picid']):
                                index = i
                        i = i + 1

                wow_prev_picid = ""
                wow_next_picid = ""
                if (wow_prev):
                        wow_prev_picid = res2[index-1]['picid']
                if (wow_nex):
                        wow_next_picid = res2[index+1]['picid']


		if albumid != wow_albumid or form != wow_form or wow_next_picid != next_picid or wow_prev_picid != prev_picid:
			error_info = "You can only update caption"
			response = json.jsonify(errors=[{"message": error_info}])
			response.status_code = 403
			return response				

		cur1.execute("UPDATE Contain SET caption = %s WHERE picid=%s", [caption, picid])
		cur1.execute("UPDATE Album SET lastupdated=Now() WHERE albumid = " + albumid)

		response = json.jsonify({"albumid": albumid, "caption": caption, "format": form, "next": next_picid, "picid": picid, "prev": prev_picid})
		response.status_code = 200
		return response

