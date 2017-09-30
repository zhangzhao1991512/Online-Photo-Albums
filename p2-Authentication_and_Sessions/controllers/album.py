from flask import *
from extensions import connect_to_database
import hashlib
import os
from werkzeug.utils import secure_filename


album = Blueprint('album', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@album.route('/album/edit', methods=['GET', 'POST'])
def album_edit_route():
	db = connect_to_database()
	cur = db.cursor()
	album_id = request.args.get('albumid')
	#print(type(album_id))
	no_seesion = True
	if 'username' in session:
		no_seesion = False
	if no_seesion:
		return abort(403)

	username = session['username']

	if request.method == "GET":
		
		cur.execute("SELECT firstname, lastname FROM User WHERE username = '" + username + "'")
		user = cur.fetchall()[0]
		cur.execute("SELECT albumid FROM Album WHERE albumid = %s", [album_id])
		r = cur.fetchall()
		if not r:
			return abort(404)
		cur.execute("SELECT albumid FROM Album WHERE albumid = %s AND username = '" + username + "'", [album_id])
		access_albums = cur.fetchall()
			# access_albums are whether <username> can access <albumid>
		if not access_albums:
			return abort(403)

		cur.execute("SELECT C.picid, C.caption, P.date, P.format FROM Contain C, Photo P WHERE C.albumid = " + str(album_id) + " AND P.picid = C.picid ORDER BY sequencenum")
		pic_result = cur.fetchall()
		cur.execute("SELECT title FROM Album WHERE albumid = " + album_id)
		album_result = cur.fetchall()
		cur.execute("SELECT username FROM Album WHERE albumid = " + album_id)
		album_username= str(cur.fetchall()[0]['username'])

		# whether private or not:
		cur.execute("SELECT access FROM Album WHERE albumid = '" + album_id + "'")
		access = str(cur.fetchall()[0]['access'])
		private = True
		if access == 'public':
			private = False
		elif access == 'private':
			private = True
		cur.execute("SELECT username FROM AlbumAccess WHERE albumid = " + album_id)
		grant_users = cur.fetchall()

		if 'error' in session:
			error = True
			error_msg = session['error_msg']
		else:
			error = False
			error_msg = ""

		options = {
			"edit": True,
			"private": private,
			"error": error,
			"error_msg": error_msg,
			"user": user,
			"grant_users": grant_users,
			"album_username": album_username,
			"albumid": album_id,
			"album_title": album_result[0]['title'],
			"pictures": pic_result
		}
		session.pop('error', None)
		session.pop('error_msg', None)
		return render_template("album.html", **options)


		





	elif request.method == "POST":
		session['error'] = False
		session['error_msg'] = ""
		if request.form['op'] == 'access':
			cur.execute("UPDATE Album SET lastupdated = Now() WHERE albumid = " + str(album_id))
			cur.execute("UPDATE Album SET access = '" + request.form['access'] + "' WHERE albumid = " + str(album_id))
			if request.form['access'] == 'public':
				cur.execute("DELETE FROM AlbumAccess WHERE albumid = " + str(album_id))
			return redirect(request.url)
		if request.form['op'] == 'grant':
			# check whether the input username is a valid username
			cur.execute("SELECT username FROM User WHERE username = %s", [request.form['username']])
			valid = cur.fetchall()
			if not valid:
				session['error'] = True
				session['error_msg'] = "Username does not exist"
				return redirect(request.url)
			if request.form['username'] == username:
				session['error'] = True
				session['error_msg'] = "You don't need to grant yourself"
				return redirect(request.url)
			cur.execute("SELECT username FROM AlbumAccess WHERE username = '" + request.form['username'] + "' AND albumid = " + str(album_id))
			access = cur.fetchall()
			if access:
				session['error'] = True
				session['error_msg'] = request.form['username'] + "has already been granted access to the album"
				return redirect(request.url)
			else:
				cur.execute("INSERT INTO AlbumAccess VALUES (" + str(album_id) + ", '" + request.form['username'] + "')")
				return redirect(request.url)

		if request.form['op'] == 'revoke':

			cur.execute("DELETE FROM AlbumAccess WHERE username = '" + request.form['username'] + "' AND albumid = " + request.form['albumid'])
			return redirect(request.url)



		if request.form['op'] == 'delete':
			picid = request.form['picid']
			
			cur.execute("SELECT format FROM Photo WHERE picid = '" + picid + "'" )
			pic_format = str(cur.fetchall()[0]['format'])

			cur.execute("DELETE FROM Contain WHERE picid = '" + picid + "'")
			cur.execute("DELETE FROM Photo WHERE picid = '" + picid + "'" )
			#update the lastupdated time for this album
			cur.execute("UPDATE Album SET lastupdated = Now() WHERE albumid = %s", [album_id])
			cur.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + str(album_id) + " AND P.picid = C.picid ORDER BY sequencenum")
			pic_result = cur.fetchall()
			# cur.execute("SELECT title FROM Album WHERE albumid = " + album_id)
			# album_result = cur.fetchall()

			#the path can change!!!!!!!!!!!!!!!!!
			os.remove("./static/images/" + picid + "." + pic_format)

			# options = {
			# 	"edit": True,
			# 	"albumid": album_id,
			# 	"album_title": album_result[0]['title'],
			# 	"pictures": pic_result
			# }
			return redirect(request.url)

		if request.form['op'] == 'add':
			#check if the post request has the file (the uplode file is not empty)
			if 'file' not in request.files:
				return redirect(request.url)
			file = request.files['file']
			if file.filename == '':
				return redirect(request.url)

			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file_format = filename.split('.')[1]

				# m = hashlib.md5((str(albumid)+i).encode('utf-8'))
				# m = m.hexdigest()
				new_picid = hashlib.md5((str(album_id) + filename).encode('utf-8')).hexdigest()
				#new_picid = (hashlib.md5(str(album_id) + filename)).encode('utf-8').hexdigest()

				#path can change!!!!!!!!!!!!!!!
				new_filepath = os.path.join("./static/images/" + new_picid + "." +file_format)
				file.save(new_filepath)

				cur.execute("SELECT Max(sequencenum) FROM Contain")
				seq = int(cur.fetchall()[0]["Max(sequencenum)"])+1
				#print(seq)
				#print(type(seq))
				#insert the new picture
				cur.execute("INSERT INTO Photo(picid, format) VALUES ('" + new_picid + "', '" + file_format + "')")
				cur.execute("INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (" + str(seq) + ", " + str(album_id) + ", '" + new_picid + "', '' )")
				#update the lastupdated time for this album
				cur.execute("UPDATE Album SET lastupdated = Now() WHERE albumid = %s", [album_id])
				# cur.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + album_id + " AND P.picid = C.picid ORDER BY sequencenum")
				# pic_result = cur.fetchall()
				# cur.execute("SELECT title FROM Album WHERE albumid = " + album_id)
				# album_result = cur.fetchall()

				# options = {
				# 	"edit": True,
				# 	"albumid": album_id,
				# 	"album_title": album_result[0]['title'],
				# 	"pictures": pic_result
				# }
				return redirect(request.url)




@album.route('/album', methods=['GET', 'POST'])
def album_route():
	db = connect_to_database()
	cur = db.cursor()
	album_id = request.args.get('albumid')
	if request.method == "GET":
		cur.execute("SELECT albumid FROM Album WHERE albumid = %s", [album_id])
		r = cur.fetchall()
		if not r:
			return abort(404)
		else:
			cur.execute("SELECT C.picid, C.caption, P.date, P.format FROM Contain C, Photo P WHERE C.albumid = " + str(album_id) + " AND P.picid = C.picid ORDER BY sequencenum")
			pic_result = cur.fetchall()
			# for pic in pic_result:
			# 	pic['date'] = str(pic['date'])
			# 	print(type(pic['date']))
			# 	print(pic['date'])

			cur.execute("SELECT title FROM Album WHERE albumid = " + str(album_id))
			album_result = cur.fetchall()
			cur.execute("SELECT username FROM Album WHERE albumid = " + str(album_id))
			album_username= str(cur.fetchall()[0]['username'])

		# print(album_result)

		if 'username' in session:
			username = session['username']
			cur.execute("SELECT firstname, lastname FROM User WHERE username = '" + username + "'")
			user = cur.fetchall()[0]
			cur.execute("SELECT albumid FROM Album WHERE (access = 'public' AND albumid = " + str(album_id) + ") OR (username = '" + username + "' AND albumid = " + str(album_id) + ") UNION SELECT albumid FROM AlbumAccess WHERE username = '" + username + "' AND albumid = " + str(album_id) )
			access_albums = cur.fetchall()
			# access_albums are whether <username> can access <albumid>
			if not access_albums:
				return abort(403)
			
			link = True
			if album_username != username:
				link = False
			options = {
				"edit": False,
				"user": user,
				"edit_link": link,
				"albumid": album_id,
				"album_title": album_result[0]['title'],
				"pictures": pic_result,
				"album_username": album_username
			}
			return render_template("album.html", **options)
		else:
			cur.execute("SELECT access FROM Album WHERE albumid = " + str(album_id))
			access = str(cur.fetchall()[0]['access'])
			if access == 'private':
				return redirect(url_for('user.login_route'))
			else:

				options = {
					"edit": False,
					"edit_link": False,
					"albumid": album_id,
					"album_title": album_result[0]['title'],
					"pictures": pic_result,
					"album_username": album_username
				}
				return render_template("album.html", **options)

	elif request.method == "POST":
		return abort(404)



