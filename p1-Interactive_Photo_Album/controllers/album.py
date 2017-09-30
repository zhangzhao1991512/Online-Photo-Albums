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
	if request.method == "GET":
		cur.execute("SELECT albumid FROM Album WHERE albumid = %s", [album_id])
		r = cur.fetchall()
		if not r:
			return abort(404)
		else:
			cur.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + album_id + " AND P.picid = C.picid ORDER BY sequencenum")
			pic_result = cur.fetchall()
			cur.execute("SELECT title FROM Album WHERE albumid = " + album_id)
			album_result = cur.fetchall()
		# print(album_result)


		options = {
			"edit": True,
			"albumid": album_id,
			"album_title": album_result[0]['title'],
			"pictures": pic_result
		}
		return render_template("album.html", **options)

	elif request.method == "POST":
		if request.form['op'] == 'delete':
			picid = request.form['picid']
			
			cur.execute("SELECT format FROM Photo WHERE picid = '" + picid + "'" )
			pic_format = str(cur.fetchall()[0]['format'])

			cur.execute("DELETE FROM Contain WHERE picid = '" + picid + "'")
			cur.execute("DELETE FROM Photo WHERE picid = '" + picid + "'" )
			#update the lastupdated time for this album
			cur.execute("UPDATE Album SET lastupdated = Now() WHERE albumid = %s", [album_id])
			cur.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + album_id + " AND P.picid = C.picid ORDER BY sequencenum")
			pic_result = cur.fetchall()
			cur.execute("SELECT title FROM Album WHERE albumid = " + album_id)
			album_result = cur.fetchall()

			#the path can change!!!!!!!!!!!!!!!!!
			os.remove("./static/images/" + picid + "." + pic_format)

			options = {
				"edit": True,
				"albumid": album_id,
				"album_title": album_result[0]['title'],
				"pictures": pic_result
			}
			return render_template("album.html", **options)

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
				cur.execute("INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (" + str(seq) + ", " + album_id + ", '" + new_picid + "', '' )")
				#update the lastupdated time for this album
				cur.execute("UPDATE Album SET lastupdated = Now() WHERE albumid = %s", [album_id])
				cur.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + album_id + " AND P.picid = C.picid ORDER BY sequencenum")
				pic_result = cur.fetchall()
				cur.execute("SELECT title FROM Album WHERE albumid = " + album_id)
				album_result = cur.fetchall()

				options = {
					"edit": True,
					"albumid": album_id,
					"album_title": album_result[0]['title'],
					"pictures": pic_result
				}
				return render_template("album.html", **options)




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
			cur.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + album_id + " AND P.picid = C.picid ORDER BY sequencenum")
			pic_result = cur.fetchall()
			cur.execute("SELECT title FROM Album WHERE albumid = " + album_id)
			album_result = cur.fetchall()
		# print(album_result)


		options = {
			"edit": False,
			"albumid": album_id,
			"album_title": album_result[0]['title'],
			"pictures": pic_result
		}
		return render_template("album.html", **options)



