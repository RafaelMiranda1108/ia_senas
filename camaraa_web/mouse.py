import cv2
import mediapipe as mp
import numpy as np
import pyautogui
from math import hypot

# 1. Configuración inicial
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Área de mapeo en la imagen
X_Y_INI = 100
SCREEN_GAME_X_INI = 150
SCREEN_GAME_Y_INI = 160
SCREEN_GAME_X_FIN = SCREEN_GAME_X_INI + 780
SCREEN_GAME_Y_FIN = SCREEN_GAME_Y_INI + 450
aspect_ratio = (SCREEN_GAME_X_FIN - SCREEN_GAME_X_INI) / (SCREEN_GAME_Y_FIN - SCREEN_GAME_Y_INI)

# Umbral de distancia (en píxeles de imagen) para considerar 'clic'
CLICK_THRESHOLD = 40

# Variables para suavizado
alpha = 0.2
prev_x, prev_y = 0, 0

def apply_smoothing(x, y):
    global prev_x, prev_y, alpha
    sm_x = prev_x + alpha * (x - prev_x)
    sm_y = prev_y + alpha * (y - prev_y)
    prev_x, prev_y = sm_x, sm_y
    return int(sm_x), int(sm_y)

def detect_click(landmarks, width, height):
    # Distancia pulgar–índice
    x_thumb = int(landmarks.landmark[4].x * width)
    y_thumb = int(landmarks.landmark[4].y * height)
    x_index = int(landmarks.landmark[8].x * width)
    y_index = int(landmarks.landmark[8].y * height)
    dist = hypot(x_thumb - x_index, y_thumb - y_index)
    return dist < CLICK_THRESHOLD

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)

        # Dibujar área de interacción
        area_w = width - 2 * X_Y_INI
        area_h = int(area_w / aspect_ratio)
        overlay = frame.copy()
        cv2.rectangle(overlay, (X_Y_INI, X_Y_INI),
                      (X_Y_INI + area_w, X_Y_INI + area_h),
                      (255, 0, 0), 2)
        output = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)

        # Procesar detección de manos
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            # Coordenadas de referencia (landmark 9, centro de la palma)
            x9 = int(hand.landmark[9].x * width)
            y9 = int(hand.landmark[9].y * height)
            # Mapear al área de pantalla
            xm = np.interp(x9, (X_Y_INI, X_Y_INI + area_w),
                           (SCREEN_GAME_X_INI, SCREEN_GAME_X_FIN))
            ym = np.interp(y9, (X_Y_INI, X_Y_INI + area_h),
                           (SCREEN_GAME_Y_INI, SCREEN_GAME_Y_FIN))
            # Suavizado
            sx, sy = apply_smoothing(xm, ym)
            pyautogui.moveTo(sx, sy)

            # Detección de clic
            if detect_click(hand, width, height):
                pyautogui.click()

            # Visualización
            cv2.circle(output, (x9, y9), 10, (255, 0, 255), 3)
            cv2.circle(output, (x9, y9), 5, (255, 0, 255), -1)

        cv2.imshow("Control por Mano", output)
        if cv2.waitKey(1) & 0xFF == 27:  # Esc para salir
            break

cap.release()
cv2.destroyAllWindows()
