from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# from flask import Flask, render_template, redirect, url_for, session, flash
# from flask_wtf import FlaskForm
# from wtforms import StringField,PasswordField,SubmitField
# from wtforms.validators import DataRequired, Email, ValidationError
# import bcrypt
# import subprocess
# from flask_mysqldb import MySQL

# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/yoga'
# db=SQLAlchemy(app)
app = Flask(__name__)

app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'yoga'
  
mysql = MySQL(app)





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/beginner')
def beginner():
    return render_template('beginner.html')

@app.route('/tree')
def tree():
    return render_template('tree.html')

@app.route('/advance')
def advance():
    return render_template('advance.html')

@app.route('/login', methods=['GET','POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            # session['full_name'] = user['full_name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('index.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage=mesage)

@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'full_name' in request.form and 'password' in request.form and 'email' in request.form :
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
      
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not full_name or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (full_name, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)

# @app.route('/register',methods=['GET','POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         full_name = form.full_name.data
#         email = form.email.data
#         password = form.password.data

#         hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

#         # store data into database 
#         cursor = mysql.connection.cursor()
#         cursor.execute("INSERT INTO yoga (full_name,email,password) VALUES (%s,%s,%s)",(full_name,email,hashed_password))
#         mysql.connection.commit()
#         cursor.close()

#         return redirect(url_for('login'))

#     return render_template('register.html',form=form)

# @app.route('/login',methods=['GET','POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data

#         cursor = mysql.connection.cursor()
#         cursor.execute("SELECT * FROM yoga WHERE email=%s",(email,))
#         user = cursor.fetchone()
#         cursor.close()
#         if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
#             session['user_id'] = user[0]
#             return redirect(url_for('dashboard'))
#         else:
#             flash("Login failed. Please check your email and password")
#             return redirect(url_for('login'))

#     return render_template('login.html',form=form)

# @app.route('/dashboard')
# def dashboard():
#     if 'user_id' in session:
#         user_id = session['user_id']

#         cursor = mysql.connection.cursor()
#         cursor.execute("SELECT * FROM yoga where id=%s",(user_id,))
#         user = cursor.fetchone()
#         cursor.close()

#         if user:
#             return render_template('index.html',user=user)
            
 


@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        subprocess.run(['python', 'python/main.py'], check=True)
        result = 'Script executed successfully.'
    except subprocess.CalledProcessError:
        result = 'An error occurred while running the script.'
    
    return render_template('tree.html', result=result)

if __name__ == '__main__':
    app.run()