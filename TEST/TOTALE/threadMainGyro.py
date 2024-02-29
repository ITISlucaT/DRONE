#from pynput.mouse import Listener, Button
from djitellopy import Tello
import time
import cv2
import webbrowser

from MuseThread import MuseThread
from VideoDrone import VideoDrone
from main import ResultThread


command = None
leapCommand = None

tello = Tello()
tello.connect()

time.sleep(1)
def main():
    museThread = MuseThread(tello) 
    
    print ("drone connected")
    museThread.start()
    print ("Muse thread started")

    onFlight = False
    time.sleep(2)
    leapCommand = 0
    while True:
        print("in cycle")
        museOperation = museThread.command
        print("muse Operation"+ str(museOperation))
        droneMove = museThread.droneCommandList
        rollio=droneMove[0]
        imbardata=droneMove[1]
        beccheggio=droneMove[2]

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
                time.sleep(1)
                resultThread = ResultThread()
                resultThread.start()
                onFlight=True
                museThread.GYROSCOPE_ACTIVATED = True

            if height < 200:
                # tello.move_up(20)
                tello.send_rc_control(rollio,beccheggio, 20,imbardata)
                time.sleep(2)
            else:
                tello.send_rc_control(rollio,beccheggio,0,imbardata)
                time.sleep(2)
        else:
            height = tello.get_height()
            if height>120:
                # tello.move_down(50)
                tello.send_rc_control(rollio,beccheggio,-50,imbardata)
                time.sleep(2)
            elif onFlight==False:
                print("In attesa di concentrazione...")
                time.sleep(1)
            else:
                #interrompe il programma
                tello.land()
                museThread.stop()
                videoDrone.stop()
                time.sleep(1)
                museThread.join()
                videoDrone.join()
                resultThread.join()
                cv2.destroyAllWindows()
                print("Land")
                webbrowser.open("output.html")
                break


if __name__ == '__main__':
    main()