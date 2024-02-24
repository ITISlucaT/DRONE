import cv2
import numpy as np

# Carica l'immagine
file_path = 'immagine.jpg'
img = cv2.imread(file_path)

if img is None:
    print(f"Impossibile aprire o leggere il file {file_path}.")
else:
    # Pre-elaborazione dell'immagine
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Rilevamento dell'oggetto
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Disegna i rettangoli
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Visualizza l'immagine
    cv2.imshow('img', img)
    cv2.waitKey()
