from flask import *

from extensions import connect_to_database

main = Blueprint('main', __name__, template_folder='templates')


db = connect_to_database()
cur = db.cursor()

@main.route('/')
def main_route():
	cur.execute("SELECT username FROM User")
	usernames = cur.fetchall()
	cur.execute("SELECT albumid, title FROM Album WHERE access = 'public'")
	pub_albums = cur.fetchall()

	if 'username' in session:
		# logged in
		username = session['username']
		# current logged in user
		cur.execute("SELECT firstname, lastname FROM User WHERE username = '" + username + "'")
		user = cur.fetchall()[0]
		if not user:
			return abort(404)
		else:
			cur.execute("SELECT albumid, title FROM Album WHERE access = 'private' AND username = '" + username + "'")
			private_albums = cur.fetchall()
			cur.execute("SELECT A.albumid, A.title FROM Album A, AlbumAccess C WHERE C.username = '" + username +"' AND A.albumid = C.albumid")
			friend_albums = cur.fetchall()
			options = {
				"login": True,
				"user": user,
				"usernames": usernames,
				"pub_albums": pub_albums,
				"priv_albums": private_albums,
				"fri_albums": friend_albums
			}
			return render_template("index.html", **options)

	else:
	    options = {
	    	"login": False,
	    	"usernames": usernames,
	    	"pub_albums": pub_albums
	    }
	    return render_template("index.html", **options)
