import cv2
import mediapipe as mp
import numpy as np
import time
from math import acos, degrees

# Inicialización de MediaPipe Hands
mp_manos = mp.solutions.hands
mp_dibujo = mp.solutions.drawing_utils
mp_estilos_dibujo = mp.solutions.drawing_styles

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
def obtener_angulos(resultados, ancho, alto):
    if not resultados.multi_hand_landmarks:
        return None
    mano = resultados.multi_hand_landmarks[0]
    puntos_clave = {idx: np.array([int(l.x * ancho), int(l.y * alto)])
          for idx, l in enumerate(mano.landmark)}
    a1 = calcular_angulo(puntos_clave[mp_manos.HandLandmark.PINKY_TIP], puntos_clave[mp_manos.HandLandmark.PINKY_PIP], puntos_clave[mp_manos.HandLandmark.PINKY_MCP])
    a2 = calcular_angulo(puntos_clave[mp_manos.HandLandmark.RING_FINGER_TIP], puntos_clave[mp_manos.HandLandmark.RING_FINGER_PIP], puntos_clave[mp_manos.HandLandmark.RING_FINGER_MCP])
    a3 = calcular_angulo(puntos_clave[mp_manos.HandLandmark.MIDDLE_FINGER_TIP], puntos_clave[mp_manos.HandLandmark.MIDDLE_FINGER_PIP], puntos_clave[mp_manos.HandLandmark.MIDDLE_FINGER_MCP])
    a4 = calcular_angulo(puntos_clave[mp_manos.HandLandmark.INDEX_FINGER_TIP], puntos_clave[mp_manos.HandLandmark.INDEX_FINGER_PIP], puntos_clave[mp_manos.HandLandmark.INDEX_FINGER_MCP])
    a5 = calcular_angulo(puntos_clave[mp_manos.HandLandmark.THUMB_TIP], puntos_clave[mp_manos.HandLandmark.THUMB_IP], puntos_clave[mp_manos.HandLandmark.THUMB_MCP])
    a6 = calcular_angulo(puntos_clave[mp_manos.HandLandmark.THUMB_TIP], puntos_clave[mp_manos.HandLandmark.THUMB_MCP], puntos_clave[mp_manos.HandLandmark.WRIST])
    return [a1, a2, a3, a4, a5, a6]

# Letras a calibrar (sin J)
letras = list('ABCDEFGHIKLMNOPQRSTUVWXY')
indice = 0
calibrando = False
muestras = []
tiempo_inicio = 0

# Archivo de salida
archivo_salida = 'normalizaciones_calibradas.txt'
# Vaciar o crear
with open(archivo_salida, 'w') as archivo:
    archivo.write('')

# Configurar ventana
camara = cv2.VideoCapture(0)
camara.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cv2.namedWindow('Calibración Signos', cv2.WINDOW_NORMAL)

with mp_manos.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7) as detector_manos:
    while True:
        exito, fotograma = camara.read()
        if not exito:
            break
        fotograma = cv2.flip(fotograma, 1)
        alto, ancho, _ = fotograma.shape
        rgb = cv2.cvtColor(fotograma, cv2.COLOR_BGR2RGB)
        resultados = detector_manos.process(rgb)

        letra = letras[indice] if indice < len(letras) else None
        cv2.putText(fotograma, f"Letra actual: {letra}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        if calibrando and letra:
            tiempo_transcurrido = time.time() - tiempo_inicio
            tiempo_restante = max(0, 5 - tiempo_transcurrido)
            cv2.putText(fotograma, f"Calibrando... {tiempo_restante:.1f}s", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            angulos = obtener_angulos(resultados, ancho, alto)
            if angulos:
                muestras.append(angulos)
            if tiempo_transcurrido >= 5:
                promedio = np.round(np.mean(muestras, axis=0)).astype(int).tolist() if muestras else [0]*6
                with open(archivo_salida, 'a') as archivo:
                    archivo.write(f"{letra}: {promedio}\n")
                print(f"Guardado {letra}: {promedio}")
                calibrando = False
                muestras = []
                indice += 1

        if resultados.multi_hand_landmarks:
            for puntos_mano in resultados.multi_hand_landmarks:
                mp_dibujo.draw_landmarks(fotograma, puntos_mano, mp_manos.HAND_CONNECTIONS,
                                          mp_estilos_dibujo.get_default_hand_landmarks_style(),
                                          mp_estilos_dibujo.get_default_hand_connections_style())

        cv2.imshow('Calibración Signos', fotograma)
        tecla = cv2.waitKey(1) & 0xFF
        if tecla in (ord('q'), ord('Q')):
            break
        if tecla in (ord('T'), ord('t')) and letra:
            calibrando = True
            muestras = []
            tiempo_inicio = time.time()

        if indice >= len(letras):
            print("Calibración completa.")
            break

    camara.release()
    cv2.destroyAllWindows()

print(f"Resultados guardados en {archivo_salida}")
