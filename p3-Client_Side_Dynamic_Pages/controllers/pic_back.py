from flask import *
import MySQLdb
import MySQLdb.cursors
#from extensions import db

import extensions
db = extensions.connect_to_database()


cur = db.cursor()
cur1 = db.cursor()
cur2 = db.cursor()
cur3 = db.cursor()

pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/pic', methods=['GET','POST'])
def pic_route():
	if  request.method == 'GET':
		u = request.args.get('picid')
                cur.execute("SELECT picid FROM Photo WHERE picid = %s", [u])
                r = cur.fetchall()
                if not r:
                        return abort(404)

                cur.execute("SELECT albumid FROM Contain WHERE picid = '" + request.args.get('picid') +"'")
                res = cur.fetchall()
		albumid = str (res[0]['albumid'])
#		return albumid
		cur.execute("SELECT format FROM Photo WHERE picid = '" + request.args.get('picid') + "'")
		res1 = cur.fetchall()
		form = str (res1[0]['format'])
#		return form
		cur.execute("SELECT picid FROM Contain WHERE albumid = " + albumid + " order by sequencenum")
		res2 = cur.fetchall()
		
		cur.execute("SELECT COUNT(picid) FROM Contain where albumid = " + albumid)
		countres = cur.fetchall()
		count = int (countres[0]['COUNT(picid)'])
		count = count - 1;
		first_id = str (res2[0]['picid'])
		if first_id == request.args.get('picid'):
			prev = False
		else:
			prev = True

		last_id = str (res2[count]['picid'])
		if last_id == request.args.get('picid'):
                        nex = False
                else:
                        nex = True
		index = 0
		i = 0
		while (i < count+1):
			if request.args.get('picid') == str(res2[i]['picid']):
				index = i
			i = i + 1 
		prev_picid = ""
		next_picid = ""
		if (prev):
			prev_picid = res2[index-1]['picid']
			#return str (index)
		
		if (nex):
			next_picid = res2[index+1]['picid']
	
		cur1.execute("SELECT caption FROM Contain WHERE picid = '" + request.args.get('picid') +"'")
		caption = str(cur1.fetchall()[0]['caption'])

		if 'username' in session:
			cur1.execute("SELECT A.albumid FROM Album A, Contain C WHERE C.picid = '" + request.args.get('picid') +"' AND ((A.access = 'public' AND A.albumid = C.albumid) OR (A.username = '" + session['username']+ "' AND A.albumid = C.albumid)) UNION SELECT A1.albumid FROM AlbumAccess A1, Contain C1 WHERE username = '" + session['username'] + "' AND A1.albumid = C1.albumid AND C1.picid ='" + request.args.get('picid') +"'")
			access_albums = cur1.fetchall()
			if not access_albums:
				return abort(403)
			
			cur1.execute("SELECT username, firstname, lastname From User WHERE username = '" + session['username'] + "'")
			thisuser = (cur1.fetchall())[0]
			edit = True
			cur1.execute("SELECT A.albumid FROM Album A, Contain C WHERE C.picid = '" + request.args.get('picid') +"' AND A.username = '" + session['username']+ "' AND A.albumid = C.albumid")
                        access_pic = cur1.fetchall()
                        if not access_pic:
                                edit = False
			options = {
				"login": True,
				"thisuser": thisuser,
				"caption": caption,
                        	"edit": edit,
				"albumid": albumid,
				"prev_picid": prev_picid,
				"prev_picid_Bool": prev,
	                        "cur_picid": request.args.get('picid'),
				"format": form,
				"next_picid": next_picid,
				"next_picid_Bool": nex
	                }
			return render_template("pic.html", **options)
		else:
			cur2.execute("SELECT A.access FROM Album A, Contain C WHERE C.albumid = A.albumid AND C.picid = '" + request.args.get('picid') + "'")
			access = str (cur2.fetchall()[0]['access'])
			if access == 'private':
				return redirect(url_for('main.login_route'))
                        else:
				options = {
					"login": False,
					"caption": caption,
					"edit": False,
					"albumid": albumid,
					"prev_picid": prev_picid,
					"prev_picid_Bool": prev,
					"cur_picid": request.args.get('picid'),
					"format": form,
					"next_picid": next_picid,
					"next_picid_Bool": nex
				}
				return render_template("pic.html", **options)
        else:
                if request.form['op'] == "caption":
			picid = request.form['picid']
			new_caption = request.form['caption']
			cur3.execute("UPDATE Contain SET caption = '" + new_caption + "' WHERE picid = '" + picid +"'")
			cur3.execute("SELECT albumid FROM Contain WHERE picid = '" + picid +"'")
			albumid = str (cur3.fetchall()[0]['albumid'])
			cur3.execute("UPDATE Album SET lastupdated=Now() WHERE albumid = " + albumid)
			return redirect(request.url)
