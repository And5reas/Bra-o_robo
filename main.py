import cv2 as cv
import mediapipe as mp
import serial
import math

lapis = mp.solutions.drawing_utils
mpHand = mp.solutions.hands
nail_ids = [0, 4, 8, 12, 16, 20]
ser = serial.Serial('COM3', 9600)

def cal_dist_euclid(p1, p2):
    return True if math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) < 0.2 else False

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

                h, w, c = img.shape

                pulso = (handLms.landmark[0].x, handLms.landmark[0].y)
                polegar = (handLms.landmark[4].x, handLms.landmark[4].y)
                indicador = (handLms.landmark[8].x, handLms.landmark[8].y)

                cv.circle(img, (int(pulso[0]*w) , int(pulso[1]*h)), 15, (255, 0, 255), cv.FILLED)
                cv.circle(img, (int(polegar[0]*w) , int(polegar[1]*h)), 15, (0, 255, 255), cv.FILLED)
                cv.circle(img, (int(indicador[0]*w) , int(indicador[1]*h)), 15, (255, 255, 0), cv.FILLED)

                if (cal_dist_euclid(polegar, indicador) < 0.2):
                    ser.write("SS".encode())
                    if int(pulso[0]*w) > ((w/2) + 50):
                        ser.write("4h".encode())
                    elif int(pulso[0]*w) < ((w/2) - 50):
                        ser.write("4a".encode())
                    else:
                        ser.write("4s".encode())
                else:
                    if int(pulso[1]*h) > ((h/2) + 50):
                        ser.write("1h".encode())
                    elif int(pulso[1]*h) < ((h/2) - 50):
                        ser.write("1a".encode())
                    else:
                        ser.write("1s".encode())
                    ser.write("4s".encode())
                    print("Mão fechada")

                lapis.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
        else:
            ser.write("SS".encode())

        cv.imshow("CAM", img)

        if cv.waitKey(1) & 0XFF == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()





