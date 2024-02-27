from pynput.mouse import Controller

# Inizializza il controller del mouse
mouse = Controller()

# Ottieni le coordinate attuali del cursore
x, y = mouse.position

print(f"Coordinate del cursore: x = {x}, y = {y}")
