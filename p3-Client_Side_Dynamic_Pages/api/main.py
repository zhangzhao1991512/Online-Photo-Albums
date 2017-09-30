from flask import*
import extensions
import hashlib
import uuid

import re

mainAPI = Blueprint('mainAPI', __name__, template_folder='templates')

db = extensions.connect_to_database()

cur = db.cursor()
cur1 = db.cursor()
cur2 = db.cursor()
cur3 = db.cursor()

@mainAPI.route('/api/v1/user', methods=['POST','GET','PUT'])
def API_user_route():
	if request.method == 'GET':
		if 'username' in session:
#			print "Yes"
			username = session['username']
			cur.execute("SELECT username, firstname, lastname, email FROM User WHERE username = %s", [session['username']])
			result = (cur.fetchall())[0]
			response = json.jsonify({"username":result['username'], "firstname":result['firstname'], "lastname":result['lastname'], "email": result['email']})
			response.status_code = 200
			return response
		else:
#			print "wo TM ri le"
			response = json.jsonify({"errors":[{"message":"You do not have the necessary credentials for the resource"}]})
			response.status_code = 401
			return response

	if request.method == 'POST':
		if 'username' in session:
			return redirect(url_for('main.user_edit_route'))
		else:
			try:
				username = request.get_json()['username']
				firstname = request.get_json()['firstname']
				lastname = request.get_json()['lastname']
				password1 = request.get_json()['password1']
				password2 = request.get_json()['password2']
				email = request.get_json()['email']
			except KeyError:
				response = json.jsonify(errors=[{"message": "You did not provide the necessary fields"}])
				response.status_code = 422
            			return response
			#print "cao ni ma"

			error = []
			check_error = False
#			error = [{'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}, {'error':False, 'msg':''}]
#			if username == "":
#				error[0]['error'] = True
#				error[0]['msg'] = "Username may not be left blank"
#			if firstname == "":
#				error[1]['error'] = True
#				error[1]['msg'] = "Firstname may not be left blank"
#			if lastname == "":
#				error[2]['error'] = True
#				error[2]['msg'] = "Lastname may not be left blank"
#			if password == "":
#				error[3]['error'] = True
#				error[3]['msg'] = "Password may not be left blank"
#			if email == "":
#				error[4]['error'] = True
#				error[4]['msg'] = "Email may not be left blank"
			if len(username) > 20:
				error.append({"message":"Username must be no longer than 20 characters"})
				check_error = True
#				error[5]['error'] = True
#				error[5]['msg'] = "Username must be no longer than 20 characters"
			if len(firstname) > 20:
				check_error = True
				error.append({"message":"Firstname must be no longer than 20 characters"})
#				error[6]['error'] = True
#				error[6]['msg'] = "Firstname must be no longer than 20 characters"
			if len(lastname) > 20:
				check_error = True
				error.append({"message":"Lastname must be no longer than 20 characters"})
#				error[7]['error'] = True
#				error[7]['msg'] = "Lastname must be no longer than 20 characters"
			cur3.execute("SELECT username FROM Album WHERE username = %s", [username])
			check_user = cur3.fetchall()
			if check_user:
				print "????????????????"
				check_error = True
				error.append({"message":"This username is taken"})
#				error[8]['error'] = True
#				error[8]['msg'] = "This username is taken"
			if len(username) < 3:
				check_error = True
				error.append({"message":"Usernames must be at least 3 characters long"})
#				error[9]['error'] = True
#				error[9]['msg'] = "Usernames must be at least 3 characters long"
			if not re.match("^[A-Za-z0-9_]*$", username):
				check_error = True
				error.append({"message":"Usernames may only contain letters, digits, and underscores"})
#				error[10]['error'] = True
#				error[10]['msg'] = "Usernames may only contain letters, digits, and underscores"
			if len(password1) < 8:
				check_error = True
				error.append({"message":"Passwords must be at least 8 characters long"})
#				error[11]['error'] = True
#				error[11]['msg'] = "Passwords must be at least 8 characters long"
			if hasNumbers(password1) == False or re.findall('[a-zA-Z]', password1) == []:
				check_error = True
				error.append({"message":"Passwords must contain at least one letter and one number"})
#				error[12]['error'] = True
#				error[12]['msg'] = "Passwords must contain at least one letter and one number"
#			if re.findall('[a-zA-Z]', request.form['password1']) == []:
#				error[12]['error'] = True
#				error[12]['msg'] = "Passwords must contain at least one letter and one number"
			if not re.match("^[A-Za-z0-9_]*$", password1):
				check_error = True
				error.append({"message":"Passwords may only contain letters, digits, and underscores"})
#				error[13]['error'] = True
#				error[13]['msg'] = "Passwords may only contain letters, digits, and underscores"
			if password1 != password2:
				check_error = True
				error.append({"message":"Passwords do not match"})
#				error[14]['error'] = True
#				error[14]['msg'] = "Passwords do not match"
			if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
				check_error = True
				error.append({"message":"Email address must be valid"})
#				error[15]['error'] = True
#				error[15]['msg'] = "Email address must be valid"
			if len(email) > 40:
				check_error = True
				error.append({"message":"Email must be no longer than 40 characters"})
#				error[16]['error'] = True
#				error[16]['msg'] = "Email must be no longer than 40 characters"

#			j = 0
#			while (j < 17):
#				if(error[j]['error']):
#					response = json.jsonify({})
#					response.status_code = 422
#					return response
#				j = j+1
			if check_error:
				#print "ri le gou le"
				tmp = {}
				tmp["errors"] = error
				response = json.jsonify(tmp)
				response.status_code = 422
				return response

		#------------After all the check, it is valid----------------#
		#---Then add the user and redirect it to the /login page-----#
			#print "here i am"
			algorithm = 'sha512'
			salt = uuid.uuid4().hex
			m = hashlib.new(algorithm)
			m.update(salt + password1)
			hash_password = m.hexdigest()
			store_password = algorithm + '$' + salt + '$' + hash_password
                #This command create a new user in MySQL
			cur3.execute("INSERT INTO User Values ('" + username + "', '" + firstname + "', '" + lastname + "', '" + store_password + "', '" + email + "')")

#			return redirect(url_for('main.login_route'))
			response = json.jsonify({"username": username, "firstname":firstname, "lastname":lastname, "password1": password1, "password2": password2, "email": email})
			response.status_code = 201
			return response

	if request.method == 'PUT':
		if 'username' in session:
			try:
				username = request.get_json()['username']
				firstname = request.get_json()['firstname']
				lastname = request.get_json()['lastname']
				password1 = request.get_json()['password1']
				password2 = request.get_json()['password2']
				email = request.get_json()['email']
			except KeyError:
				response = json.jsonify(errors=[{"message": "You did not provide the necessary fields"}])
				response.status_code = 422
				return response
			
			if username == "":
				response = json.jsonify({"errors":[{"message":"The requested resource could not be found"}]})
				response.status_code = 404
				return response

			if session['username'] != username:
				response = json.jsonify({"errors":[{"message":"You do not have the necessary permissions for the resource"}]})
				response.status_code = 403
				return response

			cur2.execute("SELECT username, firstname, lastname, email FROM User WHERE username=%s", [session['username']])
			u = (cur2.fetchall())[0]['username']
			f = (cur2.fetchall())[0]['firstname']
			l = (cur2.fetchall())[0]['lastname']
			e = (cur2.fetchall())[0]['email']
			
#			return "wo hai mei xie gai user ne"
			error = []
			if password1 != "" or password2 != "":
				if len(password1) < 8:
					error.append({"message":"Passwords must be at least 8 characters long"})
				if hasNumbers(password1) == False or re.findall('[a-zA-Z]', password1) == []:
					error.append({"message":"Passwords must contain at least one letter and one number"})
            			if not re.match("^[A-Za-z0-9_]*$", password1):
					error.append({"message":"Passwords may only contain letters, digits, and underscores"})
				if password1 != password2:
					error.append({"message":"Passwords do not match"})
			if e != email:
				if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
					error.append({"message":"Email address must be valid"})				
				if len(email) > 40:
					error.append({"message":"Email must be no longer than 40 characters"})					
			if len(firstname) > 20:
				error.append({"message":"Firstname must be no longer than 20 characters"})
			if len(lastname) > 20:
				error.append({"message":"Lastname must be no longer than 20 characters"})
			
			#---chech whether there is any error---
			if error != []:
				tmp = {}
				tmp["errors"] = error
				response = json.jsonify(tmp)
				response.status_code = 422
				return response
			else: #means there is no error
				if password1 != "":
					algorithm = 'sha512'
					salt = uuid.uuid4().hex
					m = hashlib.new(algorithm)
					m.update(salt + password1)
					hash_password = m.hexdigest()
					p = algorithm + '$' + salt + '$' + hash_password
					cur2.execute("UPDATE User SET password = %s where username = %s", [p, session['username']])
				if f != firstname:
					cur2.execute("UPDATE User SET firstname = %s where username = %s", [firstname, session['username']])
				if l != lastname:
					cur2.execute("UPDATE User SET lastname = %s where username = %s", [lastname, session['username']])
				if e != email:
					cur2.execute("UPDATE User SET email = %s where username = %s", [email, session['username']])
				response = json.jsonify({"username": username, "firstname":firstname, "lastname":lastname, "password1": password1, "password2": password2, "email": email})
				response.status_code = 201
				return response

		else:
			response = json.jsonify({"errors":[{"message":"You do not have the necessary credentials for the resource"}]})
			response.status_code = 401
			return response

@mainAPI.route('/api/v1/login', methods=['POST'])
def API_login_route():
	if 'username' in session:
		return redirect(url_for('/user/edit'))

	if request.method == 'POST':
#-------------------------------------Check if there is an error-----------------------------
		try:
			username = request.get_json()['username']
			password = request.get_json()['password']
		except KeyError:
			response = json.jsonify(errors=[{"message": "You did not provide the necessary fields"}])
			response.status_code = 422
			return response
		response = jsonify({"username":username, "password":password})

		error1 = False
		error2 = False
		error3 = False
		error4 = False
		if username == "":
			error1 = True
		else:
			cur1.execute("SELECT password FROM User WHERE username = '" + username + "'")
			r = cur1.fetchall()
			if not r:
				error3 = True
			else:
				if password =="":
					error2 = True
				else:
					pswd = str(r[0]['password']).split('$')
					algorithm = pswd[0]
					salt = pswd[1]
					hashpswd = pswd[2]
					m = hashlib.new(algorithm)
					m.update(salt + password)
					if m.hexdigest() == hashpswd:
						session['username'] = username
						response.status_code = 200
						response = jsonify({"username":username})
						return response
#						return redirect(url_for('main.main_route'))
					else:
						error4 = True

		if error3 or error1:
			response = json.jsonify(errors=[{"message": "Username does not exist"}])
			response.status_code = 404
			return response
		if error4 or error2:
			response = json.jsonify(errors=[{"message": "Password is incorrect for the specified username"}])
			response.status_code = 422
			return response

		return "something wrong"

@mainAPI.route('/api/v1/logout', methods=['POST'])
def API_logout_route():
	if 'username' in session:
		session.clear()
		response = json.jsonify()
		response.status_code = 204
	# --cannot logout since not login--
	else:
		response = json.jsonify(errors=[{"message": "You do not have the necessary credentials for the resource"}])
		response.status_code = 401
	return response


def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)
