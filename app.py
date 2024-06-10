# app.py

from flask import Flask, session, render_template
from login import login_bp
from db_config import DATABASE_CONFIG
from cartridge import cartridge_bp
import mysql.connector

app = Flask(__name__)
app.secret_key = '$%#E$$%^$###SSWW'

# Configure the MySQL database connection
db = mysql.connector.connect(**DATABASE_CONFIG)

# Register the login blueprint
app.register_blueprint(login_bp)


# Register the cartridge blueprint
app.register_blueprint(cartridge_bp)



@app.route('/')
def index():
    if 'username' in session and session['username'] is not None:
        return render_template('index.html')
    return redirect(url_for('login.login'))



if __name__ == '__main__':
    app.run(debug=True)
