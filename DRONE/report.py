import numpy as np
from scipy.stats import iqr
from datetime import datetime
import time


def mediaValori(listValuesStr):
    """
    Calculates the mean of the values in the list after converting them to float.

    Args:
        listValuesStr (list): List of strings representing numerical values.
    """
    
    listValues = [float(stringa) for stringa in listValuesStr]
    print(listValues)
    
    moltiplicatore = 0.1
    misurazioni = np.array(listValues)
    q1 = np.percentile(misurazioni, 15) 
    q3 = np.percentile(misurazioni, 85) 

    iqr_value = q3 - q1

    soglia_inf = q1 - moltiplicatore * iqr_value 
    soglia_sup = q3 + moltiplicatore * iqr_value

    misurazioni_filtrate = misurazioni[(misurazioni >= soglia_inf) & (misurazioni <= soglia_sup)]

    return np.mean(misurazioni_filtrate)


def scriviHtml(listaLeap, mediaLeap, listaMuse, mediaMuse, deltaT):
    """
    Generates an HTML file with the results obtained from the LEAP and Muse devices along with the session time.

    Args:
        listaLeap (list): List of values obtained from the LEAP device.
        mediaLeap (float): Mean of the values from the LEAP device.
        listaMuse (list): List of values obtained from the Muse device.
        mediaMuse (float): Mean of the values from the Muse device.
        deltaT (datetime.timedelta): Time difference between the start and end of the session.
    """
    
    
    media_arrotondataLeap = "{:.1f}".format(mediaLeap)
    media_arrotondataMuse = "{:.1f}".format(mediaMuse)

    with open("output.html", "w") as file:
        
        file.write("<html>\n<head>\n<title>USER REPORT</title>\n")
        
        file.write("<style>\n")
        file.write("body {\nbackground-color: #025052;\ncolor: white;\n}\n")
        file.write("table {\nborder-collapse: collapse;\nwidth: 50%;\nmargin: 0 auto;\nbackground-color: #237b7d;\n}\n") 
        file.write("th, td {\npadding: 8px;\ntext-align: center;\n}\n")
        file.write("th {\nbackground-color: #c1d8d9;\ncolor: black;\n}\n")
        file.write(".title {\nfont-size: 24px;\ntext-align: center;\npadding: 20px 0;\n}\n")
        file.write("p {\npadding: 8px;\ntext-align: center;\n}\n")
        file.write("</style>\n")
        
        file.write("</head>\n<body>\n")
        
        file.write("<div class='title'>USER REPORT</div>\n")
        
        file.write("""<p>The session with the LEAP involves an interactive game, where the goal is to click precisely on virtual obstacles.</p>\n
                   <p>The minimum size for an obstacle to become clickable is when its radius is greater than or equal to 30.</p>\n""")

        file.write("<table>\n<tr><th>Your results with LEAP</th></tr>\n")
        
        for valore in listaLeap:
            
            file.write("<tr><td>{}</td></tr>\n".format(valore))
        
        file.write("<tr><th>The weighted average is</th></tr>\n")
        file.write("<tr><td>{}      -   OTTIMO!!</td></tr>\n".format(media_arrotondataLeap))
        file.write("</table>\n")

        file.write("<br>")
        file.write("<br>")
        file.write("<br>")
        
        file.write("""<p>The session with the Muse involves interacting with a drone, where the goal is to remain focused to keep the drone flying.</p>\n
                   <p>The concentration detector considers a person concentrated when the detected value is less than 0.8.</p>\n""")
        file.write("<table>\n<tr><th>Your results with MUSE</th></tr>\n")
        
        for valore in listaMuse:
            
            file.write("<tr><td>{}</td></tr>\n".format(valore))
        
        file.write("<tr><th>The weighted average is</th></tr>\n")
        file.write("<tr><td>{}      -   MOLTO BUONO!!</td></tr>\n".format(media_arrotondataMuse))
        file.write("</table>\n")
        
        file.write("<br>")
        file.write("<br>")
        file.write("<br>")
        
        file.write("<table>\n<tr><th>The session time is : {}</th></tr>\n".format(deltaT))
        file.write("</body>\n</html>")


def leggiFile(fileOpen):
    """
    Reads numerical values from a file and returns a list of floats.

    Args:
        fileOpen (str): Path of the file to read values from.

    Returns:
        list: List of numerical values read from the file.
    """
    
    with open(fileOpen, 'r') as file:
        
        valori = file.readlines()

    valori = [valore.strip() for valore in valori]

    print(valori)

    with open(fileOpen, 'r') as file:
         
        valori = file.readlines()

    valori_numerici = [float(valore.strip()) for valore in valori]
    
    return valori_numerici


def createReport(deltaTime, listaMuse):
    """
    Creates an HTML report with the results obtained from the LEAP and Muse devices, along with the session time.

    Args:
        deltaTime (datetime.timedelta): Time difference between the start and end of the session.
    """
    
    listaLeap = leggiFile('circle_dimensions.txt')
    
    mediaLeap = mediaValori(listaLeap)
    mediaMuse = mediaValori(listaMuse)
    
    scriviHtml(listaLeap, mediaLeap, listaMuse, mediaMuse, deltaTime)
    print("html creato")
    
