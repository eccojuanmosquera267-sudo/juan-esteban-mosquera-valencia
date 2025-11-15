import cv2

# Cargar el modelo pre-entrenado (detección de caras)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Abrir cámara (0 = cámara del PC)
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()

    # Convertir a escala de grises (mejora la detección)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar caras
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Dibujar recuadros sobre las caras
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Deteccion de Rostros", frame)

    # Salir con tecla ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

video.release()
cv2.destroyAllWindows()


import cv2

face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read("modeloLBPH.xml")

face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cam = cv2.VideoCapture(0)

people = ["usuario1"]   # si agregas más personas, pon sus nombres aquí

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        face = gray[y:y+h, x:x+w]
        label, confidence = face_recognizer.predict(face)

        if confidence < 80:
            text = people[label]
        else:
            text = "Desconocido"

        cv2.putText(frame, f"{text} ({int(confidence)})", (x,y-10), 1, 1.2, (0,255,0), 2)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow("Reconocimiento Facial", frame)
    if cv2.waitKey(1) == 27:  # ESC
        break

cam.release()
cv2.destroyAllWindows()


# deteccion_rostros.py
import cv2

# Cargar el clasificador preentrenado de rostros de OpenCV
detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Abrir la cámara
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Convertir a escala de grises (mejora precisión)
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros
    rostros = detector.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    # Dibujar rectángulos alrededor de los rostros detectados
    for (x, y, w, h) in rostros:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Detección de Rostros", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()