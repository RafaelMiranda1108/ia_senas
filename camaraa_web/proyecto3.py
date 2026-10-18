import cv2
import mediapipe as mp
from math import degrees, acos
import numpy as np
import time  # Para medir intervalos de tiempo

# Inicialización del módulo de manos de MediaPipe
mp_hands = mp.solutions.hands

# Normalizaciones esperadas por letra (ángulos)
normalizaciones = {
    'A': [88, 74, 68, 47, 174, 178],
    'B': [178, 178, 175, 175, 115, 75],
    'C': [123, 93, 90, 108, 175, 178],
    'D': [28, 17, 18, 174, 125, 105],
    'E': [37, 20, 21, 24, 87, 91],
    'F': [179, 178, 174, 27, 150, 134],
    'G': [64, 58, 51, 176, 155, 174],
    'H': [9, 21, 176, 174, 162, 124],
    'I': [175, 19, 12, 5, 122, 108],
    'K': [89, 74, 179, 169, 172, 163],
    'L': [21, 9, 7, 177, 168, 166],
    'M': [115, 173, 178, 177, 165, 133],
    'N': [53, 24, 178, 176, 164, 120],
    'O': [106, 96, 100, 104, 174, 177],
    'P': [35, 24, 17, 177, 147, 173],
    'Q': [43, 37, 53, 69, 174, 134],
    'R': [86, 27, 166, 173, 156, 107],
    'S': [56, 37, 34, 30, 110, 112],
    'T': [100, 97, 62, 115, 174, 144],
    'U': [77, 31, 179, 173, 138, 103],
    'V': [79, 26, 177, 176, 147, 100],
    'W': [36, 174, 176, 174, 155, 80],
    'X': [63, 66, 68, 108, 173, 163],
    'Y': [179, 29, 40, 20, 164, 178]
}

# Tolerancia para la detección de ángulos
TOLERANCIA = 30

def obtenerAngulos(results, width, height):
    """
    Obtiene los ángulos de cada dedo a partir de los landmarks de la mano
    """
    angulosid = []  # Lista de ángulos por dedo
    pinky = []      # Posición del meñique para detectar movimiento (letra J)
    
    for hand_landmarks in results.multi_hand_landmarks:
        # Extraer puntos de interés
        points = {}
        for idx, landmark in enumerate(hand_landmarks.landmark):
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            points[idx] = np.array([x, y])
        
        # Puntos meñique
        p1 = points[mp_hands.HandLandmark.PINKY_TIP]
        p2 = points[mp_hands.HandLandmark.PINKY_PIP]
        p3 = points[mp_hands.HandLandmark.PINKY_MCP]
        
        # Puntos anular
        p4 = points[mp_hands.HandLandmark.RING_FINGER_TIP]
        p5 = points[mp_hands.HandLandmark.RING_FINGER_PIP]
        p6 = points[mp_hands.HandLandmark.RING_FINGER_MCP]
        
        # Puntos medio
        p7 = points[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        p8 = points[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
        p9 = points[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        
        # Puntos índice
        p10 = points[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        p11 = points[mp_hands.HandLandmark.INDEX_FINGER_PIP]
        p12 = points[mp_hands.HandLandmark.INDEX_FINGER_MCP]
        
        # Puntos pulgar externo
        p13 = points[mp_hands.HandLandmark.THUMB_TIP]
        p14 = points[mp_hands.HandLandmark.THUMB_IP]
        p15 = points[mp_hands.HandLandmark.THUMB_MCP]
        
        # Punto muñeca para pulgar interno
        p18 = points[mp_hands.HandLandmark.WRIST]
        
        def calcularAngulo(p1, p2, p3):
            """Calcula el ángulo entre tres puntos"""
            a = np.linalg.norm(p2 - p3)
            b = np.linalg.norm(p1 - p3)
            c = np.linalg.norm(p1 - p2)
            
            if a and c != 0:
                cos_value = (a**2 + c**2 - b**2) / (2 * a * c)
                if -1 < cos_value < 1:
                    return round(degrees(abs(acos(cos_value))))
            return 0
        
        # Calcular ángulos de cada dedo
        angle1 = calcularAngulo(p1, p2, p3)    # Meñique
        angle2 = calcularAngulo(p4, p5, p6)    # Anular
        angle3 = calcularAngulo(p7, p8, p9)    # Medio
        angle4 = calcularAngulo(p10, p11, p12) # Índice
        angle5 = calcularAngulo(p13, p14, p15) # Pulgar externo
        angle6 = calcularAngulo(p13, p15, p18) # Pulgar interno (con muñeca)
        
        angulosid = [angle1, angle2, angle3, angle4, angle5, angle6]
        
        # Guardar posición del meñique para detectar movimiento (letra J)
        pinky = [int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * width),
                 int(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * height)]
        
    return [angulosid, pinky]

def detectarLetraPorAngulos(angulos, tolerancia=TOLERANCIA):
    """
    Detecta la letra según la comparación de ángulos con las normalizaciones
    """
    if not angulos:
        return None
        
    mejor_letra = None
    menor_diferencia = float('inf')
    
    for letra, modelo in normalizaciones.items():
        # Calcular la diferencia total entre los ángulos y el modelo
        diferencia = sum(abs(a - m) for a, m in zip(angulos, modelo))
        
        # Verificar si todos los ángulos están dentro de la tolerancia
        if all(abs(a - m) <= tolerancia for a, m in zip(angulos, modelo)):
            if diferencia < menor_diferencia:
                menor_diferencia = diferencia
                mejor_letra = letra
    
    return mejor_letra

def deducirDedosLevantados(angulos):
    """
    Convierte los ángulos en una representación binaria de dedos levantados o no
    """
    dedos = []
    
    # Pulgar externo (ángulo 5)
    if angulos[5] > 125:
        dedos.append(1)
    else:
        dedos.append(0)
        
    # Pulgar interno (ángulo 4)
    if angulos[4] > 150:
        dedos.append(1)
    else:
        dedos.append(0)
        
    # Dedos del índice al meñique (ángulos 3, 2, 1, 0)
    for i in range(3, -1, -1):
        if angulos[i] > 90:
            dedos.append(1)
        else:
            dedos.append(0)
            
    return dedos

def condicionalesLetras(dedos, frame, angulos=None):
    """
    Detecta la letra basada en la configuración de dedos y muestra en pantalla
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    letra = None
    
    # Si tenemos información de ángulos, intentamos primero la detección por ángulos
    if angulos:
        letra_por_angulos = detectarLetraPorAngulos(angulos)
        if letra_por_angulos:
            cv2.rectangle(frame, (0, 0), (100, 100), (255, 255, 255), -1)
            cv2.putText(frame, letra_por_angulos, (20, 80), font, 3, (0, 0, 0), 2, cv2.LINE_AA)
            return letra_por_angulos
    
    # Si no se detectó por ángulos o no hay información de ángulos, usamos el método original
    # Mapeo de configuraciones de dedos a letras
    letras_config = {
        (1, 1, 0, 0, 0, 0): "A",
        (0, 0, 0, 0, 0, 0): "E",
        (0, 0, 1, 0, 0, 0): "I",
        (1, 0, 1, 0, 0, 0): "O",
        (0, 0, 1, 0, 0, 1): "U",
        (0, 0, 1, 1, 1, 1): "B",
        (1, 0, 1, 0, 0, 0): "C",
        (0, 0, 0, 0, 0, 1): "D",
        (1, 1, 1, 1, 1, 0): "F", 
        (1, 0, 0, 0, 0, 0): "G",
        (0, 1, 1, 0, 0, 0): "H",
        (1, 1, 0, 0, 1, 1): "K",
        (1, 1, 0, 0, 0, 1): "L",
        (0, 0, 0, 1, 1, 1): "M",
        (0, 1, 0, 0, 1, 1): "N",
        (0, 1, 1, 1, 1, 1): "P",
        (1, 0, 0, 1, 1, 1): "Q",
        (1, 0, 1, 1, 0, 0): "R",
        (1, 0, 0, 0, 0, 1): "S", 
        (0, 0, 0, 1, 0, 1): "T",
        (0, 1, 0, 0, 1, 1): "V",
        (0, 1, 0, 1, 1, 1): "W",
        (0, 1, 1, 0, 0, 1): "X",
        (1, 1, 1, 0, 0, 0): "Y"
    }
    
    # Convertir dedos a tupla para usarla como clave en el diccionario
    dedos_tuple = tuple(dedos)
    
    # Verificar si la configuración existe en nuestro mapeo
    if dedos_tuple in letras_config:
        letra = letras_config[dedos_tuple]
        cv2.rectangle(frame, (0, 0), (100, 100), (255, 255, 255), -1)
        cv2.putText(frame, letra, (20, 80), font, 3, (0, 0, 0), 2, cv2.LINE_AA)
        
    return letra

def main():
    lectura_actual = 0
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    mp_drawing_styles = mp.solutions.drawing_styles
    
    # Para guardar letras reconocidas
    saved_letters = []  # Lista de letras reconocidas
    current_letter = None
    letter_start_time = 0
    letter_recognition_time = 3  # segundos para guardar la letra (reducido para mejor experiencia)
    
    cap = cv2.VideoCapture(0)
    wCam, hCam = 1280, 720
    cap.set(3, wCam)
    cap.set(4, hCam)
    cv2.namedWindow('Signotec Mejorado', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('Signotec Mejorado', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    
    with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.75) as hands:
    
        while True:
            ret, frame = cap.read()
            if ret == False:
                break
                
            height, width, _ = frame.shape
            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
            
            # Mostrar letras guardadas
            cv2.rectangle(frame, (0, height-50), (width, height), (0, 0, 0), -1)
            cv2.putText(frame, "Letras guardadas: " + "".join(saved_letters), 
                       (10, height-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Mostrar instrucciones
            cv2.putText(frame, "Q: Salir | C: Borrar ultima letra | R: Reset palabra", 
                       (width-550, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
            
            if results.multi_hand_landmarks is not None:
                # Accediendo a los puntos de referencia
                resultado_angulos = obtenerAngulos(results, width, height)
                angulosid = resultado_angulos[0]
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    print("Hand landmarks:")
                    for i, landmark in enumerate(hand_landmarks.landmark):
                        print(f"  Landmark {i}: x={landmark.x:.3f}, y={landmark.y:.3f}, z={landmark.z:.3f}")
    
                    print("Handedness:", handedness.classification[0].label)
                    print("Confidence:", f"{handedness.classification[0].score:.2f}")
                    print("-" * 50)

                
                if angulosid:
                    # Mostrar ángulos en pantalla para debug
                    ang_text = f"Ángulos: {angulosid}"
                    cv2.putText(frame, ang_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
                    
                    # Obtener dedos levantados basados en ángulos
                    dedos = deducirDedosLevantados(angulosid)
                    
                    # Mostrar estado de dedos para debug
                    dedos_text = f"Dedos: {dedos}"
                    cv2.putText(frame, dedos_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)
                    
                    # Detectar letra usando ambos métodos
                    detected_letter = condicionalesLetras(dedos, frame, angulosid)
                    
                    # Gestión de la letra J (con movimiento)
                    pinky = resultado_angulos[1]
                    if pinky:
                        pinkY = pinky[1] + pinky[0]
                        resta = pinkY - lectura_actual
                        lectura_actual = pinkY
                        
                        if dedos == [0, 0, 1, 0, 0, 0]:
                            if abs(resta) > 30:
                                detected_letter = "J"
                                font = cv2.FONT_HERSHEY_SIMPLEX
                                cv2.rectangle(frame, (0, 0), (100, 100), (255, 255, 255), -1)
                                cv2.putText(frame, 'J', (20, 80), font, 3, (0, 0, 0), 2, cv2.LINE_AA)
                    
                    # Sistema de reconocimiento y guardado de letras
                    if detected_letter:
                        if current_letter == detected_letter:
                            # La misma letra sigue siendo detectada
                            time_elapsed = time.time() - letter_start_time
                            
                            # Mostrar temporizador
                            progress = min(time_elapsed / letter_recognition_time, 1.0)
                            bar_width = 200
                            progress_width = int(bar_width * progress)
                            
                            cv2.rectangle(frame, (width-bar_width-10, 60), (width-10, 80), (0, 0, 0), 2)
                            cv2.rectangle(frame, (width-bar_width-10, 60), (width-bar_width-10+progress_width, 80), (0, 255, 0), -1)
                            
                            if time_elapsed >= letter_recognition_time and detected_letter not in saved_letters[-1:]:
                                saved_letters.append(detected_letter)
                                letter_start_time = time.time()  # Reiniciar temporizador
                        else:
                            # Se detectó una nueva letra
                            current_letter = detected_letter
                            letter_start_time = time.time()
    
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())
            
            cv2.imshow('Signotec Mejorado', frame)
            
            # Comprobar teclas presionadas
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == ord('Q'):  # Salir con la tecla Q
                break
            elif key == ord('c') or key == ord('C'):  # Borrar última letra con la tecla C
                if saved_letters:
                    saved_letters.pop()
            elif key == ord('r') or key == ord('R'):  # Reiniciar palabra con la tecla R
                saved_letters = []
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
