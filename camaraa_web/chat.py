import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Inicializa la cámara
camweb = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,           # Modo dinámico para video
    max_num_hands=2,                   # Máximo de manos a detectar
    min_detection_confidence=0.5,      # Confianza mínima de detección
    min_tracking_confidence=0.5        # Confianza mínima de seguimiento
) as hands:

    while True:
        ret, frame = camweb.read()
        if not ret:
            print("No se pudo leer el frame de la cámara.")
            break

        # Convertir el frame de BGR (OpenCV) a RGB (MediaPipe)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Procesar la imagen para detectar manos
        results = hands.process(image)

        # Volver a BGR para mostrarlo con OpenCV
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Dibujar las manos detectadas
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Mostrar el resultado
        cv2.imshow("Rafa", image)

        key = cv2.waitKey(1)
        if key == ord("q"):
            break

# Liberar recursos
camweb.release()
cv2.destroyAllWindows()
