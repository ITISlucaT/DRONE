import cv2
from djitellopy import Tello

# Inizializza il drone Tello
tello = Tello()

# Connessione al drone
tello.connect()

# Avvia lo streaming video dal drone
tello.streamon()

while True:
    # Acquisisci il frame dal flusso video del drone
    frame = tello.get_frame_read().frame

    # Rileva i volti nel frame
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=4)

    # Disegna i rettangoli intorno ai volti rilevati
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Visualizza il frame con i rettangoli
    cv2.imshow("Rilevamento volti", frame)

    # Esci se viene premuto il tasto 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Ferma lo streaming video e chiudi le finestre
tello.streamoff()
cv2.destroyAllWindows()
