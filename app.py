from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

data = {}


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
   if email not in data:
       print("User not found")
       return redirect(url_for('login_error', val="User not found"))
   if data[email]["password"] != password:
       print("Password not matching")
       return redirect(url_for('login_error', val="Password not matching"))
   return render_template('dashboard.html', users=data.values(), selectedUser=data[email])


@app.route('/register')
def register():
   return render_template('register.html')


@app.route('/register', methods=["POST"])
def add_user():
   user = {'name': request.form["name"],
           'email': request.form["email-address"],
           'phoneNo': request.form["phoneNo"],
           'password': request.form["password"]}
   data[user["email"]] = user
   return render_template('login.html', addedUser=True)


if __name__ == '__main__':
   app.run()

