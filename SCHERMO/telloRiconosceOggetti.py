import cv2
import mediapipe as mp
from djitellopy import Tello
from mediapipe.python.solutions import objectron as mp_objectron
from mediapipe.python.solutions import drawing_utils as mp_drawing

# Inizializza il drone DJI Tello
tello = Tello()
tello.connect()

# Avvia lo streaming video
tello.streamon()

with mp_objectron.Objectron(
    static_image_mode=False,
    max_num_objects=1,
    min_detection_confidence=0.5,
    model_path='path_to_your_local_model/object_detection_3d_cup.tflite') as objectron:

    while True:
        # Ottieni il frame dallo streaming video del Tello
        frame = tello.get_frame_read().frame

        # Converte l'immagine in RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Rileva gli oggetti nell'immagine
        results = objectron.process(image_rgb)

       
        print(results)

        # if results.multi_object_landmarks:
        #     for detected_object in results.multi_object_landmarks:
        #         mp_drawing.draw_landmarks(
        #             image, detected_object, mp_objectron.BOX_CONNECTIONS)

        # Mostra il frame con i bounding box
        cv2.imshow("Riconoscimento oggetti con Objectron", frame)

        # Interrompi il loop premendo 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

# Rilascia la webcam e chiudi la finestra
tello.streamoff()
cv2.destroyAllWindows()
