import cv2
import mediapipe as mp

from mediapipe.python.solutions import objectron as mp_objectron

from mediapipe.python.solutions import drawing_utils as mp_drawing


def find_objects_in_image(image_path):
    # Carica l'immagine
    image = cv2.imread(image_path)
    if image is None:
        print("Impossibile leggere l'immagine.")
        return

    # Converte l'immagine in RGB (MediaPipe lavora con immagini RGB)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Inizializza l'istanza di Objectron
    with mp_objectron.Objectron(static_image_mode=True) as objectron:
        # Rileva gli oggetti nell'immagine
        results = objectron.process(image_rgb)

        print(results)

        # if results.multi_object_landmarks:
        #     for detected_object in results.multi_object_landmarks:
        #         mp_drawing.draw_landmarks(
        #             image, detected_object, mp_objectron.BOX_CONNECTIONS)

        # Mostra l'immagine con i bounding box
        cv2.imshow("Objects Detected", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Esempio di utilizzo
find_objects_in_image("./test.jpg")
