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
#app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#connect to database db

cur = db.cursor()
cur1 = db.cursor()
cur2 = db.cursor()
cur3 = db.cursor()
cur4 = db.cursor()
cur5 = db.cursor()
cur6 = db.cursor()

album = Blueprint('album', __name__, template_folder='templates')


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@album.route('/album/edit', methods=['GET','POST'])
def album_edit_route():
	#-------------First check whether there is a session------------
	no_session = True
	if 'username' in session:
		no_session = False
	if (no_session):	
		return abort(403)

	if  request.method == 'GET':
                u = request.args.get('albumid')
                cur1.execute("SELECT albumid FROM Album WHERE albumid = %s", [u])
		check = cur1.fetchall()
                if not check:
                        return abort(404)
		cur1.execute("SELECT albumid FROM Album WHERE albumid = %s AND username = '" + session['username'] + "'", [u])
		check1 = cur1.fetchall()		
		if not check1:
			return abort(403)
		#order by sequencenum#
		cur1.execute("SELECT C.picid, C.caption, P.format, P.date FROM Contain C, Photo P WHERE C.albumid = " + request.args.get('albumid') +" AND P.picid = C.picid Order by sequencenum")
                results = cur1.fetchall()
		cur1.execute("SELECT username, firstname, lastname From User WHERE username = '" + session['username'] + "'")
		thisuser = (cur1.fetchall())[0]
                #----------------Here we check whether the album is public or private-------If private, who are the granted users
		cur1.execute("SELECT access FROM Album WHERE albumid = '" + request.args.get('albumid') + "'")
		access = str( (cur1.fetchall())[0]['access'] )
		p = True
		if access == 'public':
			p = False
		if access == 'private':
			p = True

		cur1.execute("SELECT username FROM AlbumAccess WHERE albumid = '" + request.args.get('albumid') + "'")
		users = cur1.fetchall()
		cur1.execute("SELECT title FROM Album WHERE albumid = '" + request.args.get('albumid') +"'")
		title = str( cur1.fetchall()[0]['title'])
		#---------------------------------------------------------------------------
		options = {
			"login": True,
			"thisuser": thisuser,
			"edit": True,
			"private": p,
			"title": title,
			"users": users,
			"albumid": request.args.get('albumid'),
                        "information": results
                }
                return render_template("album.html", **options)

        elif request.method == 'POST':
		if request.form['op'] == "access":
#			return request.form['access']
			cur3.execute("UPDATE Album SET lastupdated=Now() WHERE albumid = " + request.form['albumid'])
			cur3.execute("UPDATE Album SET access = '" + request.form['access'] + "' WHERE albumid = " + request.form['albumid'])
			if request.form['access'] == 'public':
				cur3.execute("DELETE FROM AlbumAccess WHERE albumid = " + request.form['albumid'])
			return redirect(request.url)
		if request.form['op'] == "grant":
			#return request.form["albumid"]
			cur3.execute("UPDATE Album SET lastupdated=Now() WHERE albumid = " + request.form['albumid'])
			#-----check whether it is a valid username0----#
			cur3.execute("SELECT username FROM User WHERE username = %s", [ request.form["username"] ])
			check = cur3.fetchall()
			if not check:
				return redirect(request.url)
			#----------------------------------------------#
			#return session["username"]
			if request.form["username"] == session["username"]:
				return redirect(request.url)
			cur3.execute("SELECT username FROM AlbumAccess WHERE username = '" + request.form["username"] + "' AND albumid = " + request.form["albumid"])	
			not_access = cur3.fetchall();
			if not not_access:
				cur3.execute("INSERT INTO AlbumAccess Values (" + request.form["albumid"] + ", '" + request.form["username"] +"')")
			return redirect(request.url)
		if request.form['op'] == "revoke":
			cur3.execute("UPDATE Album SET lastupdated=Now() WHERE albumid = " + request.form['albumid'])
			cur3.execute("DELETE FROM AlbumAccess WHERE username = '" + request.form["username"] + "' AND albumid = " + request.form['albumid'])
			return redirect(request.url)
                if request.form['op'] == "delete":
			cur3.execute("SELECT format FROM Photo WHERE picid = '" + request.form['picid'] + "'")
			r = cur3.fetchall()
			form = str (r[0]['format'])
			cur3.execute("DELETE FROM Contain WHERE picid = '" + request.form['picid'] + "'")
			cur3.execute("DELETE FROM Photo WHERE picid = '" + request.form['picid'] + "'")
			##HERE WE UPDATE THE lastupdated TIME FOR THIS ALBUM
			cur3.execute("UPDATE Album SET lastupdated=Now() WHERE albumid = " + request.form['albumid'])

#			cur3.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + request.args.get('albumid') +" AND P.picid = C.picid Order by sequencenum")
#	                results = cur3.fetchall()
			
			os.remove("./static/images/" + request.form['picid']+"."+ form)
#                	options = {
#                        	"edit": True,
#                        	"albumid": request.args.get('albumid'),
#                        	"picname": results
#                	}
#			return render_template("album.html", **options)
			return redirect(request.url)

		if request.form['op'] == "add":
			# check if the post request has the file part
			if 'file' not in request.files:
            			#return "oooooooooooooooo"
				#flash('No file part')
            			return redirect(request.url)
        		
			file = request.files['file']
        		# if user does not select file, browser also submit a empty part without filename
			if file.filename == '':
            			return redirect(request.url)
			
			if file and allowed_file(file.filename):
            			filename = secure_filename(file.filename)
            			a = filename.split('.')
				#return a[1]
				new_picid = (hashlib.md5(request.form['albumid'] + filename)).hexdigest()
				#return new_picid
#				file.save( os.path.join("./static/images/", new_picid + "." + a[1])) 
				new_filename = os.path.join("./static/images/" + new_picid + "." + a[1])
				file.save(new_filename)
				
				cur5.execute("SELECT Max(sequencenum) FROM Contain")
				res = cur5.fetchall()
				next_sequencenum = str (res[0]["Max(sequencenum)"])
				b = int (next_sequencenum)
				b = b + 1
				cur4.execute("INSERT INTO Photo(picid, format) VALUES ('" + new_picid + "', '" + a[1] + "')")
				cur4.execute("INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (" + str(b) + ", " + request.form['albumid'] + ", '" + new_picid + "', '')")
				cur4.execute("UPDATE Album SET lastupdated=Now() WHERE albumid = " + request.form['albumid'])
#				cur4.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + request.args.get('albumid') +" AND P.picid = C.picid Order by sequencenum")
#				results = cur4.fetchall()
#				options = {
#                                	"edit": True,
#                                	"albumid": request.args.get('albumid'),
#                                	"picname": results
#                        	}
#				return render_template("album.html", **options)
				return redirect(request.url)

#@album.route('/album')
@album.route('/album', methods=['GET','POST'])
def album_route():
	if request.method == 'GET':
		if 'username' in session:
			cur2.execute("SELECT username, firstname, lastname From User WHERE username = '" + session['username'] + "'")
			thisuser = (cur2.fetchall())[0]
			options = {
				"login": True,
				"thisuser": thisuser,
				"edit": False,
				"albumid": request.args.get('albumid')
			}
			return render_template("album.html", **options)
		else:
			options = {
				"login": False,
				"edit": False,
				 "albumid": request.args.get('albumid')
			}
			return render_template("album.html", **options)

#	if  request.method == 'GET':
#		u = request.args.get('albumid')
#                cur2.execute("SELECT albumid FROM Album WHERE albumid = %s", [u])
#                r = cur2.fetchall()
#                if not r:
#                        return abort(404)
		
#		cur2.execute("SELECT C.picid, C.caption, P.format, P.date FROM Contain C, Photo P WHERE C.albumid = " + request.args.get('albumid') +" AND P.picid = C.picid Order by sequencenum")
#		cur2.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + request.args.get('albumid') +" AND P.picid = C.picid Order by sequencenum")
#		results = cur2.fetchall()
#		cur2.execute( "SELECT username FROM Album WHERE albumid = " + request.args.get('albumid') )
#		res = cur2.fetchall()
#		username = str (res[0]["username"])
#
#		if 'username' in session:
#			#-----if the user can access the album----#
#			cur2.execute("SELECT albumid FROM Album WHERE (access = 'public' AND albumid = " + request.args.get('albumid') + ") OR (username = '" + session['username']+ "' AND albumid = " + request.args.get('albumid') + ") UNION SELECT albumid FROM AlbumAccess WHERE username = '" + session['username'] + "' AND albumid = " + request.args.get('albumid'))
#			access_albums = cur2.fetchall()
#			if not access_albums:
#				return abort(403)
#			#-----------------------------------------#
#			cur2.execute("SELECT username, firstname, lastname From User WHERE username = '" + session['username'] + "'")
#			thisuser = (cur2.fetchall())[0]
#			cur2.execute("SELECT title FROM Album WHERE albumid = '" + request.args.get('albumid') +"'")
#			title = str( cur2.fetchall()[0]['title'])
#
#			a = True
#			cur2.execute("SELECT username From Album WHERE albumid = " + request.args.get('albumid'))
#			b = str (cur2.fetchall()[0]['username'])
#			if b != session['username']:
#				a = False
#			options = {
#				"login": True,
#				"thisuser": thisuser,
#				"title": title,
#				"edit": False,
#				"edit_link": a,
#				"albumid": request.args.get('albumid'),
#				"information": results,
#				"username": username
#			}
#			return render_template("album.html", **options)
#		else:
#			cur2.execute("SELECT access FROM Album WHERE albumid = " + request.args.get('albumid'))
#			access = str (cur2.fetchall()[0]['access'])
#			if access == 'private':
#				return redirect(url_for('main.login_route'))
#			else:
#				cur2.execute("SELECT title FROM Album WHERE albumid = '" + request.args.get('albumid') +"'")
#				title = str( cur2.fetchall()[0]['title'])
#				options = {
#					"login": False,
#					"edit": False,
#					"edit_link": False,
#					"title": title,
#					"albumid": request.args.get('albumid'),
#					"information": results,
#					"username": username
#                        }
#                        return render_template("album.html", **options)
					

#	elif request.method == 'POST':
#		return abort(404)
#		options = {
#                        "edit": False
#                }
#                return render_template("album.html", **options)
#	else :
#		cur100.execute("SELECT C.Albumid, C.picid, P.format FROM Contain C, Photo P WHERE P.picid = C.picid Order by sequencenum")
#		results = cur100.fetchall()
#		options = {
#                        "edit": False,			
#                }
#                return render_template("album.html", **options)
 
