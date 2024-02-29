from threading import Thread
import cv2


class VideoDrone(Thread):
    """
    A class representing a thread for streaming and displaying Tello drone video.

    Attributes:
    - tello (Tello): The Tello drone object.

    Methods:
    - run(): The main method that runs in the thread, continuously capturing and displaying video frames.
    """
    def __init__(self, tello):
        """
        Initializes the VideoDrone thread.

        Parameters:
        - tello (Tello): The Tello drone object to capture video from.
        """
        Thread.__init__(self)
        self.tello=tello
        self.stop_flag = False

    def run(self):
        """
        The main method that runs in the thread, continuously capturing and displaying video frames.
        """
        while not self.stop_flag:
            # Capture frame from the Tello drone
            frame = self.tello.get_frame_read().frame

            # Convert frame from RGB to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Display the frame
            cv2.imshow("Tello Stream", frame)

            # Check for 'q' key press to exit the loop
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        # Stop the video stream and close the OpenCV window
        self.tello.streamoff()
        cv2.destroyAllWindows()
        quit()
    def stop(self):
        self.stop_flag = True

# Usage example:
# Create a Tello drone object (assuming 'tello' is already instantiated)
# video_thread = VideoDrone(tello)
# video_thread.start()
# ... Perform other operations ...
# video_thread.join()  # Wait for the video thread to finish