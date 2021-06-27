import random

from flask import Flask, render_template, redirect, request, url_for
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'maheshvp'
app.config['MYSQL_DATABASE_DB'] = 'flaskdemo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.after_request
def add_header(r):
    """
   Add headers to both force latest IE rendering engine or Chrome Frame,
   and also to cache the rendered page for 10 minutes.
   """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/loginError/<val>')
def login_error(val):
    return render_template('login.html', loginFailed=True, error=val)


@app.route('/login', methods=["POST"])
def validate_login():
    email = request.form["email-address"]
    password = request.form["password"]
    cursor = mysql.get_db().cursor()
    cursor.execute('select * from users where email = %s ;', (email))
    user = cursor.fetchone()
    if not user:
        print("User not found")
        return redirect(url_for('login_error', val="User not found"))
    if user[3] != password:
        print("Password not matching")
        return redirect(url_for('login_error', val="Password not matching"))
    cursor.execute('select * from users;')
    users = cursor.fetchall()
    return render_template('dashboard.html', users=users, selectedUserName=user[1])


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=["POST"])
def add_user():
    name =  request.form["name"],
    email = request.form["email-address"],
    phoneNo = request.form["phoneNo"],
    password = request.form["password"],
    number = random.randint(0, 500)
    cursor = mysql.get_db().cursor()
    cursor.execute('insert into users values(%s, %s, %s, %s, %s);', (email, name, phoneNo, password, number))
    mysql.get_db().commit()
    return render_template('login.html', addedUser=True)


if __name__ == '__main__':
    app.run()
