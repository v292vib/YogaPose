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
    
    
import update

from flask import Flask, render_template, url_for, request, session, redirect, flash ,Response
from flask_pymongo import PyMongo
import bcrypt
import subprocess
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)
app.secret_key = 'mysecret'
app.config['MONGO_DBNAME'] = 'db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/db'

cap = cv2.VideoCapture(0)
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

mongo = PyMongo(app)

def generate_frames(user_email):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            # Convert the frame to RGB for Mediapipe processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame with Mediapipe
            results = holistic.process(rgb_frame)

            # Draw landmarks on the frame
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y,
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z]
                angl = update.calculate_angle(shoulder, elbow, wrist)
                
                rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z]
                relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z]
                rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z]
                angler = update.calculate_angle(rshoulder, relbow, rwrist)

                fshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y,
                            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].z]
                felbow = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y,
                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].z]
                fwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].z]
                fangle = update.calculate_angle(fshoulder, felbow, fwrist)

                acc0 = update.accuracy(int(angl))
                acc1 = update.accuracy(int(angler))
                acc2 = update.accuracy(int(fangle))
                acc = (acc0+ acc1 + acc2) / 3
                
                print(acc)
                
                if user_email:
                    users = mongo.db.get_collection('tab')
                    login_user = users.find_one({'email': user_email})

                    if login_user:
                        accuracies = login_user.get('accuracies', [])

            # Check if 'accuracies' field exists, create it if not
                        if 'accuracies' not in login_user:
                            users.update_one({'email': user_email}, {"$set": {"accuracies": []}})
                            accuracies = []

            # Append the new accuracy
                        accuracies.append(acc)

            # Update the 'accuracies' field in the user document
                        users.update_one({'email': user_email}, {"$set": {"accuracies": accuracies}})
                        
            #
                
                if (40 < angl < 70) and (40 < angler < 70) and (25 < fangle < 80):
                   
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                                                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=4, circle_radius=2)
                                                )
                cv2.putText(frame, f'Accuracy: {acc}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                
            # Encode the frame as JPEG
            ret, encoded_frame = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Failed to encode frame")
                continue

            # Yield the frame for streaming
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame.tobytes() + b'\r\n')
            
            # After generating frames, calculate accuracy
            # accuracy = calculate_accuracy()

             # Store accuracy in MongoDB
            
            




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


@app.route('/video_feed', methods=['POST', 'GET'])
def video_feed():
    user_email = session.get('email')

    # Call the generate_frames function with the user email
    # generate_frames(user_email)
    return Response(generate_frames(user_email), mimetype='multipart/x-mixed-replace; boundary=frame')
        

# @app.route('/run_script', methods=['POST'])
# def run_script():
#     try:
#         subprocess.run(['python', 'python/main.py'], check=True)
#         result = 'Script executed successfully.'
#     except subprocess.CalledProcessError:
#         result = 'An error occurred while running the script.'
    
#     return render_template('tree.html', result=result)

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