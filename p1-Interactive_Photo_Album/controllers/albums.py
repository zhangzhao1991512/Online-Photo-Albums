from flask import *
from extensions import connect_to_database
import os
albums = Blueprint('albums', __name__, template_folder='templates')



@albums.route('/albums/edit', methods=['GET', 'POST'])
def albums_edit_route():
	db = connect_to_database()
	cur = db.cursor()
	if request.method == 'GET':
		user = request.args.get('username')
		cur.execute("SELECT username FROM User WHERE username = %s;", [user])
		r = cur.fetchall()
		if not r:
			return abort(404)
		else:
			cur.execute("SELECT albumid, title FROM Album WHERE username = %s;", [user])
			results = cur.fetchall()
			options = {
				"edit": True,
				"username": request.args.get('username'),
				"albums": results
			}
			return render_template("albums.html", **options)
	else:
		user = request.args.get('username')
		if request.form['op'] == "delete":
			albumid = request.form['albumid']
			cur.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + albumid + " AND P.picid = C.picid")
			pictures = cur.fetchall()
			cur.execute("DELETE P, C FROM Photo P JOIN Contain C ON P.picid = C.picid AND C.albumid = " + albumid)
			cur.execute("DELETE FROM Album WHERE albumid = " + albumid)
			cur.execute("SELECT albumid, title FROM Album WHERE username = %s;", [user])
			results = cur.fetchall()
			for pic in pictures:
				os.remove("./static/images/" + pic["picid"] + "." + pic["format"])

		if request.form['op'] == "add":
			title = request.form['title']
			cur.execute("INSERT INTO Album(title, username) VALUES ('" + title + "', '" + user + "')")
			cur.execute("SELECT albumid, title FROM Album WHERE username = %s;", [user])
			results = cur.fetchall()
		options = {
			"edit": True,
			"username": user,
			"albums": results
			}
		return render_template("albums.html", **options)


@albums.route('/albums', methods=['GET', 'POST'])
def albums_route():
	db = connect_to_database()
	cur = db.cursor()
	if request.method == 'GET':
		user = request.args.get('username')
		cur.execute("SELECT username FROM User WHERE username = %s;", [user])
		r = cur.fetchall()
		if not r:
			return abort(404)
		else:
			cur.execute("SELECT albumid, title FROM Album WHERE username = %s;", [user])
			results = cur.fetchall()
			options = {
				"edit": False,
				"username": request.args.get('username'),
				"albums": results
			}
			return render_template("albums.html", **options)

	# else:
	# 	options = {
	# 		"edit": False
	# 	}
	# 	return render_template("albums.html", **options)