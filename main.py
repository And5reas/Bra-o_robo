import cv2 as cv
import mediapipe as mp
import serial
import math

lapis = mp.solutions.drawing_utils
mpHand = mp.solutions.hands
nail_ids = [0, 4, 8, 12, 16, 20]
ser = serial.Serial('COM3', 9600)

def cal_dist_euclid(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

cap = cv.VideoCapture(1)
with mpHand.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5) as hand:
    while cap.isOpened():
        _, frame = cap.read()

        img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img.flags.writeable = False

        res_hand = hand.process(img)

        img.flags.writeable = True
        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

        if res_hand.multi_hand_landmarks:
            for handLms in res_hand.multi_hand_landmarks:

                polegar = (handLms.landmark[4].x, handLms.landmark[4].y)
                indicador = (handLms.landmark[8].x, handLms.landmark[8].y)

                close_hand = True if (cal_dist_euclid(polegar, indicador) < 0.2) else False

                for id, lm in enumerate (handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    if id in nail_ids:
                        if (id == 4):
                            cv.circle(img, (cx,cy), 15, (0, 255, 255),cv.FILLED)
                        elif (id == 0):
                            if (not close_hand):
                                if (cx > w/2 + 50):
                                    ser.write("1h".encode())
                                elif (cx < w/2 - 50):
                                    ser.write("2h".encode())
                                else:
                                    ser.write("SS".encode())
                            else:
                                ser.write("SS".encode())

                            cv.circle(img,(cx,cy),15, (255, 255, 0),cv.FILLED)
                        else:
                            cv.circle(img,(cx,cy),15, (255, 0, 255),cv.FILLED)
                lapis.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
        else:
            ser.write("SS".encode())

        cv.imshow("CAM", img)

        if cv.waitKey(1) & 0XFF == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()





