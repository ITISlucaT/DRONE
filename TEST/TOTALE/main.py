import provaFrame as pf  # Importing provaFrame module as pf
import report as r
import os
from datetime import datetime
from threading import Thread
import webbrowser
import time




class ResultThread(Thread):
    def __init__(self):
        super(ResultThread, self).__init__()
        self.listMuseResult = ['0.1', '0.2', '0.3', '0.4', '0.5']
    def run(self):
        # Check if the file exists
        if os.path.exists("circle_dimensions.txt"):
            os.remove("circle_dimensions.txt") # Remove the file if it exists

        startTime = datetime.now().replace(microsecond=0)

        pf.run()  # Run the function from provaFrame module

        finishTime = datetime.now().replace(microsecond=0)

        deltaTime = finishTime - startTime
        r.createReport(deltaTime, self.listMuseResult)
        time.sleep(1) 
        
        
        
# t1 = ResultThread()
# t1.start()
# t1.join()
