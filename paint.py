import cv2
import mediapipe as mp
import time
from collections import deque


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


pointx = []
pointy = []
cap = cv2.VideoCapture(0)

rpoints = [deque(maxlen=512)]

def paint(frame,rpoints):
    points = [rpoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], (100, 0, 255), 2)

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        
        success, frame = cap.read()
        imgResult = frame.copy()
        start = time.time()
   
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

        frame.flags.writeable = False

        results = hands.process(frame)

        frame.flags.writeable = True

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)


        if results.multi_hand_landmarks:
          for hand_landmarks in results.multi_hand_landmarks:

            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            x = int(hand_landmarks.landmark[8].x*640)
            y= int(hand_landmarks.landmark[8].y*480)


     
            rpoints[0].append((x, y))
            cv2.circle(frame, (x, y), 3, (250, 250, 0), 6)
            
            
            


        paint(frame,rpoints)
        end = time.time()
        totalTime = end - start
      
        fps = 1 / totalTime
        

        cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)

        cv2.imshow('Hand Painting', frame)


        if cv2.waitKey(5) & 0xFF == 27:
          break

cap.release()