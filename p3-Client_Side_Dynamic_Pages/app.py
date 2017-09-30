from flask import Flask, render_template, jsonify
#import extensions
import config
import controllers
import api

#from extensions import db

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

# ps
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'proj1'
# mysql.init_app(app)


# Register the controllers
prefix = "/m18kcsvh/p3"
app.register_blueprint(controllers.album, url_prefix = prefix)
app.register_blueprint(controllers.albums, url_prefix = prefix)
app.register_blueprint(controllers.pic, url_prefix = prefix)
app.register_blueprint(controllers.main, url_prefix = prefix)

# Register for the APIs
app.register_blueprint(api.mainAPI, url_prefix=prefix)
app.register_blueprint(api.albumAPI, url_prefix=prefix)
app.register_blueprint(api.picAPI, url_prefix=prefix)


################ The Secret Key###############
app.secret_key = "ahahahasecretkey"

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host='0.0.0.0', port=3000, debug=True)
