from djitellopy import Tello
import cv2
import time


tello = Tello()


def visual():
    # Avvia lo streaming video
    tello.streamoff()
   # tello.takeoff()
    time.sleep(1)
    tello.streamon()
    # Loop principale
    while True:
        # Acquisisce il frame dal flusso video
        frame = tello.get_frame_read().frame
        print(frame.shape)
        # Inverte i colori del frame da RGB a BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Visualizza il frame
        cv2.imshow("Tello Stream", frame)
        
        # Controlli della tastiera per interrompere il programma
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Premi 'q' per uscire
           # tello.land()
            break
    
    tello.streamoff()
    cv2.destroyAllWindows()


tello.connect()
visual()