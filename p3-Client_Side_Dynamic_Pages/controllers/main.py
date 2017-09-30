from flask import*
import extensions
import hashlib
import uuid

import re

main = Blueprint('main', __name__, template_folder='templates')

db = extensions.connect_to_database()

cur = db.cursor()
cur1 = db.cursor()
cur2 = db.cursor()
cur3 = db.cursor()
cur4 = db.cursor()

@main.route('/')
def main_route():
#	return session['username']
#	if 'sportslover' == session['username']:
	cur.execute("SELECT username FROM User")
	result = cur.fetchall()
	if 'username' in session:
		cur.execute("SELECT COUNT(username) FROM User")
		res = cur.fetchall()
		n = int(res[0]['COUNT(username)'])
		i = 0
		while(i < n):
			u = str(result[i]['username'])
			if u == session['username']:
				##This means: this user is logged in!!!
				cur2.execute("SELECT username, firstname, lastname From User WHERE username = '" + u + "'")
				res = (cur2.fetchall())[0]
				cur2.execute("SELECT albumid, title FROM Album WHERE access = 'public' UNION SELECT albumid, title FROM Album WHERE username = '" + u + "'" + " UNION SELECT A.albumid, A.title FROM Album A, AlbumAccess C WHERE A.albumid = C.albumid AND C.username = '" + u + "'")
				res_albums = cur2.fetchall()
				options = {
                	       		"keyin": True,
					"login": True,
               		        	"thisuser": res,
					"albums": res_albums
	        	        }
				return render_template("index.html", **options)
			i=i+1
	else:
		cur.execute("SELECT albumid, title FROM Album WHERE access = 'public'")
		results = cur.fetchall()
		options = {
			"usernames": result,
			"albumids": results,
			"keyin": False,
			"login": False
		}
		return render_template("index.html", **options)

@main.route('/login', methods=['GET','POST'])
def login_route():
#	if request.method == 'POST':
#		#-------------------------------------Check if there is an error-----------------------------
#		username = request.form['username']
#		password = request.form['password']
#		error1 = False
#		error2 = False
#		error3 = False
#		error4 = False
#		if username == "":
#			error1 = True
#		else:
#			cur1.execute("SELECT password FROM User WHERE username = '" + request.form['username'] + "'")
#               	r = cur1.fetchall()
#                	if not r:	
#				error3 = True
#			else:		
#				if password =="":
#					error2 = True
#				else:	
#					pswd = str(r[0]['password']).split('$')
#					algorithm = pswd[0]
#					salt = pswd[1]
#					hashpswd = pswd[2]
#					m = hashlib.new(algorithm)
#					m.update(salt + request.form['password'])
#					if m.hexdigest() == hashpswd:
#						session['username'] = request.form['username']
#						return redirect(url_for('main.main_route'))
#					else:
#						error4 = True
#		options = {
#			"error1": error1,
#			"error2": error2,
#			"error3": error3,
#			"error4": error4,
#			"login": False,
#			"keyin": True,
#			"newuser": False
#		}
#		return render_template("index.html", **options)	
#	else:
	options = {
		"error1": False,
		"error2": False,
		"error3": False,
		"error4": False,
		"login": False,
		"keyin": True,
		"newuser": False
        }
        return render_template("index.html", **options)


@main.route('/logout', methods=['GET','POST'])
def logout_route():
    ###############remove the username from the session if it's there
	#session.pop('username', None)
	if request.method == 'POST':
		session.clear()
#	session['username'] = 'null'
		return redirect(url_for('main.main_route'))

@main.route('/user', methods=['GET','POST'])
def user_route():
	if 'username' in session:
		return redirect(url_for('main.user_edit_route'))
#	cur3.execute("SELECT username FROM User")
#	result = cur3.fetchall()
#	cur3.execute("SELECT COUNT(username) FROM User")
#	res = cur3.fetchall()
#	n = int(res[0]['COUNT(username)'])
#	i = 0
#	while(i < n):
#		u = str(result[i]['username'])
#		if u == session['username']:
#			return redirect(url_for('main.user_edit_route'))
#		i = i + 1
	
	#There is no session...#
	if request.method == 'POST':
#		cur3.execute("SELECT username FROM User")
#        	result = cur3.fetchall()
#        	cur3.execute("SELECT COUNT(username) FROM User")
#        	res = cur3.fetchall()
#        	n = int(res[0]['COUNT(username)'])
#        	i = 0
#        	while(i < n):
#                	u = str(result[i]['username'])
#                	if u == session['username']:
#				cur3.execute("SELECT username, firstname, lastname From User WHERE username = '" + u + "'")
#				res = (cur3.fetchall())[0]
#				options = {
#					##Keyin is False, then it is in the user_edit mode
#					"keyin": False,
#					"login": True,
#					"thisuser": res
#                        	}
#				return render_template("index.html", **options)
#			return redirect(url_for('main.user_edit_route', ))
#	                i=i+1

		username = request.form['username']
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		email = request.form['email']
		password = request.form['password1']
		r_password = request.form['password2']
		#HERE WE NEED TO DO THE PART 3 ----> Check whether it is valid#
		#Error = {'error':False, 'msg':''}
		#error = [Error] * 17
		error = [{'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}]
		if username == "":
			error[0]['error'] = True
			error[0]['msg'] = "Username may not be left blank"
#			return str(error[16]['msg'])
		if firstname == "":
			error[1]['error'] = True
			error[1]['msg'] = "Firstname may not be left blank"
		if lastname == "":
			error[2]['error'] = True
			error[2]['msg'] = "Lastname may not be left blank"
		if password == "":
                        error[3]['error'] = True
                        error[3]['msg'] = "Password may not be left blank"
		if email == "":
                        error[4]['error'] = True
                        error[4]['msg'] = "Email may not be left blank"
		if len(username) > 20:
			error[5]['error'] = True
			error[5]['msg'] = "Username must be no longer than 20 characters"
		if len(firstname) > 20:
			error[6]['error'] = True
			error[6]['msg'] = "Firstname must be no longer than 20 characters"
		if len(lastname) > 20:
			error[7]['error'] = True
			error[7]['msg'] = "Lastname must be no longer than 20 characters"
		cur3.execute("SELECT username FROM Album WHERE username = %s", [username])
		check_user = cur3.fetchall()
		if check_user:
			error[8]['error'] = True
			error[8]['msg'] = "This username is taken"
		if len(username) < 3:
			error[9]['error'] = True
			error[9]['msg'] = "Usernames must be at least 3 characters long"
		if not re.match("^[A-Za-z0-9_]*$", username):
			error[10]['error'] = True
			error[10]['msg'] = "Usernames may only contain letters, digits, and underscores"
		if len(password) < 8:
			error[11]['error'] = True
			error[11]['msg'] = "Passwords must be at least 8 characters long"
		if hasNumbers(password) == False:
			error[12]['error'] = True
			error[12]['msg'] = "Passwords must contain at least one letter and one number"
		if re.findall('[a-zA-Z]', request.form['password1']) == []:
			error[12]['error'] = True
			error[12]['msg'] = "Passwords must contain at least one letter and one number"
		if not re.match("^[A-Za-z0-9_]*$", password):
                        error[13]['error'] = True
                        error[13]['msg'] = "Passwords may only contain letters, digits, and underscores"
		if password != r_password:
			error[14]['error'] = True
                        error[14]['msg'] = "Passwords do not match"
		if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
			error[15]['error'] = True
                        error[15]['msg'] = "Email address must be valid"
		if len(email) > 40:
			error[16]['error'] = True
                        error[16]['msg'] = "Email must be no longer than 40 characters"
		j = 0
		while (j < 17):
			print error[j]['msg']
			j = j+1
		j = 0
		while (j < 17):
			if(error[j]['error']):
				options = {
					"login": False,
					"keyin": True,
					"newuser": True,
					"edit": False,
					"errors": error,
					"input1": username,
					"input2": firstname,
					"input3": lastname,
					"input4": email,
					"input5": password,
					"input6": r_password
				}
				return render_template("index.html", **options)
			j = j+1

		#------------After all the check, it is valid----------------#
		#---Then add the user and redirect it to the /login page-----#
		algorithm = 'sha512'
		salt = uuid.uuid4().hex
		m = hashlib.new(algorithm)
		m.update(salt + password)
		hash_password = m.hexdigest()
		store_password = algorithm + '$' + salt + '$' + hash_password
		#This command create a new user in MySQL
		cur3.execute("INSERT INTO User Values ('" + username + "', '" + firstname + "', '" + lastname + "', '" + store_password + "', '" + email + "')")
		return redirect(url_for('main.login_route'))
	else:
		error = [{'error': False, 'msg':''}] * 17
		options = {
			"login": False,
			"keyin": True,
			"newuser": True,
			"edit": False,
			"errors": error,
			"input1": '',
			"input2": '',
			"input3": '',
			"input4": '',
			"input5": '',
			"input6": ''
        	}
        	return render_template("index.html", **options)

@main.route('/user/edit', methods=['GET','POST'])
def user_edit_route():
	if 'username' not in session:
		return redirect(url_for('main.login_route'))

	#First need to check whether have the user session#
	cur4.execute("SELECT username FROM User")
        result = cur4.fetchall()
        cur4.execute("SELECT COUNT(username) FROM User")
        res = cur4.fetchall()
        n = int(res[0]['COUNT(username)'])
        i = 0
	no_session = True
        while(i < n):
                u = str(result[i]['username'])
                if u == session['username']:
                	no_session = False
		i = i + 1

	msg = ""
	msg2 = ""
	msg3 = ""
	msg4 = ""
	error1 = False
	error2 = False
	error3 = False
	error4 = False
	
	if(no_session):
		return abort(403)
#		return "hahahahahahahah"
	else:
		if request.method == 'POST':
			if 'firstname' in request.form:
				if request.form['firstname'] == "":
					msg = "Firstname may not be left blank"
				else:
					if len(request.form['firstname']) > 20:
						msg = "Firstname must be no longer than 20 characters"
					else:
						cur4.execute("UPDATE User SET firstname = '" + request.form['firstname'] + "' WHERE username = '" + session['username'] + "'")
						return redirect(url_for('main.user_edit_route'))
			if 'lastname' in request.form:
				if request.form['lastname'] == "":
					msg = "Lastname may not be left blank"
				else:
					if len(request.form['lastname']) > 20:
						msg = "Lastname must be no longer than 20 characters"
					else:
                        	        	cur4.execute("UPDATE User SET lastname = '" + request.form['lastname'] + "' WHERE username = '" + session['username'] + "'")
						return redirect(url_for('main.user_edit_route'))
			if 'email' in request.form:
				if request.form['email'] == "":
					msg = "Email may not be left blank"
					msg2 = "Email address must be valid"
				else:
					if not re.match(r"[^@]+@[^@]+\.[^@]+", request.form['email']):
						msg = "Email address must be valid"
						if len(request.form['email']) > 40:
							msg2 = "Email must be no longer than 40 characters"
					else:
						if len(request.form['email']) > 40:
							msg = "Email must be no longer than 40 characters"

					if not re.match(r"[^@]+@[^@]+\.[^@]+", request.form['email']):
						print "no"
					elif len(request.form['email']) > 40:
						print "nonono"
					else:
						cur4.execute("UPDATE User SET email = '" + request.form['email'] + "' WHERE username = '" + session['username'] + "'")
						return redirect(url_for('main.user_edit_route'))
			if 'password1' in request.form:
				#--------------HAHA, Here we need to check whether the password valid or not---------------#
				if len(request.form['password1']) < 8:
					msg = "Passwords must be at least 8 characters long"
				if hasNumbers(request.form['password1']) == False:
					msg2 = "Passwords must contain at least one letter and one number"
				if re.findall('[a-zA-Z]', request.form['password1']) == []:
					msg2 = "Passwords must contain at least one letter and one number"
				if not re.match("^[A-Za-z0-9_]*$", request.form['password1']):
					msg3 = "Passwords may only contain letters, digits, and underscores"
				if request.form['password1'] != request.form['password2']:
					msg4 = "Passwords do not match"

				if len(request.form['password1']) < 8:
					print "oh no"
				elif hasNumbers(request.form['password1']) == False:
					print "oh nono"
				elif re.search('[a-zA-Z]', request.form['password1']) == False:
					print "oh nono"
				elif not re.match("^[A-Za-z0-9_]*$", request.form['password1']):
					print "oh nonono"
				elif request.form['password1'] != request.form['password2']:
					print "oh nononono"
				else:
				#----------------------------------Okay, it is valid---------------------------------------#
					algorithm = 'sha512'
					salt = uuid.uuid4().hex
					m = hashlib.new(algorithm)
					password = request.form['password1']
					m.update(salt + password)
					hashed = m.hexdigest()
					hash_password = algorithm + '$' + salt + '$' + hashed
					cur4.execute("UPDATE User SET password = '" + hash_password + "' WHERE username = '" + session['username'] + "'")
					return redirect(url_for('main.user_edit_route'))
			
			cur4.execute("SELECT username, firstname, lastname, email From User WHERE username = '" + session['username'] + "'")
			thisuser = (cur4.fetchall())[0]

			if msg != "":
				error1 = True
			if msg2 != "":
                                error2 = True
			if msg3 != "":
                                error3 = True
			if msg4 != "":
                                error4 = True
			options = {
				"login": True,
				"error1": error1,
				"error2": error2,
				"error3": error3,
				"error4": error4,
				"msg": msg,
				"msg2": msg2,
				"msg3": msg3,
				"msg4": msg4,
				"keyin": False,
				"thisuser": thisuser
			}
			return render_template("index.html", **options)

		else:
			cur4.execute("SELECT username, firstname, lastname, email From User WHERE username = '" + session['username'] + "'")
			thisuser = (cur4.fetchall())[0]
			options = {
				"login": True,
				"error1": False,
				"error2": False,
				"error3": False,
				"error4": False,
				"msg": msg,
				"msg2": msg2,
				"msg3": msg3,
				"msg4": msg4,
				"keyin": False,
				"thisuser": thisuser
			}
			return render_template("index.html", **options)

def hasNumbers(inputString):
     return any(char.isdigit() for char in inputString)

