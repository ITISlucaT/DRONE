"""
Tello Drone Control with Muse and Computer Vision

This script utilizes a Tello drone, Muse EEG data, and computer vision to control the drone's flight based on user concentration.

Libraries:
    - djitellopy: Tello drone control library
    - cv2: OpenCV for image processing
    - webbrowser: Module for opening a web browser
    - MuseThread: Custom thread for processing EEG and gyroscope data
    - VideoDrone: Custom thread for streaming and displaying Tello drone video
    - ResultThread: Custom thread for running the circles game and generating a report

Usage:
    - Run the script to initiate Tello drone control using Muse and computer vision.

Example:
    - python tello_muse_control.py

Date: 29/02/2023
"""
from djitellopy import Tello
import time
import cv2
import webbrowser

from MuseThread import MuseThread
from VideoDrone import VideoDrone
from ResultThread import ResultThread


tello = Tello()
tello.connect()

MAX_HEIGHT = 200
MINIMUM_HEIGHT_VALUE_TO_ACTIVATE_MOVEMENT = 120
MINIMUM_CONCENTRATION_VALUE = 0.8 #NOTE: this value is the result of a logarithm so the lower the value, the higher the concentration


time.sleep(1)
def main():
    museThread = MuseThread(tello) 
    print ("drone connected")
    museThread.start()
    print ("Muse thread started")
    onFlight = False
    time.sleep(2)
    while True:
        museOperation = museThread.command
        print("muse Operation"+ str(museOperation))
        droneMove = museThread.droneCommandList
        roll=droneMove[0]
        yaw=droneMove[1]
        pitch=droneMove[2]
        print("Height: "+str(tello.get_height()))
        print("battery: " + str(tello.get_battery()))
        if museOperation < MINIMUM_CONCENTRATION_VALUE: 
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

            if height < MAX_HEIGHT:
                tello.send_rc_control(roll,pitch, 20,yaw)
                time.sleep(2)
            else:
                tello.send_rc_control(roll,pitch,0,yaw)
                time.sleep(2)
        else:
            height = tello.get_height()
            if height>MINIMUM_HEIGHT_VALUE_TO_ACTIVATE_MOVEMENT:
                # tello.move_down(50)
                tello.send_rc_control(roll,pitch,-50,yaw)
                time.sleep(2)
            elif onFlight==False:
                print("In attesa di concentrazione...")
                time.sleep(1)
            else:
                #stop the program
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