
from threading import Thread
from pylsl import StreamInlet, resolve_byprop
import utils
import numpy as np 

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
        self.SX_GAMMA = 1.5
        self.DX_GAMMA = -1.5
        self.SX_THETA = 3
        self.DX_THETA = -3
        self.FW_ALPHA = 1.5
        self.RW_ALPHA = -1.5
        self.ANGLE = 90
        self.HEIGHT = 20
        self.FORWARD = 20
        self.prec = 0
        self.vertical_position=20
        self.stop_flag = False
    def run(self):
        """
        Run the MuseThread to process EEG and gyroscope data, and control the Tello drone accordingly.
        """
        global command
        self.initialize_eeg_stream()
        self.initialize_buffer()
        try:
            while not self.stop_flag:
                self.acquire_data()
                self.compute_band_power()
                self.compute_gyro_data()
                command = np.mean(self.band_beta)

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

        global GYROSCOPE_ACTIVATED


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
        
        theta = 0.2 * (gyro_data[-1][2] + gyro_data[-2][2] + gyro_data[-3][2] + gyro_data[-4][2] + gyro_data[-5][2]) * 1 / self.fs_Gyro #velocita in questo istante, media degli ultimi 2 valori, per giroscopio
        
        gamma = 0.2 * (gyro_data[-1][0] + gyro_data[-2][0] + gyro_data[-3][0] + gyro_data[-4][0] + gyro_data[-5][0]) * 1 / self.fs_Gyro

        alpha = 0.2 * (gyro_data[-1][1] + gyro_data[-2][1] + gyro_data[-3][1] + gyro_data[-4][1] + gyro_data[-5][1]) * 1 / self.fs_Gyro
        print(theta, gamma, alpha)

        if GYROSCOPE_ACTIVATED == True:
            print("vola")
            if gamma > self.SX_GAMMA:
                self.tello.move_right(20)
                self.vertical_position += self.HEIGHT
            elif gamma < self.DX_GAMMA:
                if self.vertical_position > self.HEIGHT:
                    self.tello.move_left(20)
                    self.vertical_position -= self.HEIGHT
            
            #Rotation
            if self.prec > self.DX_THETA and self.prec < self.SX_THETA:
                if theta > self.SX_THETA:
                    self.tello.rotate_counter_clockwise(self.ANGLE)
                    self.time.sleep(2)
                elif theta < self.DX_THETA:
                    self.tello.rotate_counter_clockwise(-(self.ANGLE))
                    self.time.sleep(2)
            self.prec = theta
            
            #FW and BW
            if alpha > self.FW_ALPHA:
                self.tello.move_forward(self.FORWARD)
            elif alpha < self.RW_ALPHA:
                self.tello.move_back(self.FORWARD)
    def stop(self):
        self.stop_flag = True



