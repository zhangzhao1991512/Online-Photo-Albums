from flask import Flask, render_template
import extensions
import controllers
import config

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

# Register the controllers
prefix = "/9x0y8d3y/p2"
app.register_blueprint(controllers.album, url_prefix = prefix)
app.register_blueprint(controllers.albums, url_prefix = prefix)
app.register_blueprint(controllers.pic, url_prefix = prefix)
app.register_blueprint(controllers.main, url_prefix = prefix)
app.register_blueprint(controllers.user, url_prefix = prefix)

app.secret_key = '\xd5\xe9M\xca\x0e\x1d\xed\xdf\xae\x023:[\xc6\xaf\xdbZc\x14\n\xc66\xfc\x1d'
# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
