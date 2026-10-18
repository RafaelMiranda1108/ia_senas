import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Iniciar la cámara
camweb = cv2.VideoCapture(0)

#Opciones para configuracion del detecto
with mp_hands.Hands(
	static_image_mode=False,           # Modo dinámico para video
	max_num_hands=2,                   # Máximo de manos a detectar
	min_detection_confidence=0.5,      # Confianza mínima de detección
	min_tracking_confidence=0.5        # Confianza mínima de seguimiento
	) as hands:
	while True:
		ret, frame = camweb.read()
		if ret:
			frame = cv2.flip(frame, 1)
			# Pasar los frames de bgr a rgb ya que las detecciones se realizan con imágenes en rgb
			frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			# Se procesará por MediaPipe Hands
			results = hands.process(frame_rgb)
			# Se imprimirá una colección de datos de las manos detectadas HANDEDNESS
			print("Handedness: ", results.multi_handedness)
			#Para evitar problemas en la ejecución si no se encontro una mano añadi una condicion para que se realice el proceso siempre cuando landmarks sea no:
			if results.multi_hand_landmarks is not None:
				#Se necesita recorer cada mano para poder dibujar los 21 puntos
				for hand_landmarks in results.multi_hand_landmarks:
					mp_drawing.draw_landmarks(
					frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
					mp_drawing.DrawingSpec(color= (62, 108, 216), thickness=2, circle_radius=3),
					mp_drawing.DrawingSpec(color=(56, 210, 105), thickness=2))
				#Mostrará las coordenas de los puntos clave
				print ("Hand landmarks: ", results.multi_hand_landmarks)

			cv2.imshow("Rafa", frame)
			key = cv2.waitKey(1)

			if key == ord("q"):
				break
		else:
			print("No se pudo leer el frame de la cámara.")
			break

camweb.release()
cv2.destroyAllWindows()
