# PROJECT AND GROUP PRESENTATION

The project we developed is designed to offer an engaging and therapeutic experience for people with ALS (Amyotrophic Lateral Sclerosis), allowing them to explore an open space using a drone. Drone control is achieved through the Muse 2 sensor, while interaction with the environment is facilitated by circles appearing on the screen, which are selected by clicking. To further enhance the experience and make rehabilitation activities more interactive, we integrated the Leap Motion sensor, which reads the user's hand movements to control the pointer on the screen.
This approach not only provides an opportunity for patients to actively participate in outdoor activities but also has a positive impact on enhancing cognitive functions, particularly the ability to manage simultaneous tasks. For example, the concentration value read by the Muse 2 sensor during drone control can be correlated with the accuracy and timeliness of clicking on the circles on the screen, providing immediate and personalized feedback to the patient.

The program aims not only to improve cognitive and motor skills but also to provide a therapeutic experience that promotes overall well-being and quality of life for patients with ALS.

Additionally, at the end of the session, an HTML file is generated, which explains the parameters recorded during the session. This file can be interpreted by the therapist to indicate possible improvements or deteriorations.

Overall, the project not only offers an interactive and therapeutic experience but also provides useful tools for monitoring and evaluating the progress of rehabilitation over time.

Our group is composed of five members: Luca Torelli, Eugenio Armando, Lorenzo Martino, Pietro Giordano and Francesco Re. 

At first we choose the leader, Luca Torelli, and then we divided various tasks:
* Luca Torelli and Eugenio Armando have studied the functionality of the Muse, interpreting the sampled values, and subsequently integrated it with the drone to enable spatial movement using the Muse-provided oscilloscope.
* Lorenzo Martino and Francesco Re have developed the code to create circles on the screen and the interface to resize them, move them in space, or make them clickable and subsequently removable. Additionally, they have been responsible for creating the final user report and interpreting all the data provided by all the programs.
* Pietro Giordano took charge of crafting the comprehensive PowerPoint presentation of the entire project.

# INSTRUCTION FOR USE
* In order to use the Muse2, you have to:
  * click on this link and download all the folder: https://github.com/kowalej/BlueMuse , then must unzip this folder: https://github.com/kowalej/BlueMuse/blob/master/DistArchived/BlueMuse_2.0.0.0.zip, and follow his tutorial
  * Then you have to switch on the bluetooth on your pc and start the software of BlueMuse and click on "Start Streaming" and the Muse2 will start to record data.
* To use Tello, you have to connect your device to Tello's wifi.
* In order to use the Leap Motion sensor, you have to:
  * click on this link and download https://leap2.ultraleap.com/ultraleap-widgets/ and also https://leap2.ultraleap.com/gemini-downloads/ (download only in the Desktop/Laptop Computers section), from the official website of the leap motion
  * than you must start the ultraleap widgets app on your pc and use the pointer widget

# LIBRARIES TO DOWNLOAD

Not all the libraries used from our project are directly involved in python, these are:  pysls, numpy, tkinter, random, scipy, djitellopy, opencv-python, matplotlib and sklearn.
So you have to download them writing in the terminal:
* `pip install pysls`, in order to install pysls a library for DJI drone control.
  
* `pip install numpy`, in order to install numpy a fundamental library for array manipulation and scientific computing in Python.
  
* `pip install scipy`, in order to install scipy a library for data processing and analysis in scientific computing.
  
* `pip install djitellopy`, in order to install djitellopy a library for controlling the DJI Tello drone
  
* `pip install opencv-python`, in order to install opencv-python a library for computer vision and image recognition.
  
* `pip install scikit-learn`, in order to install scikit-learn a library for machine learning and data analysis.
  
* `pip install matplotlib`, in order to install matplotlib a library for creating graphs and data visualizations in Python.

# EXECUTION

You must connect with the usb the Leap Motion tracker and use the pointer widget from the ultraleap widgets app, than you must connect the Muse2 via Bluetooth using his own program and than you must connect the drone via Wifi.

After, you have to run `TEST/TOTALE/main.py` in the terminal, and wait that the process starts. 

**!!NOTE:** Remember to focus on the wondow that generates the circles.
