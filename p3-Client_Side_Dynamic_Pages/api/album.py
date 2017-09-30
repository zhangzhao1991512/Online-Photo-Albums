from flask import *

import MySQLdb
import MySQLdb.cursors
import hashlib
import os
from werkzeug.utils import secure_filename
#from extensions import db
import extensions
db = extensions.connect_to_database()

#UPLOAD_FOLDER = '/static/images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp', 'gif'])

cur = db.cursor()
cur1 = db.cursor()
cur2 = db.cursor()

albumAPI = Blueprint('albumAPI', __name__, template_folder='templates')


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@albumAPI.route('/api/v1/album/<albumid>')
def API_album_route(albumid):
	cur.execute("SELECT albumid FROM Album WHERE albumid = " + albumid)
	check_album = cur.fetchall()
	if not check_album:
		response = json.jsonify(errors=[{"message": "The requested resource could not be found"}])
		response.status_code = 404
		return response

	if 'username' in session:
		#-----if the user can access the album----#
		cur2.execute("SELECT albumid FROM Album WHERE (access = 'public' AND albumid = " + albumid + ") OR (username = '" + session['username']+ "' AND albumid = " + albumid + ") UNION SELECT albumid FROM AlbumAccess WHERE username = '" + session['username'] + "' AND albumid = " + albumid)
		access_albums = cur2.fetchall()
		if not access_albums:
			response = json.jsonify(errors=[{"message": "You do not have the necessary permissions for the resource"}])
			response.status_code = 403
			return response
		#-----------------Valid-------------------#
		cur2.execute("SELECT access, title, created, lastupdated, username FROM Album WHERE albumid = " + albumid)
		r = cur2.fetchall()[0]
		access = str( r['access'])
		title = str( r['title'])
		#created = str( r['created'])
		#lastupdated = str( r['lastupdated'])
		created = r['created']
                lastupdated = r['lastupdated']
		username = str( r['username'])

		response = json.jsonify({"access": access,
					"albumid": albumid,
					"created": created.strftime('%Y-%m-%d'),
					"lastupdated": lastupdated.strftime('%Y-%m-%d'),
					"pics": get_pic(albumid),
					"title": title,
					"username": username})
		response.status_code = 200
		return response
	else:
		cur2.execute("SELECT access FROM Album WHERE albumid = " + albumid)
		access = str (cur2.fetchall()[0]['access'])
		if access == 'private':
#			return redirect(url_for('main.login_route'))
			response = json.jsonify(errors=[{"message": "You do not have the necessary credentials for the resource"}])
			response.status_code = 401
			return response
		else:
			cur2.execute("SELECT title, created, lastupdated, username FROM Album WHERE albumid = " + albumid)
			title = str( cur2.fetchall()[0]['title'])
			#created = str( cur2.fetchall()[0]['created'])
			#lastupdated = str( cur2.fetchall()[0]['lastupdated'])
			created = cur2.fetchall()[0]['created']
			lastupdated = cur2.fetchall()[0]['lastupdated']
			username = str( cur2.fetchall()[0]['username'])

			response = json.jsonify({"access": "public",
						"albumid": albumid,
						"created": created.strftime('%Y-%m-%d'),
						"lastupdated": lastupdated.strftime('%Y-%m-%d'),
						"pics": get_pic(albumid),
						"title": title,
						"username": username})
			response.status_code = 200
			return response

def get_pic(albumid):
	cur1.execute("SELECT caption, picid, sequencenum FROM Contain WHERE albumid = " + albumid + " Order by sequencenum")
	pictures = cur1.fetchall()
	pics = []
	for p in pictures:
		cur1.execute("SELECT date, format FROM Photo WHERE picid = '" + pictures[0]['picid'] + "'")
		results = cur1.fetchall()
		pics.append({"albumid": albumid, "caption": p['caption'], "date": results[0]['date'].strftime('%Y-%m-%d'),
					"format": results[0]['format'], "picid": p['picid'], "sequencenum": p['sequencenum']})
	return pics
