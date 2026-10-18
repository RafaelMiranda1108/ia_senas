import cv2
import mediapipe as mp
import numpy as np
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Capturamos la cámara
cap = cv2.VideoCapture(0)

# Obtenemos la resolución de pantalla
SCREEN_W, SCREEN_H = pyautogui.size()

# Colores para dibujo
color_mouse_pointer = (255, 0, 255)
color_base = (255, 0, 112)
color_index = (255, 198, 82)

def calculate_distance(x1, y1, x2, y2):
    return np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))

def detect_finger_down(hand_landmarks, img):
    """
    Devuelve True si el índice está “bajado” (pinch),
    dibuja bases e índice en la imagen.
    """
    h, w, _ = img.shape

    x_base1 = int(hand_landmarks.landmark[0].x * w)
    y_base1 = int(hand_landmarks.landmark[0].y * h)
    x_base2 = int(hand_landmarks.landmark[9].x * w)
    y_base2 = int(hand_landmarks.landmark[9].y * h)

    x_index = int(hand_landmarks.landmark[8].x * w)
    y_index = int(hand_landmarks.landmark[8].y * h)

    d_base = calculate_distance(x_base1, y_base1, x_base2, y_base2)
    d_base_index = calculate_distance(x_base1, y_base1, x_index, y_index)

    down = d_base_index < d_base

    c_base = (255, 0, 255) if down else color_base
    c_index = (255, 0, 255) if down else color_index
    cv2.circle(img, (x_base1, y_base1), 5, c_base, 2)
    cv2.circle(img, (x_index, y_index), 5, c_index, 2)
    cv2.line(img, (x_base1, y_base1), (x_base2, y_base2), c_base, 3)
    cv2.line(img, (x_base1, y_base1), (x_index, y_index), c_index, 3)

    return down

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5) as hands:

    while True:
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape

            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    x_norm = hand_landmarks.landmark[9].x
                    y_norm = hand_landmarks.landmark[9].y

                    x_screen = np.interp(x_norm, [0, 1], [0, SCREEN_W])
                    y_screen = np.interp(y_norm, [0, 1], [0, SCREEN_H])

                    pyautogui.moveTo(int(x_screen), int(y_screen))

                    if detect_finger_down(hand_landmarks, frame):
                        pyautogui.click()

                    cv2.circle(frame,
                               (int(x_norm * width), int(y_norm * height)),
                               10, color_mouse_pointer, 3)
                    cv2.circle(frame,
                               (int(x_norm * width), int(y_norm * height)),
                               5, color_mouse_pointer, -1)

            cv2.imshow("mouse", frame)
            key = cv2.waitKey(1)
            if key == ord("q"):
                break
        else:
            print("No se pudo leer el frame de la cámara.")
            break

cap.release()
cv2.destroyAllWindows()
