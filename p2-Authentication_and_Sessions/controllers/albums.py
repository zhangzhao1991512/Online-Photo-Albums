from flask import *
from extensions import connect_to_database
import os
albums = Blueprint('albums', __name__, template_folder='templates')



@albums.route('/albums/edit', methods=['GET', 'POST'])
def albums_edit_route():
	db = connect_to_database()
	cur = db.cursor()
	if 'username' not in session:
		return redirect(url_for('user.login_route'))

	if request.method == 'GET':
		username = session['username']
		cur.execute("SELECT username FROM User WHERE username = %s;", [username])
		r = cur.fetchall()
		if not r:
			return abort(404)
		else:
			cur.execute("SELECT firstname, lastname FROM User WHERE username = '" + username + "'")
			user = cur.fetchall()[0]
			cur.execute("SELECT albumid, title FROM Album WHERE username = %s;", [username])
			results = cur.fetchall()
			options = {
				"edit": True,
				"user": user,
				"username": username,
				"albums": results
			}
			return render_template("albums.html", **options)
	else:
		username = session['username']
		cur.execute("SELECT firstname, lastname FROM User WHERE username = '" + username + "'")
		user = cur.fetchall()[0]
		if request.form['op'] == "delete":
			albumid = request.form['albumid']
			cur.execute("DELETE FROM AlbumAccess WHERE albumid = " + albumid )
			cur.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + albumid + " AND P.picid = C.picid")
			pictures = cur.fetchall()
			cur.execute("DELETE P, C FROM Photo P JOIN Contain C ON P.picid = C.picid AND C.albumid = " + albumid)
			cur.execute("DELETE FROM Album WHERE albumid = " + albumid)
			cur.execute("SELECT albumid, title FROM Album WHERE username = %s;", [username])
			results = cur.fetchall()
			for pic in pictures:
				os.remove("./static/images/" + pic["picid"] + "." + pic["format"])

		if request.form['op'] == "add":
			title = request.form['title']
			cur.execute("INSERT INTO Album(title, username, access) VALUES ('" + title + "', '" + username + "', 'private')")
			cur.execute("SELECT albumid, title FROM Album WHERE username = %s;", [username])
			results = cur.fetchall()
		options = {
			"edit": True,
			"user": user,
			"username": username,
			"albums": results
			}
		return render_template("albums.html", **options)


@albums.route('/albums', methods=['GET', 'POST'])
def albums_route():
	db = connect_to_database()
	cur = db.cursor()
	if request.method == 'GET':
		if not request.args.get('username'):
			# no username parameter, sensitive My Albums Page, edit link exist
			if 'username' not in session:
				return abort(404)
			else:
				username = session['username']
				# current logged in user
				cur.execute("SELECT firstname, lastname FROM User WHERE username = '" + username + "'")
				user = cur.fetchall()[0]
				cur.execute("SELECT albumid, title FROM Album WHERE username = '" + username + "'")
				albums = cur.fetchall()
				options = {
					'edit': False,
					'edit_link': True,
					'user': user,
					'username': username,
					'albums': albums
				}
				return render_template('albums.html', **options)
		
		else:
			# there is a parameter 'username' in the url, Public Albums of User, no edit link
			username = request.args.get('username')
			cur.execute("SELECT username FROM User WHERE username = %s;", [username])
			r = cur.fetchall()
			if not r:
				return abort(404)
			if 'username' not in session:
				albums = get_user_public_albums()
				options = {
					'edit': False,
					'edit_link': False,
					'username': username,
					'albums': albums
				}
				return render_template("albums.html", **options)

			else:
				# someone's login show the login information
				cur.execute("SELECT firstname, lastname FROM User WHERE username = '" + session['username'] + "'")
				user = cur.fetchall()[0]
				albums = get_user_public_albums()
				# albums?username=<username>, show private albums when <username> = session['username']?????????????????????????????
				options = {
					'edit': False,
					'edit_link': False,
					'user': user,
					'username': username,
					'albums': albums
				}
				return render_template("albums.html", **options)

	else:
		return abort(404)


def get_user_albums():
	db = connect_to_database()
	cur = db.cursor()
	username = session['username']
	cur.execute("SELECT albumid, title FROM Album WHERE username = %s", [username])
	results = cur.fetchall()
	return results



def get_user_public_albums():
	db = connect_to_database()
	cur = db.cursor()
	username = request.args.get('username')
	cur.execute("SELECT albumid, title FROM Album WHERE username = %s AND access = 'public'", [username])
	results = cur.fetchall()
	return results