#THREADS = 3  (Muse, Leap, EyeTracker)

from threading import Thread
import time
import queue


def MuseFunction(result_queue, cont0):
    #cont=0
    while True:
    #for i in range(4):
        print("Muse Function\n")
        time.sleep(1)
        result_queue.put(("Muse",cont0))
        cont0+=1
        

    
def LeapFunction(result_queue, cont1):
    #cont=100
    while True: 
    #for i in range(4):
        print("Leap Function\n")
        time.sleep(1)
        result_queue.put(("Leap",cont1))
        cont1+=1
    
def EyeTrackerFunction(result_queue, cont2):#result_queue
    #cont=1000
    while True:
    #for i in range(4):
        print("EyeTracker Function\n")
        time.sleep(1)
        result_queue.put(("Eye",cont2))
        cont2+=1



def main():
    
    cont0=0
    cont1=100
    cont2=1000
    
    result_queue = queue.Queue()
    
    tMuse = Thread(target=MuseFunction, args=(result_queue , cont0)) #args=(result_queue,)
    tLeap = Thread(target=LeapFunction, args=(result_queue , cont1))
    tEye = Thread(target=EyeTrackerFunction, args=(result_queue , cont2))

    tMuse.start()
    tLeap.start()
    tEye.start()
    
    #tMuse.join()
    #tLeap.join()
    #tEye.join()
    
    while True:  # Ciclo infinito per continuare a leggere dalla coda
        try:
            result = result_queue.get(timeout=1)  # timeout = 1 secondo per controllare la coda
            print(result)
        except queue.Empty:  # Se la coda è vuota
            pass


if __name__ == "__main__":
    main()