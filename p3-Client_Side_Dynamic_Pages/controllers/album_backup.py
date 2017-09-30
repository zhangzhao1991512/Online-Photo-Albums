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

album = Blueprint('album', __name__, template_folder='templates', url_prefix='/sz2es3gbxzw9i50442t9/p1')


def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@album.route('/album/edit', methods=['GET','POST'])
def album_edit_route():
	if  request.method == 'GET':
		cur6.execute("SELECT albumid FROM Album")
		a_id = cur6.fetchall()
		cur6.execute("SELECT count(*) from Album")
		count_album = cur6.fetchall()
		n = int (count_album[0]["count(*)"])
		return str(n)
#		if request.args.get('albumid') not in a_id['albumid']:
#			abort(404)
		
#		return  request.args.get('albumid')
                cur1.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + request.args.get('albumid') +" AND P.picid = C.picid Order by sequencenum")
                results = cur1.fetchall()
		
                options = {
                        "edit": True,
			"albumid": request.args.get('albumid'),
                        "picname": results
                }
                return render_template("album.html", **options)

        elif request.method == 'POST':
                if request.form['op'] == "delete":
			cur3.execute("SELECT format FROM Photo WHERE picid = '" + request.form['picid'] + "'")
			r = cur3.fetchall()
			form = str (r[0]['format'])

			cur3.execute("DELETE FROM Contain WHERE picid = '" + request.form['picid'] + "'")
			cur3.execute("DELETE FROM Photo WHERE picid = '" + request.form['picid'] + "'")
			##HERE WE UPDATE THE lastupdated TIME FOR THIS ALBUM
			cur3.execute("UPDATE Album SET lastupdated=Now() WHERE albumid = " + request.form['albumid'])

			cur3.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + request.args.get('albumid') +" AND P.picid = C.picid Order by sequencenum")
	                results = cur3.fetchall()
			
			os.remove("./static/images/" + request.form['picid']+"."+ form)

                	options = {
                        	"edit": True,
                        	"albumid": request.args.get('albumid'),
                        	"picname": results
                	}
			return render_template("album.html", **options)

		if request.form['op'] == "add":
			# check if the post request has the file part
			if 'file' not in request.files:
            			#return "oooooooooooooooo"
				#flash('No file part')
            			return redirect(request.url)
        		
			file = request.files['file']
        		# if user does not select file, browser also submit a empty part without filename
			if file.filename == '':
				#return "AAAAAAAAAA"
            			#flash('No selected file')
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
#				newpath = "/static/images" + new_picid + "." + a[1]
#				os.rename(filename ,new_filename)
#				return "ahahahahaha"
				
				cur5.execute("SELECT Max(sequencenum) FROM Contain")
				res = cur5.fetchall()
				next_sequencenum = str (res[0]["Max(sequencenum)"])
				b = int (next_sequencenum)
				b = b + 1
#				return a
#				return "INSERT INTO Photo(picid, format) VALUES ('" + new_picid + "', '" + a[1] + "')"				
				cur4.execute("INSERT INTO Photo(picid, format) VALUES ('" + new_picid + "', '" + a[1] + "')")
#				return "????"
				cur4.execute("INSERT INTO Contain(sequencenum, albumid, picid, caption) VALUES (" + str(b) + ", " + request.form['albumid'] + ", '" + new_picid + "', '')")
#				return "oh"
				cur4.execute("UPDATE Album SET lastupdated=Now() WHERE albumid = " + request.form['albumid'])
#				return "here"
				cur4.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + request.args.get('albumid') +" AND P.picid = C.picid Order by sequencenum")
				results = cur4.fetchall()
				options = {
                                	"edit": True,
                                	"albumid": request.args.get('albumid'),
                                	"picname": results
                        	}
				return render_template("album.html", **options)


#@album.route('/album')
@album.route('/album', methods=['GET','POST'])
def album_route():
	if  request.method == 'GET':
		cur.execute("SELECT C.picid, P.format FROM Contain C, Photo P WHERE C.albumid = " + request.args.get('albumid') +" AND P.picid = C.picid Order by sequencenum")
		results = cur.fetchall()
		cur2.execute( "SELECT username FROM Album WHERE albumid = " + request.args.get('albumid') )
		res = cur2.fetchall()
		username = str (res[0]["username"])
		options = {
			"edit": False,
			"albumid": request.args.get('albumid'),
			"picname": results,
			"username": username
		}
		return render_template("album.html", **options)

	elif request.method == 'POST':
		options = {
                        "edit": False

                }
                return render_template("album.html", **options)
#	else :
#		cur100.execute("SELECT C.Albumid, C.picid, P.format FROM Contain C, Photo P WHERE P.picid = C.picid Order by sequencenum")
#		results = cur100.fetchall()
#		options = {
#                        "edit": False,			
#                }
#                return render_template("album.html", **options)
 
