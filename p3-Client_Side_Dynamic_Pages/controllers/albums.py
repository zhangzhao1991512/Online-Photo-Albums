from flask import *

import MySQLdb
import MySQLdb.cursors
#from extensions import db
import extensions
db = extensions.connect_to_database()

#options = {'host': 'localhost',
#           'user': 'group105',
#           'passwd': 'bowenjackminzhe',
#           'db': 'group105db',
#           'cursorclass': MySQLdb.cursors.DictCursor}
#db = MySQLdb.connect(**options)
#db.autocommit(True)


cur = db.cursor()
cur1 = db.cursor()
cur2 = db.cursor()
cur3 = db.cursor()
cur4 = db.cursor()
cur5 = db.cursor()

c = db.cursor()
c1 = db.cursor()

albums = Blueprint('albums', __name__, template_folder='templates')


@albums.route('/albums/edit', methods=['GET','POST'])
def albums_edit_route():
	#                u = request.args.get('username')
#                c.execute("SELECT username FROM User WHERE username = %s", [u])
#                r = c.fetchall()
#                if not r:
#                        return abort(404)
        #-------First we need to check whether there is a session------#
#	c1.execute("SELECT username FROM User")
#	name = c1.fetchall()
#	c1.execute("SELECT COUNT(username) FROM User")
#	temp = c1.fetchall()
#	n = int(temp[0]['COUNT(username)'])
#	i = 0
#	no_session = True
#	while(i < n):
#		u = str(name[i]['username'])
#		if u == session['username']:
#			no_session = False
#		i=i+1

#	if (no_session):
#		return "Sorry, you cannot access this page..."
#		return abort(403)
	if 'username' not in session:
		return redirect(url_for('main.login_route'))
        #---------------------------------------------------------------
	
	if request.method == 'POST':
		#id = request.form['albumid']
		#return id
		if request.form['op'] == "delete":
	#-------------------------New delete AlbumAccess----------------------
			cur2.execute("Delete FROM AlbumAccess WHERE albumid = '" + request.form['albumid'] + "'")

			cur2.execute("Delete P, C from Photo P JOIN Contain C ON P.picid = C.picid And C.albumid = " + request.form['albumid'])
#			cur2.execute("Delete from Contain WHERE  albumid = '" + request.form['albumid'] +"'")
			cur2.execute("Delete from Album WHERE  albumid = '" + request.form['albumid'] +"'")
			cur2.execute("SELECT albumid,title FROM Album WHERE username = '" + session['username'] +"'");
			results = cur2.fetchall()
		if request.form['op'] == 'add':
#!!!!!!			cur3.execute("Select Max(sequencenum) from Contain")
#			res = cur3.fetchall()
#			next_sequencenum = str (res[0]["Max(sequencenum)"])
#			a = int (next_sequencenum)
#!!!!!!			a = a + 1
                	cur4.execute("Insert Into Album (title, username, access) Values ('" + request.form['title'] +"', '" + session['username'] + "', 'private')")
			cur4.execute("SELECT albumid,title FROM Album WHERE username = '" + session['username'] +"'");
                        results = cur4.fetchall()	
		
		c1.execute("SELECT username, firstname, lastname From User WHERE username = '" + session['username'] + "'")
		thisuser = (c1.fetchall())[0]
		options = {
			"login": True,
			"thisuser": thisuser,
			"edit": True,
			"username": request.args.get('username'),
			"albums": results
		}
                return render_template("albums.html", **options)
	else:
		c.execute("SELECT username, firstname, lastname From User WHERE username = '" + session['username'] + "'")
		thisuser = (c.fetchall())[0]
		res = get_user_albums()
		options = {
			"login": True,
			"thisuser": thisuser,
			"edit": True,
			"username": request.args.get('username'),
			"albums": res
		}
		return render_template("albums.html", **options)

#@albums.route('/albums')
@albums.route('/albums', methods=['GET','POST'])
def albums_route():
	if  request.method == 'GET':
		if not request.args.get('username'):
			if 'username' not in session:
				return abort(403)
			else:
				c1.execute("SELECT username, firstname, lastname From User WHERE username = '" + session['username'] + "'")
				thisuser = (c1.fetchall())[0]
				c1.execute("SELECT albumid, title FROM Album WHERE username = '" + session['username'] + "'")
				wow =  c1.fetchall()
				options = {
					"login": True,
					"thisuser": thisuser,
					"edit": False,
					"edit_link": True,
					"username": session['username'],
					"albums": wow
				}
				return render_template("albums.html", **options)
		else:
			u = request.args.get('username')
			cur5.execute("SELECT username FROM User WHERE username = %s", [u])
	                r = cur5.fetchall()
        	        if not r:
				return abort(404)
			#--------------First, we also need to know if there is a session------------#
			if 'username' not in session:
				public_albums = get_user_public_albums()
				options = {
					"login": False,
					"edit": False,
					"edit_link": False,
					"username": request.args.get('username'),
					"albums": public_albums
				}
				return render_template("albums.html", **options)	
		#---------------------------------------------------------------------------#
			else:
				cur5.execute("SELECT username, firstname, lastname From User WHERE username = '" + session['username'] + "'")
        	                thisuser = (cur5.fetchall())[0]
				results = get_user_public_albums()
				#------------------------#
				#a = True --- HAHAHA NO MATTER WHAT, there should be link to edit
				#------------------------#
				a = False
				if thisuser['username'] != u:
					a = False
#					cur5.execute("SELECT albumid, title FROM Album WHERE username = '" + u + "' AND access = 'public' ")
#					results = cur5.fetchall()
				options = {
					"login": True,
					"thisuser": thisuser,
					"edit": False,
					"edit_link": a,
					"username": request.args.get('username'),
					"albums": results
		        	}
				return render_template("albums.html", **options)
	else:
		return abort(404)


#'''return selected username and his albums'''
def get_user_albums():
	#get username from albums.html
	username = session['username']
	cur = db.cursor()
	cur.execute("SELECT albumid, title FROM Album WHERE username = %s", [username]);
	results = cur.fetchall()
	return results

def get_user_public_albums(): 
	#get username from albums.html
	username = request.args.get('username')
	cur = db.cursor()
	cur.execute("SELECT albumid, title FROM Album WHERE username = %s AND access = 'public'", [username]);
	results = cur.fetchall()
	return results

