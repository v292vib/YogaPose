# from flask import Flask, render_template, url_for, request, session, redirect, flash
# from flask_pymongo import PyMongo
# import bcrypt
# import subprocess


# # from flask import Flask, render_template, redirect, url_for, session, flash
# # from flask_wtf import FlaskForm
# # from wtforms import StringField,PasswordField,SubmitField
# # from wtforms.validators import DataRequired, Email, ValidationError
# # import bcrypt
# # import subprocess
# # from flask_mysqldb import MySQL

# # app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/yoga'
# # db=SQLAlchemy(app)
# app = Flask(__name__)
# app.secret_key = 'mysecret'
# app.config['MONGO_DBNAME'] = 'db'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/db'

# mongo = PyMongo(app)

# @app.route('/')
# def index():
#     if 'email' and 'password' in session:
#         flash('you are logged in as '+ session['email'], 'info')
#         return render_template('index.html')
#     return render_template('index.html')

# @app.route('/beginner')
# def beginner():
#     return render_template('beginner.html')

# @app.route('/tree')
# def tree():
#     return render_template('tree.html')

# @app.route('/advance')
# def advance():
#     return render_template('advance.html')

# @app.route('/loginpage')
# def loginpage():
#     return render_template('login.html')

# @app.route('/registerpage')
# def registerpage():
#     return render_template('register.html')

# @app.route('/login', methods=['POST','GET'])
# def login():
#     if request.method=='POST':
#         users = mongo.db.get_collection('tab')
#         login_user = users.find_one({'email' : request.form['email']})

#         if login_user and bcrypt.checkpw(request.form['pass'].encode('utf-8'), login_user['password']):
#             session['email'] = request.form['email']
#             flash('Login successful!', 'success')
#             return redirect('index.html')

    
#         flash('Invalid email/password combination', 'error')
#     return render_template('login.html')


# @app.route('/register', methods =['POST' , 'GET'])
# def register():
#     if request.method=='POST':
#         users = mongo.db.get_collection('tab')
    
#     #check for empty form fields 
#         name = request.form.get('name')
#         email = request.form.get('email')
#         password = request.form.get('pass')
    
#         if not email or not password:
#             return render_template('register.html', error='Invalid form data')
    
    
#         existing_user = users.find_one({'email':email})
    
#         if existing_user is None:
#             hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
#             users.insert_one({'name': name,'email': email, 'password': hashpass})
        
#             session['email']=email
#             return redirect(url_for('login'))
#         return render_template('register.html', error='email already exists')
#     return render_template('register.html')


# @app.route('/run_script', methods=['POST'])
# def run_script():
#     try:
#         subprocess.run(['python', 'python/main.py'], check=True)
#         result = 'Script executed successfully.'
#     except subprocess.CalledProcessError:
#         result = 'An error occurred while running the script.'
    
#     return render_template('tree.html', result=result)

# if __name__ == '__main__':
#     app.secret_key = 'mysecret'
#     app.run(debug=True)
    
    
from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
import bcrypt
import subprocess

app = Flask(__name__)
app.secret_key = 'mysecret'
app.config['MONGO_DBNAME'] = 'db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/db'

mongo = PyMongo(app)

@app.route('/' , methods=['POST','GET'])
def index():
    if 'email' and 'password' in session:
        flash('you are logged in as '+ session['email'], 'info')
        return render_template('login.html')

    return render_template('login.html')

@app.route('/main',methods=['POST','GET'])
def main():
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/beginner')
def beginner():
    return render_template('beginner.html')

@app.route('/tree')
def tree():
    return render_template('tree.html')

@app.route('/advance')
def advance():
    return render_template('advance.html')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html')

@app.route('/registerpage')
def registerpage():
    return render_template('register.html')



@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        subprocess.run(['python', 'python/main.py'], check=True)
        result = 'Script executed successfully.'
    except subprocess.CalledProcessError:
        result = 'An error occurred while running the script.'
    
    return render_template('tree.html', result=result)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        users = mongo.db.get_collection('tab')
        login_user = users.find_one({'email' : request.form['email']})

        if login_user and bcrypt.checkpw(request.form['pass'].encode('utf-8'), login_user['password']):
            session['email'] = request.form['email']
            flash('Login successful!', 'success')
            return redirect(url_for('/main'))
            # return render_template('index.html')
    
        flash('Invalid email/password combination', 'error')
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method=='POST':
        users = mongo.db.get_collection('tab')
    
    #check for empty form fields 
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pass')
    
        if not email or not password:
            return render_template('register.html', error='Invalid form data')
    
    
        existing_user = users.find_one({'email':email})
    
        if existing_user is None:
            hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
            users.insert_one({'name': name,'email': email, 'password': hashpass})
        
            session['email']=email
            return redirect(url_for('login'))
        return render_template('register.html', error='email already exists')
    return render_template('register.html')
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)