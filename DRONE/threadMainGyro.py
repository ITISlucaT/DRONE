from threading import Thread
import queue
import numpy as np 
from pylsl import StreamInlet, resolve_byprop
import utils
from pynput.mouse import Listener, Button
from djitellopy import Tello
import time
import cv2

class Band:
   # Delta = 0
    #Theta = 1
    Alpha = 2
    Beta = 3

""" EXPERIMENTAL PARAMETERS """

BUFFER_LENGTH = 5
EPOCH_LENGTH = 1
OVERLAP_LENGTH = 0.8
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH
INDEX_CHANNEL = [0]

GYROSCOPE_ACTIVATED = False

command = None
leapCommand = None

tello = Tello()
tello.connect()
 
def museDxSx():
    # Obtain EEG data from the LSL stream
    gyro_data, timestamp = inlet_Gyro.pull_chunk(
    timeout=1, max_samples=int(SHIFT_LENGTH * fs_Gyro))
    
    theta = 0.2 * (gyro_data[-1][2] + gyro_data[-2][2] + gyro_data[-3][2] + gyro_data[-4][2] + gyro_data[-5][2]) * 1 / fs_Gyro #velocita in questo istante, media degli ultimi 2 valori, per giroscopio
    
    gamma = 0.2 * (gyro_data[-1][0] + gyro_data[-2][0] + gyro_data[-3][0] + gyro_data[-4][0] + gyro_data[-5][0]) * 1 / fs_Gyro

    alpha = 0.2 * (gyro_data[-1][1] + gyro_data[-2][1] + gyro_data[-3][1] + gyro_data[-4][1] + gyro_data[-5][1]) * 1 / fs_Gyro
    
    #theta = head rotation dx e sx
    #gamma = side tilt dx e sx
    #alpha = fw and rw tilt
    
    return theta, gamma, alpha #Data for the movement of the drone

class MuseThread(Thread):
    def __init__(self):
        super(MuseThread, self).__init__()
        self.buffer = queue.Queue()
    def run(self):
        global command
        SX_GAMMA = 1.5

        DX_GAMMA = -1.5

        SX_THETA = 3

        DX_THETA = -3

        FW_ALPHA = 1.5

        RW_ALPHA = -1.5

        ANGLE = 90  #Rotation angle (degrees)
        HEIGHT = 20 #Height differential value (centimeters)
        FORWARD = 20 #FW and BW movement distance (centimeters)


        print('Looking for an EEG stream...')
        streams = resolve_byprop('type', 'EEG', timeout=2)
        streams_Gyro = resolve_byprop('type', 'Gyroscope', timeout=2) #start gyroscope
        if len(streams) == 0:
            raise RuntimeError('Can\'t find EEG stream.')
        print("Start acquiring data")
        inlet = StreamInlet(streams[0], max_chunklen=12)
        inlet_Gyro = StreamInlet(streams_Gyro[0], max_chunklen=12) 
        info_Gyro = inlet_Gyro.info()
        eeg_time_correction = inlet.time_correction()
        info = inlet.info()
        description = info.desc()
        fs = int(info.nominal_srate())
        fs_Gyro = int(info_Gyro.nominal_srate()) #gyro data frequency

        """ 2. INITIALIZE BUFFERS """
        eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
        filter_state = None  # for use with the notch filter
        n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) / SHIFT_LENGTH + 1))
        band_buffer = np.zeros((n_win_test, 4))
        prec = 0
        """ 3. GET DATA """
        try:
            while True:
                """ 3.1 ACQUIRE DATA """
                eeg_data, timestamp = inlet.pull_chunk(timeout=1, max_samples=int(SHIFT_LENGTH * fs))
                ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]
                eeg_buffer, filter_state = utils.update_buffer(eeg_buffer, ch_data, notch=True, filter_state=filter_state)

                """ 3.2 COMPUTE BAND POWERS """
                data_epoch = utils.get_last_data(eeg_buffer, EPOCH_LENGTH * fs)
                band_powers = utils.compute_band_powers(data_epoch, fs)
                #print (band_powers) 
                
                """prova per concentrazione"""
                band_beta = utils.compute_beta(data_epoch, fs)
                
                band_alpha = utils.compute_alpha(data_epoch, fs)
                gyro_data, timestamp = inlet_Gyro.pull_chunk(
                timeout=1, max_samples=int(SHIFT_LENGTH * fs_Gyro))
                
                theta = 0.2 * (gyro_data[-1][2] + gyro_data[-2][2] + gyro_data[-3][2] + gyro_data[-4][2] + gyro_data[-5][2]) * 1 / fs_Gyro #velocita in questo istante, media degli ultimi 2 valori, per giroscopio
                
                gamma = 0.2 * (gyro_data[-1][0] + gyro_data[-2][0] + gyro_data[-3][0] + gyro_data[-4][0] + gyro_data[-5][0]) * 1 / fs_Gyro

                alpha = 0.2 * (gyro_data[-1][1] + gyro_data[-2][1] + gyro_data[-3][1] + gyro_data[-4][1] + gyro_data[-5][1]) * 1 / fs_Gyro
                print(theta, gamma, alpha)
                global GYROSCOPE_ACTIVATED
                if GYROSCOPE_ACTIVATED == True:
                    print("vola")
                    if gamma > SX_GAMMA:
                        tello.move_right(20)
                        k += HEIGHT
                    elif gamma < DX_GAMMA:
                        if k > HEIGHT:
                            tello.move_left(20)
                            k -= HEIGHT
                    
                    #Rotation
                    if prec > DX_THETA and prec < SX_THETA:
                        if theta > SX_THETA:
                            tello.rotate_counter_clockwise(+ANGLE)
                            time.sleep(2)
                        elif theta < DX_THETA:
                            tello.rotate_counter_clockwise(-ANGLE)
                            time.sleep(2)
                    prec = theta
                    
                    #FW and BW
                    if alpha > FW_ALPHA:
                        tello.move_forward(FORWARD)
                    elif alpha < RW_ALPHA:
                        tello.move_back(FORWARD)

                command = np.mean(band_beta)

        except KeyboardInterrupt:
            print('Closing!')

def on_click(x, y, button, pressed):
    if button == Button.left:
        print(f'Il pulsante sinistro è stato {"premuto" if pressed else "rilasciato"}')

def on_scroll(x, y, dx, dy):
# Controlla se lo spostamento verticale è verso l'alto o verso il basso e stampa di conseguenza
    global leapCommand 
    if dy < 0:
        leapCommand = 50
    else:
        leapCommand = -50

class VideoDrone(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        #Keep track of the already opened images and to prevent them to be showed again
        while True:
            # Acquisisce il frame dal flusso video
            frame = tello.get_frame_read().frame

            frame = cv2.resize(frame, (360, 240))

            cv2.waitKey(1)

            # Inverte i colori del frame da RGB a BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Visualizza il frame
            #cv2.imshow("Tello Stream", frame)
            
            # Controlli della tastiera per interrompere il programma
            # key = cv2.waitKey(1) & 0xFF
            # if key == ord('q'):  # Premi 'q' per uscire
            #      break
        tello.streamoff()
        cv2.destroyAllWindows()
        quit()



def main():
    #tello.streamon() 
    global GYROSCOPE_ACTIVATED
    
    museThread = MuseThread() 
    
    print ("drone connected")
    museThread.start()
    
    print ("thread started")

    listener = Listener(on_click=on_click, on_scroll=on_scroll)
    listener.start()

    onFlight = False
    time.sleep(2)
    while True:
        print("in cycle")
        museOperation = command
        print("muse Operation"+ str(museOperation))
        leapCommand = 0
        print("closed muse operation")
        print("Altezza: "+str(tello.get_height()))
        print("Batteria: " + str(tello.get_battery()))
        if museOperation < 0.5: 
            height = tello.get_height()
            if onFlight == False:
                print("Takeoff")
                tello.streamoff()
                tello.takeoff() 
                time.sleep(1)
                #tello.streamon()
                #videoDrone = VideoDrone()
                #videoDrone.start()
                onFlight=True
                GYROSCOPE_ACTIVATED = True
            if height < 200:
                tello.move_up(20)
            else:
                if leapCommand == 50:
                    tello.rotate_counter_clockwise(50)# manda i comandi al drone per non farlo scendere
                elif leapCommand == -50:
                    tello.rotate_counter_clockwise(-50)
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
                cv2.destroyAllWindows()
                print("Land")
                break

    museThread.join()
   # t2.join()

if __name__ == '__main__':
    main()