
from threading import Thread
from pylsl import StreamInlet, resolve_byprop
import utils
import numpy as np 
import time

BUFFER_LENGTH = 5
EPOCH_LENGTH = 1
OVERLAP_LENGTH = 0.8
SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH
INDEX_CHANNEL = [0]

class Band:
   # Delta = 0
    #Theta = 1
    Alpha = 2
    Beta = 3

class MuseThread(Thread):

    """
    Thread class for processing EEG data and controlling a Tello drone based on the acquired data.

    Attributes:
        tello (Tello): Instance of the Tello drone.
        SX_GAMMA (float): Threshold for gamma value indicating a move to the right.
        DX_GAMMA (float): Threshold for gamma value indicating a move to the left.
        SX_THETA (float): Threshold for theta value indicating a clockwise rotation.
        DX_THETA (float): Threshold for theta value indicating an anticlockwise rotation.
        FW_ALPHA (float): Threshold for alpha value indicating a move forward.
        RW_ALPHA (float): Threshold for alpha value indicating a move backward.
        ANGLE (float): Rotation angle in degrees.
        HEIGHT (float): Height differential value in centimeters.
        FORWARD (float): Forward and backward movement distance in centimeters.
        prec (float): Variable to store the previous theta value.
        vertical_position (float): Variable for maintaining vertical position during movement.
        inlet (StreamInlet): Inlet for EEG data stream.
        inlet_Gyro (StreamInlet): Inlet for gyroscope data stream.
        fs (int): Nominal sampling rate for EEG data.
        fs_Gyro (int): Nominal sampling rate for gyroscope data.
        eeg_buffer (numpy.ndarray): Buffer for storing EEG data.
        filter_state: State for the notch filter.
        band_beta (numpy.ndarray): Band power values for beta frequency range.
    """

    def __init__(self, tello):
        """
        Initialize the MuseThread with a Tello instance.

        Args:
            tello (Tello): Instance of the Tello drone.
        """
        super(MuseThread, self).__init__()
        self.tello = tello
        self.SX_GAMMA = 10  #ROLLIO
        self.DX_GAMMA = -10
        self.SX_THETA = 20  #IMBARDATA
        self.DX_THETA = -20
        self.FW_ALPHA = -10  #BECCHEGGIO
        self.RW_ALPHA = 10
        self.ANGLE = 40
        self.HEIGHT = 20
        self.FORWARD = 20
        self.prec = 0
        self.vertical_position=20
        self.stop_flag = False
        self.GYROSCOPE_ACTIVATED = False
        self.command = 20
        self.droneCommandList = [0,0,0]
    def run(self):
        """
        Run the MuseThread to process EEG and gyroscope data, and control the Tello drone accordingly.
        """
        self.initialize_eeg_stream()
        self.initialize_buffer()
        try:
            while not self.stop_flag:
                self.acquire_data()
                self.compute_band_power()
                self.compute_gyro_data()
                self.command = np.mean(self.band_beta)

        except KeyboardInterrupt:
            print('Closing!')

    def initialize_eeg_stream(self):
        """
        Initialize the EEG stream by resolving and configuring the required streams.
        """
        print('Looking for an EEG stream...')
        streams = resolve_byprop('type', 'EEG', timeout=2)
        streams_Gyro = resolve_byprop('type', 'Gyroscope', timeout=2)

        if len(streams) == 0:
            raise RuntimeError('Can\'t find EEG stream.')
        
        print("Start acquiring data")
        self.inlet = StreamInlet(streams[0], max_chunklen=12)
        self.inlet_Gyro = StreamInlet(streams_Gyro[0], max_chunklen=12) 
        info_Gyro = self.inlet_Gyro.info()
        eeg_time_correction = self.inlet.time_correction()
        info = self.inlet.info()
        description = info.desc()
        self.fs = int(info.nominal_srate())
        self.fs_Gyro = int(info_Gyro.nominal_srate()) 

    def initialize_buffer(self):
        """
        Initialize the EEG buffer and related parameters.
        """
        self.eeg_buffer = np.zeros((int(self.fs * BUFFER_LENGTH), 1))
        self.filter_state = None  # for use with the notch filter
        n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) / SHIFT_LENGTH + 1))
        band_buffer = np.zeros((n_win_test, 4))



    def acquire_data(self):
        """
        Acquire EEG data from the stream and update the EEG buffer.
        """
        eeg_data, timestamp = self.inlet.pull_chunk(timeout=1, max_samples=int(SHIFT_LENGTH * self.fs))
        ch_data = np.array(eeg_data)[:, INDEX_CHANNEL]
        self.eeg_buffer, filter_state = utils.update_buffer(self.eeg_buffer, ch_data, notch=True, filter_state=self.filter_state)

    def compute_band_power(self):
        """
        Compute band powers using the EEG data.
        """
        data_epoch = utils.get_last_data(self.eeg_buffer, EPOCH_LENGTH * self.fs)
        band_powers = utils.compute_band_powers(data_epoch, self.fs)
        #print (band_powers) 
        self.band_beta = utils.compute_beta(data_epoch, self.fs)
                
        band_alpha = utils.compute_alpha(data_epoch, self.fs)

    def compute_gyro_data(self):
        """
        Acquire and process gyroscope data to control the Tello drone.
        """
        gyro_data, timestamp = self.inlet_Gyro.pull_chunk(
        timeout=1, max_samples=int(SHIFT_LENGTH * self.fs_Gyro))
        
        theta = (gyro_data[-1][2] + gyro_data[-2][2] + gyro_data[-3][2] + gyro_data[-4][2] + gyro_data[-5][2]+ gyro_data[-6][2] + gyro_data[-7][2] + gyro_data[-8][2] + gyro_data[-9][2] + gyro_data[0][2]) * 1 / 10 #velocita in questo istante, media degli ultimi 2 valori, per giroscopio
    
        gamma = (gyro_data[-1][0] + gyro_data[-2][0] + gyro_data[-3][0] + gyro_data[-4][0] + gyro_data[-5][0]+ gyro_data[-6][0] + gyro_data[-7][0] + gyro_data[-8][0] + gyro_data[-9][0] + gyro_data[0][0]) * 1 / 10 #velocita in questo istante, media degli ultimi 2 valori, per giroscopio

        alpha = (gyro_data[-1][1] + gyro_data[-2][1] + gyro_data[-3][1] + gyro_data[-4][1] + gyro_data[-5][1]+ gyro_data[-6][1] + gyro_data[-7][1] + gyro_data[-8][1] + gyro_data[-9][1] + gyro_data[0][1]) * 1 / 10 #velocita in questo istante, media degli ultimi 2 valori, per giroscopio
        # print(theta, gamma, alpha)

        if self.GYROSCOPE_ACTIVATED == True:
            # print("vola")
            print("Rollio: " + str(gamma))
            print("Imbardata: " + str(theta))
            print("Beccheggio: " + str(alpha))
            
            if gamma > self.SX_GAMMA:
                self.droneCommandList.insert(0,20)  
            elif gamma < self.DX_GAMMA:
                self.droneCommandList.insert(0,-20)
            else:
                self.droneCommandList.insert(0,0)
            
            if theta > self.SX_THETA:
                self.droneCommandList.insert(1,self.ANGLE) 
            elif theta < self.DX_THETA:
                self.droneCommandList.insert(1,-(self.ANGLE)) 
            else:
                self.droneCommandList.insert(1,0) 
            
            if alpha > self.FW_ALPHA:
                self.droneCommandList.insert(3,20) 
            elif alpha < self.RW_ALPHA:
                self.droneCommandList.insert(3,-20) 
            else:
                self.droneCommandList.insert(3,0)


    def stop(self):
        self.stop_flag = True



