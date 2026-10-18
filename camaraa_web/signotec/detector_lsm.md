# Detector de Lenguaje de Señas Mexicano

Este script detecta letras del alfabeto en Lengua de Señas Mexicana usando OpenCV y MediaPipe.

```python
import cv2
import mediapipe as mp
import numpy as np
from math import acos, degrees

# Inicializar MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Umbral para considerar un dedo como "levantado"
UMBRAL_MEÑIQUE = 150
UMBRAL_ANULAR = 150
UMBRAL_MEDIO = 150
UMBRAL_INDICE = 150
UMBRAL_PULGAR_EXT = 150
UMBRAL_PULGAR_INT = 150

def obtenerAngulos(results, width, height):
    angulosid = []
    pinky = []
    if not results.multi_hand_landmarks:
        return [[0,0,0,0,0,0], [0,0]]
    for hand_landmarks in results.multi_hand_landmarks:
        # Coordenadas de cada articulación...
        # (igual que en tu código original)
        # COORDENADAS MEÑIQUE
        x1, y1 = [int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * width),
                  int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * height)]
        x2, y2 = [int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].x * width),
                  int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y * height)]
        x3, y3 = [int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x * width),
                  int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y * height)]

        # COORDENADAS ANULAR
        x4 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * width)
        y4 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * height)
        x5 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x * width)
        y5 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * height)
        x6 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x * width)
        y6 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y * height)

        # COORDENADAS MEDIO
        x7 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * width)
        y7 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * height)
        x8 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x * width)
        y8 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * height)
        x9 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x * width)
        y9 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * height)

        # COORDENADAS INDICE
        x10 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
        y10 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
        x11 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x * width)
        y11 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * height)
        x12 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x * width)
        y12 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y * height)

        # COORDENADAS PULGAR PARTE EXTERNA
        x13 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * width)
        y13 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * height)
        x14 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x * width)
        y14 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y * height)
        x15 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x * width)
        y15 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y * height)

        # COORDENADAS PULGAR PARTE INTERNA
        x16 = x13; y16 = y13
        x17 = x15; y17 = y15
        x18 = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * width)
        y18 = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * height)

        # Convertir a arrays numpy...
        p1, p2, p3 = np.array([x1,y1]), np.array([x2,y2]), np.array([x3,y3])
        p4, p5, p6 = np.array([x4,y4]), np.array([x5,y5]), np.array([x6,y6])
        p7, p8, p9 = np.array([x7,y7]), np.array([x8,y8]), np.array([x9,y9])
        p10, p11, p12 = np.array([x10,y10]), np.array([x11,y11]), np.array([x12,y12])
        p13, p14, p15 = np.array([x13,y13]), np.array([x14,y14]), np.array([x15,y15])
        p16, p17, p18 = np.array([x16,y16]), np.array([x17,y17]), np.array([x18,y18])

        # Calcular longitudes
        l1, l2, l3 = np.linalg.norm(p2-p3), np.linalg.norm(p1-p3), np.linalg.norm(p1-p2)
        l4, l5, l6 = np.linalg.norm(p5-p6), np.linalg.norm(p4-p6), np.linalg.norm(p4-p5)
        l7, l8, l9 = np.linalg.norm(p8-p9), np.linalg.norm(p7-p9), np.linalg.norm(p7-p8)
        l10, l11, l12 = np.linalg.norm(p11-p12), np.linalg.norm(p10-p12), np.linalg.norm(p10-p11)
        l13, l14, l15 = np.linalg.norm(p14-p15), np.linalg.norm(p13-p15), np.linalg.norm(p13-p14)
        l16, l17, l18 = np.linalg.norm(p17-p18), np.linalg.norm(p16-p18), np.linalg.norm(p16-p17)

        # Función auxiliar para calcular ángulo
        def calc_angle(a, b, c):
            num = (a**2 + c**2 - b**2)
            den = 2*a*c
            cos_val = num/den if den>0 else 0
            return round(degrees(abs(acos(max(-1, min(1, cos_val))))))
        
        angle1 = calc_angle(l1,l2,l3)
        angle2 = calc_angle(l4,l5,l6)
        angle3 = calc_angle(l7,l8,l9)
        angle4 = calc_angle(l10,l11,l12)
        angle5 = calc_angle(l13,l14,l15)
        angle6 = calc_angle(l16,l17,l18)

        angulosid = [angle1, angle2, angle3, angle4, angle5, angle6]
        pinky = [x1, y1]
    return [angulosid, pinky]

def condicionalesLetras(dedos, frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    # (tus condicionales aquí, igual que antes)
    # ...
    return ""

def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('DetectorLSM', cv2.WINDOW_NORMAL)
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5) as hands:
        texto_formado = ""; ultima_letra = ""; contador_frames = 0
        try:
            while cap.isOpened():
                success, frame = cap.read()
                if not success: continue
                frame = cv2.flip(frame,1)
                h,w,_ = frame.shape
                results = hands.process(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
                if results.multi_hand_landmarks:
                    for lm in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame, lm, mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
                    angulosid, _ = obtenerAngulos(results,w,h)
                    dedos = [1 if ang>thr else 0 for ang,thr in zip(
                        angulosid,
                        [UMBRAL_MEÑIQUE,UMBRAL_ANULAR,UMBRAL_MEDIO,
                         UMBRAL_INDICE,UMBRAL_PULGAR_EXT,UMBRAL_PULGAR_INT])]
                    letra_actual = condicionalesLetras(dedos,frame)
                    if letra_actual:
                        if letra_actual!=ultima_letra:
                            contador_frames=1; ultima_letra=letra_actual
                        else:
                            contador_frames+=1
                            if contador_frames>=15:
                                if letra_actual=='BORRAR' and texto_formado:
                                    texto_formado=texto_formado[:-1]
                                else:
                                    texto_formado+=letra_actual
                                contador_frames=0; ultima_letra=""
                cv2.rectangle(frame,(0,h-50),(w,h),(0,0,0),-1)
                cv2.putText(frame,texto_formado,(10,h-20),
                            cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
                cv2.imshow('DetectorLSM', frame)
                if cv2.waitKey(5)&0xFF==ord('q'): break
        finally:
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
```
