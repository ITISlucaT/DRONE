#
from djitellopy import Tello
import cv2

tello = Tello()
tello.connect()

def visual():
    frame_read = tello.get_frame_read()
    while True:
        # Ottieni il frame corrente dal drone
        frame = frame_read.frame

        # Visualizza il frame in una finestra
        cv2.imshow("Drone", frame)

        # Premi q sulla tastiera per uscire dal ciclo
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    tello.streamoff()


tello.takeoff()

# Movimento
tello.move_left(100)  # Muove il drone di 100 cm a sinistra
tello.move_right(100)  # Muove il drone di 100 cm a destra
tello.move_up(100)  # Muove il drone di 100 cm in su
tello.move_down(100)  # Muove il drone di 100 cm in giù
tello.move_forward(100)  # Muove il drone di 100 cm in avanti
tello.move_back(100)  # Muove il drone di 100 cm indietro

# Rotazione
tello.rotate_clockwise(90)  # Ruota il drone di 90 gradi in senso orario
tello.rotate_counter_clockwise(90)  # Ruota il drone di 90 gradi in senso antiorario

tello.land()
