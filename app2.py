import numpy as np
from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
from keras.models import load_model
import update

from camera_module import cap
# from app import cap
app = Flask(__name__)


mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def inFrame(lst):
    if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility > 0.6 and lst[16].visibility > 0.6:
        return True
    return False

model = load_model("C:\\Users\\hp\\OneDrive\\Desktop\\myenv\\model.h5")
label = np.load("C:\\Users\\hp\\OneDrive\\Desktop\\myenv\\labels.npy")



def generate_frames1():
    while True:
        lst = []

        _, frm = cap.read()

        frm = cv2.flip(frm, 1)

        res = holistic.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

        frm = cv2.blur(frm, (4, 4))
        if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
            for i in res.pose_landmarks.landmark:
                lst.append(i.x - res.pose_landmarks.landmark[0].x)
                lst.append(i.y - res.pose_landmarks.landmark[0].y)

            lst_array = np.array(lst).reshape(1, -1)
            lst_reshaped = lst_array.reshape((lst_array.shape[0], 1, lst_array.shape[1]))

            # Predict using the reshaped input
            p = model.predict(lst_reshaped)
            pred = label[np.argmax(p)]
            
            if p[0][np.argmax(p)] > 0.75:
                cv2.putText(frm, pred, (180, 180), cv2.FONT_ITALIC, 1.3, (0, 255, 0), 2)
                if pred=="Vrikshasana":
                    if res.pose_landmarks:
                        landmarks = res.pose_landmarks.landmark
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
                        # print(acc2)
                        cv2.putText(frm, f'Accuracy: {acc2}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                # Rest of your code for drawing landmarks and calculating angles
            else:
                cv2.putText(frm, "Asana is either wrong or not trained", (100, 180), cv2.FONT_ITALIC, 1.8, (0, 0, 255), 3)
        else:
            cv2.putText(frm, "Make Sure Full body is visible", (100, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

        # Drawing landmarks
        mp_drawing.draw_landmarks(frm, res.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=6),
                                  connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), circle_radius=3, thickness=3))

        ret, encoded_frame = cv2.imencode('.jpg', frm)
        if not ret:
            print("Error: Failed to encode frame")
            continue

        # Yield the frame for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame.tobytes() + b'\r\n')

@app.route('/video_feed', methods=['POST', 'GET'])
def video_feed():
    return Response(generate_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
