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

albums = Blueprint('albums', __name__, template_folder='templates', url_prefix='/sz2es3gbxzw9i50442t9/p1')


@albums.route('/albums/edit', methods=['GET','POST'])
def albums_edit_route():
        if  request.method == 'GET':
		#abort 404
		username = request.args.get('username')
		cur5.execute("SELECT username FROM User WHERE username = %s", [username])
		results = cur5.fetchall()
		if not results:
			return abort(404)
		#original part
                res = get_user_albums()
		options = {
			"edit": True,
			"username": request.args.get('username'),
			"albums": res
		}
                return render_template("albums.html", **options)
        else:
		if request.form['op'] == "delete":
			cur2.execute("Delete P, C from Photo P JOIN Contain C ON P.picid = C.picid And C.albumid = " + request.form['albumid'])
#			cur2.execute("Delete from Contain WHERE  albumid = '" + request.form['albumid'] +"'")
			cur2.execute("Delete from Album WHERE  albumid = '" + request.form['albumid'] +"'")
			cur2.execute("SELECT albumid,title FROM Album WHERE username = '" + request.args.get('username') +"'");
			results = cur2.fetchall()
		if request.form['op'] == 'add':
                	cur4.execute("Insert Into Album (title, username) Values ('" + request.form['title'] +"', '" + request.form['username']+ "')")
			cur4.execute("SELECT albumid,title FROM Album WHERE username = '" + request.args.get('username') +"'");
                        results = cur4.fetchall()	
		options = {
            "edit": True,
			"username": request.args.get('username'),
			"albums": results}
                return render_template("albums.html", **options)



#@albums.route('/albums')
@albums.route('/albums', methods=['GET','POST'])
def albums_route():
	if  request.method == 'GET':
		#check 404
		username = request.args.get('username')
		cur6 = db.cursor()
		cur6.execute("SELECT username FROM User WHERE username = %s", [username])
        res = cur6.fetchall()
       	if not res:
        	return abort(404)
        #original part
		results = get_user_albums()
		albumid_list = get_albumid_list()
		if results[0] not in albumid_list:
			abort(404)
		else:
			options = {
				"edit": False,
				"username": request.args.get('username'),
	            "albums": results
		        }
		return render_template("albums.html", **options)
	else:
		options = {
			"edit": False
	    	}
	    	return render_template("albums.html", **options)


'''return selected username and his albums'''
def get_user_albums():
	#get username from albums.html
	username = request.args.get('username')
	cur = db.cursor()
	cur.execute("SELECT albumid, title FROM Album WHERE username = %s", [username]);
	results = cur.fetchall()
	return results

def get_albumid_list():
	cur = db.cursor()
	cur.execute("SELECT albumid FROM Album WHERE *");
	albumid_list = cur.fetchall()
	return albumid_list
