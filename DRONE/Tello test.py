from djitellopy import Tello
import time

def main():
    # Inizializza il drone Tello
    tello = Tello()
    
    try:
        # Connessione al drone
        tello.connect()
        
        while True:
            # Legge il comando da terminale
            command = input("Inserisci un comando ('t' per decollare, 'l' per atterrare, 'x' per uscire): ")
            
            # Esegue il comando
            if command == 't':  # Decolla
                print("ciao")
                tello.takeoff()
                
            elif command == 'l'or command=='x':  # Atterra
                tello.land()
                break  # Esci dal loop quando atterra
            
            # Controlli di movimento del drone
            if command in ['w', 's', 'a', 'd', 'e', 'q']:
                # Movimenti relativi
                distance = 30
                if command == 'w':  # Avanti
                    tello.move_forward(distance)
                elif command == 's':  # Indietro
                    tello.move_back(distance)
                elif command == 'a':  # Sinistra
                    tello.move_left(distance)
                elif command == 'd':  # Destra
                    tello.move_right(distance)
                elif command == 'e':  # Salita
                    tello.move_up(distance)
                elif command == 'q':  # Discesa
                    tello.move_down(distance)
    
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    main()
