from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
app.secret_key = 'mysecret'
app.config['MONGO_DBNAME'] = 'db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/db'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'email' and 'password' in session:
        flash('you are logged in as '+ session['email'], 'info')
        return render_template('index.html')

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.get_collection('tab')
    login_user = users.find_one({'email' : request.form['email']})

    if login_user and bcrypt.checkpw(request.form['pass'].encode('utf-8'), login_user['password']):
        session['email'] = request.form['email']
        flash('Login successful!', 'success')
        return redirect(url_for('index'))
    
    flash('Invalid email/password combination', 'error')
    return redirect(url_for('login'))

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
            return redirect(url_for('index'))
        return render_template('register.html', error='email already exists')
    return render_template('register.html')
if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)