import tkinter as tk
import random

MAX_CIRCLES = 1
MIN_DISTANCE = 40  # Distanza minima tra i cerchi per evitare sovrapposizioni

# Lista per tenere traccia delle posizioni e dei raggi dei cerchi generati
circle_info = []
root = tk.Tk()

def generate_circles():
    for _ in range(MAX_CIRCLES):
        generate_circle()

def generate_circle(x = random.randint(10, root.winfo_width() - 10), y = random.randint(10, root.winfo_height() - 10), radius = random.randint(5, 30)):
    if len(circle_info) < MAX_CIRCLES:
        while True:
            
            color = random.choice(['red', 'green', 'blue', 'yellow', 'orange', 'purple'])

            # Controllo se il nuovo cerchio si sovrappone a un altro cerchio già presente
            overlapping = False
            for circle in circle_info:
                if distance(x, y, circle[0], circle[1]) < MIN_DISTANCE + radius + circle[2]: #aggiunto radius a MIN_DISTANCE
                    overlapping = True
                    break

            # Controllo se il nuovo cerchio esce dalla finestra
            if not overlapping and x - radius > 0 and y - radius > 0 and x + radius < root.winfo_width() and y + radius < root.winfo_height():
                canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color, tags='circle')
                canvas.tag_bind('circle', '<Button-1>', remove_circle)  # Associa la rimozione del cerchio al clic del mouse
                circle_info.append((x, y, radius)) #aggiunta delle info del cerchio alla lista circle_info
                break

def remove_circle(event):
    canvas.delete(tk.CURRENT)
    for i, circle in enumerate(circle_info):
        if canvas.find_withtag('circle') == ():
            circle_info.pop(i)  # Rimuove le informazioni del cerchio rimosso dalla lista circle_info
            generate_circle()

def distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5


root.attributes("-transparentcolor", "white")
root.attributes('-fullscreen', True)
root.update_idletasks()

canvas = tk.Canvas(root, bg='red', highlightthickness=0, bd=0)
canvas.pack(fill=tk.BOTH, expand=True)

generate_circles()

root.mainloop()
