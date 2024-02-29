"""
This script defines a ResultThread class that runs a circles game, records the time it takes to run,
and creates a report based on the results.

Classes:
    - ResultThread: A threading class that runs the circles game and generates a report.

Usage:
    To use this script, import the ResultThread class from circlesGameRunner and create an instance.

Example:
    from circlesGameRunner import ResultThread

    t1 = ResultThread()
    t1.start()
    t1.join()

Date: 29/02/2023
"""

import circlesGame as cg 
import report as r
import os
from datetime import datetime
from threading import Thread
import time




class ResultThread(Thread):
    
    """
    A class representing a ResultThread class that runs a circles game, records the time it takes to run,
    and creates a report based on the results.


    Methods:
    - run(): The main method that runs in the thread runs the circles game and generates a report.
    """

    def __init__(self):
        """
        Constructor for ResultThread class.

        Initializes the ResultThread with a list of Muse results.

        Attributes:
            listMuseResult (list): A list of Muse results.

        Returns:
            None
        """
        super(ResultThread, self).__init__()
        self.listMuseResult = ['0.1', '0.2', '0.3', '0.4', '0.5']
    def run(self):
        """
        Run method of the ResultThread class.

        Executes the circles game, records the time it takes to run, and creates a report.

        Returns:
            None
        """
        # Check if the file exists
        if os.path.exists("circle_dimensions.txt"):
            os.remove("circle_dimensions.txt") # Remove the file if it exists

        startTime = datetime.now().replace(microsecond=0)

        cg.run()  # Run the function from provaFrame module

        finishTime = datetime.now().replace(microsecond=0)

        deltaTime = finishTime - startTime
        r.createReport(deltaTime, self.listMuseResult)
        time.sleep(1) 