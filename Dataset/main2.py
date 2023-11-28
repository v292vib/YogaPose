def accuracy(angle):
    # Step 1: Calculate the absolute difference
    diff = abs(angle - 65)
   
    # Step 2: Convert difference to error percentage
    err = (diff / 65) * 100
   
    # Step 3: Calculate accuracy
    acc = 100 - err
   
    # Step 4: Ensure accuracy is within the range [0, 100]
    acc = max(0, min(int(acc), 100))
   
    return acc

import time
from tkinter import Image
import cv2
import mediapipe as mp
import numpy as np
import pandas as pand
#Sfrom IPython.display import display, clear_output

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

# Curl counter variables
counter = 0
acc=0

data_frame=pand.read_csv('C:\\Users\\Lenovo\\Downloads\\Yogapose.csv')
#print(data_frame)
min1=data_frame.min()
#abx = min1[0]
#print(abx)
max1=data_frame.max()
#print(max1)
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
       
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
     
        # Make detection
        results = pose.process(image)
   
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
   
   
    #calculate angle
   
       
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
           
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
             # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)
           
            rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            #Calculate angle
            angler = calculate_angle(rshoulder, relbow, rwrist)
           
            #  # Get coordinates
            fshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            felbow = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            fwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            # Calculate angle
            fangle = calculate_angle(fshoulder, felbow, fwrist)
           
           
            # Visualize angle
            cv2.putText(image, str(angle),
                           tuple(np.multiply(elbow, [640, 480]).astype(int)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            )
           
            # # Visualize angle
            cv2.putText(image, str(angler),
                            tuple(np.multiply(relbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            )
           
            #  # Visualize angle
            cv2.putText(image, str(fangle),
                            tuple(np.multiply(felbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
             )
           
            acc0 = accuracy(angle)
            acc1=accuracy(angler)
            acc2=accuracy(fangle)
            acc=(acc+acc1+acc2)/3
           
            # Curl counter logic
            if (min[0]< angle <max[0] ) & (min[0]< angler <max[0] ) & (min[2]< fangle <max[2] ):
               
                 # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                                mp_drawing.DrawingSpec(color=(0,255,0), thickness=4, circle_radius=2)
                                 )              
               
                #display(image, display_id="video_frame")
       
                # Clear the previous output in the cell to avoid stacking frames
                #clear_output(wait=True)
       
                cv2.imshow('Mediapipe Feed', image)
                cv2.moveWindow('Mediapipe Feed', 700, 100)
                # while counter:
                #     secs = divmod(counter, 60)
                #     timer = '{:02d}'.format(secs)
                #     print(timer, end="\r")
                #     time.sleep(1)
                #     counter -= 1
               
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
               
            #     stage = "down"
            # if angle < 30 and stage =='down':
            #     stage="up"
                #print(counter)
            print(err)
        except:
            pass
       
        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
       
        # Rep data
        cv2.putText(image, 'Accuracy', (15,12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(int(acc)),
                    (10,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
       
       
       
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,255,255), thickness=2, circle_radius=2),
                                mp_drawing.DrawingSpec(color=(245,255,255), thickness=4, circle_radius=2)
                                 )              
       # display(image, display_id="video_frame")
       
        # Clear the previous output in the cell to avoid stacking frames
       # clear_output(wait=True)
        #cv2.displayOverlay(Image(data=cv2.imencode('.jpg', image)[1]))
        cv2.imshow('Mediapipe Feed', image)
        cv2.moveWindow('Mediapipe Feed', 700, 100)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
       
        # for lndmrk in mp_pose.PoseLandmark:
            # print(lndmrk)
        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
       
       
        def calculate_angle(a,b,c):
            a = np.array(a) # First
            b = np.array(b) # Mid
            c = np.array(c) # End
   
            radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
   
            if angle >180.0:
                angle = 360-angle
       
            return angle

    cap.release()
    cv2.destroyAllWindows()