import update
# import sound
# import os
from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)
cap = cv2.VideoCapture(0)
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def generate_frames():
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

                
                acc0 = update.accuracy(angl,45)
                acc1 = update.accuracy(angler,45)
                acc2 = update.accuracy(fangle,45)
                acc = (acc0+ acc1 + acc2) / 3
                
                # if(angl<30 | angl>50 ):
                #     text = "Correct your right hand"
                #     output_file = sound.text_to_speech(text)
                #     sound.play_sound(output_file)
                #     os.remove(output_file)
                # if(angler<30 | angler>50 ):
                #     text = "Correct your left hand"
                #     output_file = sound.text_to_speech(text)
                #     sound.play_sound(output_file)
                #     os.remove(output_file)
                # if(fangle<40):
                #     text = "Move your leg down"
                #     output_file = sound.text_to_speech(text)
                #     sound.play_sound(output_file)
                #     os.remove(output_file)
                # if(fangle>50):
                #     text = "Move your leg up"
                #     output_file = sound.text_to_speech(text)
                #     sound.play_sound(output_file)
                #     os.remove(output_file)
                
                if (30 < angl < 50) and (30 < angler < 50) and (40 < fangle < 50):
                   
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                                                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=4, circle_radius=2)
                                                )
                    # text = "Well done , Doing good"
                    # output_file = sound.text_to_speech(text)
                    # sound.play_sound(output_file)

                    # # Clean up: remove the generated sound file
                    # os.remove(output_file)
                cv2.putText(frame, f'Accuracy: {acc2}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                
            # Encode the frame as JPEG
            ret, encoded_frame = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Failed to encode frame")
                continue

            # Yield the frame for streaming
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)


//extraaa
 <!--<form method="post" action="{{ url_for('stop_capture') }}">
          <button type="submit">Stop Capture</button>
      </form>-->
