from djitellopy import Tello
import cv2
import time
import numpy as np 
from pylsl import StreamInlet, resolve_byprop
import utils

# tello = Tello()
# tello.connect()
# tello.land()

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

tello = Tello()

def museSettings():
    # Search and active LSL streams
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
    return inlet, fs, eeg_buffer


def acquireData(inlet, fs, eeg_buffer):
    """ 3.1 ACQUIRE DATA """
    filter_state = None # for use with the
    eeg_data, timestamp = inlet.pull_chunk(timeout=1, max_samples=int(SHIFT_LENGTH * fs))
    ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]
    eeg_buffer, filter_state = utils.update_buffer(eeg_buffer, ch_data, notch=True, filter_state=filter_state)

    """ 3.2 COMPUTE BAND POWERS """
    data_epoch = utils.get_last_data(eeg_buffer, EPOCH_LENGTH * fs)
    band_powers = utils.compute_band_powers(data_epoch, fs)
    #print (band_powers) 
    
    """prova per concentrazione"""
    band_beta = utils.compute_beta(data_epoch, fs)
    #print(band_beta)
    
    band_alpha = utils.compute_alpha(data_epoch, fs)
    return band_beta
    

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

def main():
    print("entrato nel main")
    inlet,fs, eeg_buffer = museSettings()
    tello.connect()
    onFlight = False
    while True:
        print("in cycle")
        museOperation = np.mean(acquireData(inlet=inlet, fs=fs, eeg_buffer=eeg_buffer))
        print(museOperation)
        print("closed muse operation")
        if museOperation < 0.15: 
            print("Altezza: "+str(tello.get_height()))
            print("Batteria: " + str(tello.get_battery()))
            height = tello.get_height()
            if onFlight == False:
                print("Takeoff")
                tello.takeoff()
                onFlight=True
            if height < 200:
                tello.move_up(20)
            else:
                tello.send_rc_control(0,0,0,0)# manda i comandi al drone per non farlo scendere
        else:
            print("Altezza: "+str(tello.get_height()))
            print("Batteria: " + str(tello.get_battery()))
            height = tello.get_height()
            if height>120:
                tello.move_down(50)
            elif onFlight==False:
                print("In attesa di concentrazione...")
            else:
                print("Land")
                break

    time.sleep(1)
    tello.land()
    tello.end()


    #visual()
    
if __name__ == '__main__':
    main()
