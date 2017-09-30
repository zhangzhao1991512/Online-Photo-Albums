from flask import *
import MySQLdb
import MySQLdb.cursors
#from extensions import db

import extensions
db = extensions.connect_to_database()


cur = db.cursor()
cur1 = db.cursor()

pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/pic', methods=['GET','POST'])
def pic_route():
	if request.method == 'GET':
		if 'username' in session:
			haha = True
			cur.execute("SELECT A.albumid FROM Album A, Contain C WHERE C.picid = '" + request.args.get('picid') +"' AND A.username = '" + session['username']+ "' AND A.albumid = C.albumid")
                        access_pic = cur.fetchall()
                        if not access_pic:
                                haha = False

			cur1.execute("SELECT username, firstname, lastname From User WHERE username = '" + session['username'] + "'")
			thisuser = (cur1.fetchall())[0]
			options = {
				"login": True,
				"thisuser": thisuser,
				"picid": request.args.get('picid'),
				"permission": haha
			}
			return render_template("pic.html", **options)
		else:
			options = {
				"login": False,
				"picid": request.args.get('picid'),
				"permission": False
			}
			return render_template("pic.html", **options)
