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

command = None
leapCommand = None

tello = Tello()
tello.connect()
 

class MuseThread(Thread):
    def __init__(self):
        super(MuseThread, self).__init__()
        self.buffer = queue.Queue()
    def run(self):
        global command
        print('Looking for an EEG stream...')
        streams = resolve_byprop('type', 'EEG', timeout=2)
        if len(streams) == 0:
            raise RuntimeError('Can\'t find EEG stream.')
        print("Start acquiring data")
        inlet = StreamInlet(streams[0], max_chunklen=12)
        eeg_time_correction = inlet.time_correction()
        info = inlet.info()
        description = info.desc()
        fs = int(info.nominal_srate())

        """ 2. INITIALIZE BUFFERS """
        eeg_buffer = np.zeros((int(fs * BUFFER_LENGTH), 1))
        filter_state = None  # for use with the notch filter
        n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) / SHIFT_LENGTH + 1))
        band_buffer = np.zeros((n_win_test, 4))
        rilevations = np.zeros()
        """ 3. GET DATA """
        try:
            while True:
                for i in range(1,10):
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
                    rilevations = np.insert(band_beta)


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
                tello.streamon()
                videoDrone = VideoDrone()
                videoDrone.start()
                onFlight=True
            if height < 200:
                tello.move_up(20)
            else:
                if leapCommand == 50:
                    tello.rotate_counter_clockwise(50)# manda i comandi al drone per non farlo scendere
                elif leapCommand == -50:
                    tello.rotate_counter_clockwise(-50)
                else:
                    tello.send_rc_control(0,0,0,0)
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