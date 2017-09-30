from flask import *

from extensions import connect_to_database

main = Blueprint('main', __name__, template_folder='templates')


db = connect_to_database()
cur = db.cursor()

@main.route('/')
def main_route():
    cur.execute("SELECT username FROM User")
    result = cur.fetchall()
    options = {
    	"usernames": result
    }
    return render_template("index.html", **options)


# @main.route('/hello')
# def main_hello():
#     return "Hello everyone!"




# @main.route('/hello')
# def main_hello():
#     db = connect_to_database()
#     cur = db.cursor()
#     cur.execute('SELECT id, name FROM test_tbl')
#     results = cur.fetchall()
#     print(results)
#     print_str = "<table>"
#     for result in results:
#         print_str += "<tr><td>%s</td><td>%s</td><tr>" % (result['id'], result['name'])
#     print_str += "</table>"
#     return print_str
