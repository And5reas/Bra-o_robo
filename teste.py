# import cv2
# import mediapipe as mp
# import time

# cap = cv2.VideoCapture(1)
# mpHands = mp.solutions.hands
# hands = mpHands.Hands()
# mpDraw = mp.solutions.drawing_utils

# pTime = 0
# cTime = 0
 
# while True:
#     success, image = cap.read()
#     imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = hands.process(imgRGB)
 
#     #rint(results.multi_hand_landmarks)
#     if results.multi_hand_landmarks:
#         for handLms in results.multi_hand_landmarks:
#             for id, lm in enumerate (handLms.landmark):
#                 #print(id,lm)
#                 h, w, c = image.shape
#                 cx, cy = int(lm.x*w), int(lm.y*h)
#                 print(id, cx, cy)
#                 if id == 4:
#                     cv2.circle(image,(cx,cy),15, (255,0,255),cv2.FILLED)
 
#             mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
 
#     cTime = time.time()
#     fps = 1/(cTime-pTime)
#     pTime = cTime
 
#     cv2.putText(image, str(int(fps)),(10,60), cv2.FONT_HERSHEY_PLAIN,3, (255,0,255),4)
#     cv2.imshow("Results", image)
#     if cv2.waitKey(1) & 0XFF == ord('q'):
#         break


# import serial

# # Abra a porta serial. Verifique se o número da porta está correto (pode variar de sistema para sistema).
# ser = serial.Serial('COM3', 9600)  # No Windows, pode ser algo como 'COM3'

# while True:
#     data = input("Digite algo para enviar ao Arduino: ")
#     ser.write(data.encode())  # Envie os dados para o Arduino
#     received_data = ser.readline().decode().strip()  # Leia os dados recebidos do Arduino
#     print("Dados recebidos do Arduino:", received_data)

# ser.close()  # Feche a porta serial quando terminar



# coordenadas = {0: (404, 379), 4: (415, 299), 8: (414, 302), 12: (430, 314), 16: (445, 327), 20: (452, 344)}

# # Inicialize as variáveis para as médias
# media_x = 0
# media_y = 0

# # Percorra o dicionário para calcular a soma das coordenadas x e y
# for valor in coordenadas.values():
#     media_x += valor[0]
#     media_y += valor[1]

# # Divida a soma pelo número de elementos para obter a média
# num_elementos = len(coordenadas)
# media_x /= num_elementos
# media_y /= num_elementos

# print("Média das coordenadas x:", media_x)
# print("Média das coordenadas y:", media_y)

import cv2 as cv
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Função para calcular a distância euclidiana entre dois pontos (x, y)
def calcular_distancia(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Inicialize o detector de mãos
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

cap = cv.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Converta a imagem para RGB
    image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # Detecte mãos na imagem
    results = hands.process(image)

    if results.multi_hand_landmarks:
        # Para cada mão detectada
        for hand_landmarks in results.multi_hand_landmarks:
            # Desenhe landmarks na imagem
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Verifique a distância entre os landmarks dos dedos
            thumb_tip = (hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y)
            index_tip = (hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y)

            distancia = calcular_distancia(thumb_tip, index_tip)

            # Defina um limite para determinar se a mão está fechada
            limite_mao_fechada = 0.05 # Ajuste conforme necessário

            if distancia < limite_mao_fechada:
                print("Mão está fechada")

    cv.imshow('Hand Detection', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

hands.close()
cap.release()
cv.destroyAllWindows()
