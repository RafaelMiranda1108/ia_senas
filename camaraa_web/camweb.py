import cv2

# Iniciar la cámara (0 normalmente es la cámara predeterminada de la lap)
camweb = cv2.VideoCapture(0)

while True:
    ret, frame = camweb.read()

    if ret:
        cv2.imshow("Rafa", frame)
        key = cv2.waitKey(1)

        if key == ord("q"):
            break
    else:
        print("No se pudo leer el frame de la cámara.")
        break

camweb.release()
cv2.destroyAllWindows()

