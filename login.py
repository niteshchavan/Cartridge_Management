# login.py

from flask import Blueprint, render_template, request, redirect, url_for, session
from db_config import DATABASE_CONFIG
import mysql.connector
import bcrypt

login_bp = Blueprint('login', __name__)
db = mysql.connector.connect(**DATABASE_CONFIG)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE users = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['username'] = user['users']
            return redirect(url_for('index'))  # Redirect to index page upon successful login
        else:
            error = 'Invalid Credentials. Please try again.'
    
    return render_template('login.html', error=error)


@login_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login.login'))