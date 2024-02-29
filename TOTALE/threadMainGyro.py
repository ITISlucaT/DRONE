#from pynput.mouse import Listener, Button
from djitellopy import Tello
import time
import cv2

import MuseThread
import VideoDrone


GYROSCOPE_ACTIVATED = False

command = None
leapCommand = None

tello = Tello()
tello.connect()


def main():
    global GYROSCOPE_ACTIVATED
    
    museThread = MuseThread(tello) 
    
    print ("drone connected")
    museThread.start()
    print ("Muse thread started")

    onFlight = False
    time.sleep(2)
    leapCommand = 0
    while True:
        print("in cycle")
        museOperation = command
        print("muse Operation"+ str(museOperation))
        
        print("closed muse operation")
        print("Height: "+str(tello.get_height()))
        print("battery: " + str(tello.get_battery()))
        if museOperation < 0.8: 
            height = tello.get_height()
            if onFlight == False:
                print("Takeoff")
                tello.streamoff()
                tello.takeoff() 
                time.sleep(1)
                tello.streamon()
                videoDrone = VideoDrone(tello)
                videoDrone.start()
                onFlight=True
                GYROSCOPE_ACTIVATED = True
            if height < 200:
                tello.move_up(20)
                if leapCommand == 50:
                    tello.rotate_counter_clockwise(50)# manda i comandi al drone per non farlo scendere
                    leapCommand = 0
                elif leapCommand == -50:
                    tello.rotate_counter_clockwise(-50)
                    leapCommand = 0
            else:
                if leapCommand == 50:
                    tello.rotate_counter_clockwise(50)# manda i comandi al drone per non farlo scendere
                    leapCommand = 0
                elif leapCommand == -50:
                    tello.rotate_counter_clockwise(-50)
                    leapCommand = 0
                # else:
                #     tello.send_rc_control(0,0,0,0)
        else:

            height = tello.get_height()
            if height>120:
                tello.move_down(50)
            elif onFlight==False:
                print("In attesa di concentrazione...")
            else:
                tello.land()
                museThread.stop()
                videoDrone.stop()
                museThread.join()
                videoDrone.join()
                cv2.destroyAllWindows()
                print("Land")
                break


if __name__ == '__main__':
    main()