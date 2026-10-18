import cv2
import mediapipe as mp
import numpy as np
import time
from math import acos, degrees

# Inicialización de MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Función para calcular el ángulo entre tres puntos
def calcular_angulo(p1, p2, p3):
    a = np.linalg.norm(p2 - p3)
    b = np.linalg.norm(p1 - p3)
    c = np.linalg.norm(p1 - p2)
    if a * c == 0:
        return 0
    cos_val = (a**2 + c**2 - b**2) / (2 * a * c)
    cos_val = np.clip(cos_val, -1.0, 1.0)
    return round(degrees(acos(cos_val)))

# Extrae los seis ángulos de interés
def obtener_angulos(results, w, h):
    if not results.multi_hand_landmarks:
        return None
    hand = results.multi_hand_landmarks[0]
    lm = {idx: np.array([int(l.x * w), int(l.y * h)])
          for idx, l in enumerate(hand.landmark)}
    a1 = calcular_angulo(lm[mp_hands.HandLandmark.PINKY_TIP], lm[mp_hands.HandLandmark.PINKY_PIP], lm[mp_hands.HandLandmark.PINKY_MCP])
    a2 = calcular_angulo(lm[mp_hands.HandLandmark.RING_FINGER_TIP], lm[mp_hands.HandLandmark.RING_FINGER_PIP], lm[mp_hands.HandLandmark.RING_FINGER_MCP])
    a3 = calcular_angulo(lm[mp_hands.HandLandmark.MIDDLE_FINGER_TIP], lm[mp_hands.HandLandmark.MIDDLE_FINGER_PIP], lm[mp_hands.HandLandmark.MIDDLE_FINGER_MCP])
    a4 = calcular_angulo(lm[mp_hands.HandLandmark.INDEX_FINGER_TIP], lm[mp_hands.HandLandmark.INDEX_FINGER_PIP], lm[mp_hands.HandLandmark.INDEX_FINGER_MCP])
    a5 = calcular_angulo(lm[mp_hands.HandLandmark.THUMB_TIP], lm[mp_hands.HandLandmark.THUMB_IP], lm[mp_hands.HandLandmark.THUMB_MCP])
    a6 = calcular_angulo(lm[mp_hands.HandLandmark.THUMB_TIP], lm[mp_hands.HandLandmark.THUMB_MCP], lm[mp_hands.HandLandmark.WRIST])
    return [a1, a2, a3, a4, a5, a6]

# Letras a calibrar (sin J)
letras = list('ABCDEFGHIKLMNOPQRSTUVWXY')
idx = 0
calibrando = False
samples = []
start_time = 0

# Archivo de salida
en = 'normalizaciones_calibradas.txt'
# Vaciar o crear
with open(en, 'w') as f:
    f.write('')

# Configurar ventana
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cv2.namedWindow('Calibración Signos', cv2.WINDOW_NORMAL)

with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7) as hands:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        letra = letras[idx] if idx < len(letras) else None
        cv2.putText(frame, f"Letra actual: {letra}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        if calibrando and letra:
            elapsed = time.time() - start_time
            remaining = max(0, 5 - elapsed)
            cv2.putText(frame, f"Calibrando... {remaining:.1f}s", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            angulos = obtener_angulos(results, w, h)
            if angulos:
                samples.append(angulos)
            if elapsed >= 5:
                promedio = np.round(np.mean(samples, axis=0)).astype(int).tolist() if samples else [0]*6
                with open(en, 'a') as f:
                    f.write(f"{letra}: {promedio}\n")
                print(f"Guardado {letra}: {promedio}")
                calibrando = False
                samples = []
                idx += 1

        if results.multi_hand_landmarks:
            for lm in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing_styles.get_default_hand_landmarks_style(),
                                          mp_drawing_styles.get_default_hand_connections_style())

        cv2.imshow('Calibración Signos', frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord('q'), ord('Q')):
            break
        if key in (ord('T'), ord('t')) and letra:
            calibrando = True
            samples = []
            start_time = time.time()

        if idx >= len(letras):
            print("Calibración completa.")
            break

    cap.release()
    cv2.destroyAllWindows()

print(f"Resultados guardados en {en}")
