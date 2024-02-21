from ast import With
from unittest import result
import cv2 as cv
import numpy as np
import mediapipe as mp

lapis = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
mpHand = mp.solutions.hands
nail_ids = [4, 8, 12, 16, 20]

cap = cv.VideoCapture(1)

with mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    with mpHand.Hands() as hand:
        while cap.isOpened():
            _, frame = cap.read()

            img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img.flags.writeable = False

            res_pose = pose.process(img)
            res_hand = hand.process(img)

            img.flags.writeable = True
            img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

            lapis.draw_landmarks(img, res_pose.pose_landmarks, mpPose.POSE_CONNECTIONS)
            if res_hand.multi_hand_landmarks:
                for handLms in res_hand.multi_hand_landmarks:
                    for id, lm in enumerate (handLms.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        if id in nail_ids:
                            cv.circle(img,(cx,cy),15, (255,0,255),cv.FILLED)
                    lapis.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)

            cv.imshow("CAM", img)

            if cv.waitKey(1) & 0XFF == ord('q'):
                break
    
    cap.release()
    cv.destroyAllWindows()





