from djitellopy import Tello
import cv2
import time


tello = Tello()


def visual():
    # Avvia lo streaming video
    tello.streamon()
    # Loop principale
    while True:
        # Acquisisce il frame dal flusso video
        frame = tello.get_frame_read().frame
        
        # Inverte i colori del frame da RGB a BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Visualizza il frame
        cv2.imshow("Tello Stream", frame)
        
        # Controlli della tastiera per interrompere il programma
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Premi 'q' per uscire
            break
    tello.streamoff()
    cv2.destroyAllWindows()


tello.connect()
# tello.takeoff()

# # Movimento
# tello.move_left(100)  # Muove il drone di 100 cm a sinistra
# tello.move_right(100)  # Muove il drone di 100 cm a destra
# tello.move_up(100)  # Muove il drone di 100 cm in su
# tello.move_down(100)  # Muove il drone di 100 cm in giù
# tello.move_forward(100)  # Muove il drone di 100 cm in avanti
# tello.move_back(100)  # Muove il drone di 100 cm indietro

# # Rotazione
# tello.rotate_clockwise(90)  # Ruota il drone di 90 gradi in senso orario
# tello.rotate_counter_clockwise(90)  # Ruota il drone di 90 gradi in senso antiorario

# time.sleep(3)
# tello.land()


visual()
    

