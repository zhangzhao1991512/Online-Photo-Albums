from flask import *
from extensions import connect_to_database
import hashlib
import uuid
import re

# these modules need to check!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


user = Blueprint('user', __name__, template_folder='templates')
db = connect_to_database()
cur = db.cursor()


# Generate secret_key: 
#    import os 
#    os.urandom(24)

@user.route('/user', methods=['GET', 'POST'])
def signup_route():
    if 'username' in session:
        return redirect(url_for('user.edit_account'))
    
    if request.method == 'POST':
        username = request.form['username']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password1']
        confirm_pd = request.form['password2']
        error =[]
        for j in range(0,17):
            error.append({'error': False, 'msg': ''})

        # print(len(error))

        if username == "":
            error[0]['error'] = True
            error[0]['msg'] = "Username may not be left blank"
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
        cur.execute("SELECT * FROM User WHERE username = '" + username + "'")
        user_result = cur.fetchall()
        if user_result:
            error[8]['error'] = True
            error[8]['msg'] = "This username is taken"
        if len(username) < 3:
            error[9]['error'] = True
            error[9]['msg'] = "Usernames must be at least 3 characters long"
        if not re.match('^[A-Za-z0-9_]*$', username):
            error[10]['error'] = True
            error[10]['msg'] = "Usernames may only contain letters, digits, and underscores" 
        if len(password) < 8:
            error[11]['error'] = True
            error[11]['msg'] = "Passwords must be at least 8 characters long"
        if any(char.isdigit() for char in password) == False:
            error[12]['error'] = True
            error[12]['msg'] = "Passwords must contain at least one letter and one number"
        if re.findall('[a-zA-Z]', password) == []:
            error[12]['error'] = True
            error[12]['msg'] = "Passwords must contain at least one letter and one number"
        if not re.match('^[A-Za-z0-9_]*$', password):
            error[13]['error'] = True
            error[13]['msg'] = "Passwords may only contain letters, digits, and underscores"
        if password != confirm_pd:
            error[14]['error'] = True
            error[14]['msg'] = "Passwords do not match"
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error[15]['error'] = True
            error[15]['msg'] = "Email address must be valid"
        if len(email) > 40:
            error[16]['error'] = True
            error[16]['msg'] = "Email must be no longer than 40 characters"

        i = 0
        while (i < 17):
            if (error[i]['error']):
                options = {
                    "errors": error,
                    "input1": username,
                    "input2": firstname,
                    "input3": lastname,
                    "input4": password,
                    "input5": confirm_pd,
                    "input6": email
                }
                return render_template("new_user.html", **options)
            i+=1

        # if no error, update the database and create new user
        algorithm = 'sha512'
        salt = uuid.uuid4().hex
        m = hashlib.new(algorithm)
        m.update(str(salt+password).encode('utf-8'))
        password_hash = m.hexdigest()
        psd = '$'.join([algorithm, salt, password_hash])
        cur.execute("INSERT INTO User VALUES ('" + username + "', '" + firstname + "', '" + lastname + "', '" + psd + "', '" + email + "')")
        return redirect(url_for('user.login_route'))

    else:
        error = [{'error': False, 'msg': ''}]*17
        options={
            "errors": error,
            "input1": "",
            "input2": "",
            "input3": "",
            "input4": "",
            "input5": "",
            "input6": ""
        }
        return render_template("new_user.html", **options)

@user.route('/login', methods=['GET', 'POST'])
def login_route():
    error1 = False
    error2 = False
    error3 = False
    error4 = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == "":
            error1 = True
            # username can't be left blank
            if password == "":
                error2 = True
            # If both the username and the password are blank, 
            # then both "Username may not be left blank" and "Password may not be left blank" should be displayed.

            options = {
            "error1": error1,
            "error2": error2,
            "error3": error3,
            "error4": error4
            }
            return render_template("login.html", **options)
            # If the username is left blank, but any password is entered, 
            # the only error that should be displayed is "Username may not be left blank".
        else:
            
            cur.execute("SELECT password FROM User WHERE username = '" + username + "'")
            p = cur.fetchall()
            

            # if the username doesn't exist in the database, and password is left blank, 
            # then both "Username does not exist" and "Password may not be left blank" should be displayed
            if not p:
                error3 = True
                if password == "":
                    error2 = True
            else:
                # password validation checks are dependent on the username entered being present in the database, unless the password is blank.
                if password == "":
                    error2 = True
                else:
                    p = str(p[0]['password']).split('$')
                    algorithm = p[0]
                    salt = p[1]
                    hashedpswd = p[2]

                    m = hashlib.new(algorithm)
                    m.update(str(salt + password).encode('utf-8'))
                    if m.hexdigest() == hashedpswd:
                        session['username'] = username
                        return redirect(url_for('main.main_route'))
                    else:
                        error4 = True


        options = {
            "error1": error1,
            "error2": error2,
            "error3": error3,
            "error4": error4
        }
        return render_template("login.html", **options)


    #don't need to check session??????????????????????????????????? 
    else:
        options = {
            "error1": error1,
            "error2": error2,
            "error3": error3,
            "error4": error4
        }
        return render_template("login.html", **options)

@user.route('/user/edit', methods=['GET', 'POST'])
def edit_account():

    # edit information one at a time:
    # error1 is for blank and max length check
    # error2 is for email valid or not

    # password can have 4 erors, so error1 -- error4



    if 'username' not in session:
        return redirect(url_for('user.login_route'))
    else:
        # logged in
        username = session['username']
        # current logged in user
        cur.execute("SELECT firstname, lastname FROM User WHERE username = '" + username + "'")
        user = cur.fetchall()[0]
        error1 = False
        error2 = False
        error3 = False
        error4 = False
        msg1 = ""
        msg2 = ""
        msg3 = ""
        msg4 = ""
        if not user:
            return abort(404)
        else:
            if request.method == 'GET':
                options = {
                    "user": user,
                    "error1": False,
                    "error2": False,
                    "error3": False,
                    "error4": False,
                    "msg1": msg1,
                    "msg2": msg2,
                    "msg3": msg3,
                    "msg4": msg4
                }
                return render_template("user_edit.html", **options)
            else:
                if 'firstname' in request.form:
                    if request.form['firstname'] == "":
                        msg1 = "Firstname may not be left blank"
                    else:
                        if len(request.form['firstname']) > 20:
                            msg1 = "Firstname must be no longer than 20 characters"
                        else:
                            cur.execute("UPDATE User SET firstname = '" + request.form['firstname'] + "' WHERE username = '" + username + "'")
                            return redirect(url_for('user.edit_account'))

                if 'lastname' in request.form:
                    if request.form['lastname'] == "":
                        msg1 = "Lastname may not be left blank"
                    else:
                        if len(request.form['lastname']) > 20:
                            msg1 = "Lastname must be no longer than 20 characters"
                        else:
                            cur.execute("UPDATE User SET lastname = '" + request.form['lastname'] + "' WHERE username = '" + username + "'")
                            return redirect(url_for('user.edit_account'))   

                if 'email' in request.form:
                    if request.form['email'] == "":
                        msg1 = "Email may not be left blank"
                        msg2 = "Email address must be valid"
                    else:
                        
                        if not re.match(r"[^@]+@[^@]+\.[^@]+", request.form['email']):
                            msg2 = "Email address must be valid"
                            if len(request.form['email']) > 40:
                                msg1 = "Email must be no longer than 40 characters"
                        elif len(request.form['email']) > 40:
                            msg1 = "Email must be no longer than 40 characters"
                        else:
                            cur.execute("UPDATE User SET email = '" + request.form['email'] +"' WHERE username = '" + username + "'")
                            return redirect(url_for('user.edit_account'))

                if 'password1' in request.form:
                    
                    if len(request.form['password1']) < 8:
                        msg1 = "Passwords must be at least 8 characters long"
                    elif any(char.isdigit() for char in request.form['password1']) == False:
                        msg2 = "Passwords must contain at least one letter and one number"
                    elif re.findall('[a-zA-Z]', request.form['password1']) == []:
                        msg2 = "Passwords must contain at least one letter and one number"
                    elif not re.match('^[A-Za-z0-9_]*$', request.form['password1']):
                        msg3 = "Passwords may only contain letters, digits and underscores"
                    elif request.form['password1'] != request.form['password2']:
                        msg4 = "Passwords do not match"
                    else:
                        algorithm = 'sha512'
                        salt = uuid.uuid4().hex
                        password = request.form['password1']
                        m = hashlib.new(algorithm)
                        m.update(str(salt+password).encode('utf-8'))
                        password_hash = m.hexdigest()
                        psd = '$'.join([algorithm, salt, password_hash])
                        cur.execute("UPDATE User SET password = '" + psd + "' WHERE username = '" + username + "'")
                        return redirect(url_for('user.edit_account'))

                if msg1 != "":
                    error1 = True
                if msg2 != "":
                    error2 = True
                if msg3 != "":
                    error3 = True
                if msg4 != "":
                    error4 = True
                options = {
                    "user": user,
                    "error1": error1,
                    "error2": error2,
                    "error3": error3,
                    "error4": error4,
                    "msg1": msg1,
                    "msg2": msg2,
                    "msg3": msg3,
                    "msg4": msg4
                }
                return render_template("user_edit.html", **options)


# what happens if we use GET /logout ???????????????????????????????????????????????
@user.route('/logout', methods=['GET', 'POST'])
def logout():
        if request.method == 'POST':
            session.clear()
            return redirect(url_for('main.main_route'))
