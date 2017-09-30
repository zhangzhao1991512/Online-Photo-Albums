from flask import *
from extensions import connect_to_database
pic = Blueprint('pic', __name__, template_folder='templates')

@pic.route('/pic', methods=['GET', 'POST'])
def pic_route():
	db = connect_to_database()
	cur = db.cursor()
	if request.method == 'GET':
		pic = request.args.get('picid')
		cur.execute("SELECT picid FROM Photo WHERE picid = %s;", [pic])
		r = cur.fetchall()
		if not r:
			return abort(404)
		else:
			cur.execute("SELECT albumid FROM Contain WHERE picid = %s", [pic])
			albumid = cur.fetchall()[0]['albumid']
			cur.execute("SELECT format FROM Photo WHERE picid = %s", [pic])
			pic_format = cur.fetchall()[0]['format']

			#find out how many pitures there are in the album, and whether to show the prev or next button
			cur.execute("SELECT picid FROM Contain WHERE albumid = " + str(albumid) + " ORDER BY sequencenum")
			pictures = cur.fetchall()
			cur.execute("SELECT COUNT(picid) FROM Contain WHERE albumid = %s", [albumid])
			num_pics = int (cur.fetchall()[0]['COUNT(picid)'])

			#the index of current picture
			i = 0
			while (i<num_pics):
				if pic == pictures[i]['picid']:
					index = i
					break
				i+=1

			# first_picid = pictures[0]['picid']
			# if pic == first_picid:
			# 	prev_pic = False
			# else:
			# 	prev_pic = True
			# 	prev_picid = pictures[index-1]['picid']


			# last_picid = pictures[num_pics-1]['picid']
			# if pic == last_picid:
			# 	nex == False
			# else:
			# 	nex == True
			# 	next_picid == pictures[index+1]['picid']
			prev_picid = ""
			next_picid = ""

			if index == 0:
				prev_pic = False
			else:
				prev_pic = True
				prev_picid = pictures[index-1]['picid']

			if index == num_pics-1:
				next_pic = False
			else:
				next_pic = True
				next_picid = pictures[index+1]['picid']

			cur.execute("SELECT caption FROM Contain WHERE picid = '" + pic + "'")
			caption = str(cur.fetchall()[0]['caption'])

			if 'username' in session:
				username = session['username']
				cur.execute("SELECT firstname, lastname FROM User WHERE username = '" + username + "'")
				user = cur.fetchall()[0]



				cur.execute("SELECT A.albumid FROM Album A, Contain C WHERE C.picid = '" + pic \
					+ "' AND ((A.access = 'public' AND A.albumid = C.albumid) OR (A.username = '" + username + \
					"' AND A.albumid = C.albumid)) UNION SELECT A1.albumid FROM AlbumAccess A1, Contain C1 WHERE C1.picid = '" + pic \
					+ "' AND A1.username = '" + username + "' AND A1.albumid = C1.albumid")
				access_album = cur.fetchall()
				if not access_album:
					return abort(403)

				edit = True
				cur.execute("SELECT A.albumid FROM Album A, Contain C WHERE A.albumid = C.albumid AND C.picid = '" + pic + "' AND A.username = '" + username +"'")
				own_album = cur.fetchall()
				if not own_album:
					edit = False
				options = {
					"user": user,
					"edit": edit,
					"caption": caption,
					"albumid": albumid,
					"current_picid": pic,
					"prev_pic": prev_pic,
					"prev_picid": prev_picid,
					"next_pic": next_pic,
					"next_picid": next_picid,
					"format": pic_format
				}
				return render_template("pic.html", **options)
			else:
				cur.execute("SELECT A.access FROM Album A, Contain C WHERE C.albumid = A.albumid AND C.picid = '" + pic +"'")
				access = str(cur.fetchall()[0]['access'])
				if access == "private":
					return redirect(url_for('user.login_route'))
				else:
					options = {
						"edit": False,
						"caption": caption,
						"albumid": albumid,
						"current_picid": pic,
						"prev_pic": prev_pic,
						"prev_picid": prev_picid,
						"next_pic": next_pic,
						"next_picid": next_picid,
						"format": pic_format
					}
					return render_template("pic.html", **options)

	elif request.method == 'POST':
		if request.form['op'] == "caption":
			picid = request.form['picid']
			new_caption = request.form['caption']
			cur.execute("UPDATE Contain SET caption = '" + new_caption + "' WHERE picid = '" + picid + "'")
			cur.execute("SELECT albumid FROM Contain WHERE picid = '" + picid + "'")
			albumid = cur.fetchall()[0]['albumid']
			cur.execute("UPDATE Album SET lastupdated = Now() WHERE albumid = " + str(albumid))
			return redirect(request.url)


















			

