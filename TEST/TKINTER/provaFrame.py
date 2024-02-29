import tkinter as tk
import random

MAX_CIRCLES = 3
MIN_DISTANCE = 40  # Distanza minima tra i cerchi per evitare sovrapposizioni
circle_info = []
global cont
cont = 0

def run():

    
    # Lista per tenere traccia delle posizioni e dei raggi dei cerchi generati
    root = tk.Tk()

    def generate_circles():
        for _ in range(MAX_CIRCLES):
            generate_circle()

    def generate_circle(x=None, y=None, radius=None):
        if x is None:
            x = random.randint(10, root.winfo_width() - 10)
        if y is None:
            y = random.randint(10, root.winfo_height() - 10)
        if radius is None:
            radius = random.randint(5, 30)
            
        if len(circle_info) < MAX_CIRCLES:
            while True:
                if radius >= 30:
                    color = 'green'
                else:
                    color = 'red'

                # Controllo se il nuovo cerchio si sovrappone a un altro cerchio già presente
                overlapping = False
                for circle in circle_info:
                    if distance(x, y, circle[0], circle[1]) < MIN_DISTANCE + radius + circle[2]:
                        overlapping = True
                        break

                # Controllo se il nuovo cerchio esce dalla finestra
                if not overlapping:
                    circle_id = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color)
                    circle_info.append((x, y, radius, circle_id)) #aggiunta delle info del cerchio alla lista circle_info
                    break

    def enlarge_all_circles():
        global circle_info
        for circle in circle_info:
            x, y, radius, circle_id = circle
            new_radius = radius + 4  # Aumenta il raggio di 4 unità
            canvas.coords(circle_id, x - new_radius, y - new_radius, x + new_radius, y + new_radius)  # Modifica le coordinate del cerchio per ingrandirlo
            if new_radius >= 30:
                canvas.itemconfig(circle_id, fill='green')  # Imposta il colore a verde
            circle_info[circle_info.index(circle)] = (x, y, new_radius, circle_id)

    def shrink_all_circles():
        global circle_info
        for circle in circle_info:
            x, y, radius, circle_id = circle
            new_radius = max(radius - 4, 5)  # Diminuisci il raggio di 4 unità, con il minimo raggio di 5
            canvas.coords(circle_id, x - new_radius, y - new_radius, x + new_radius, y + new_radius)  # Modifica le coordinate del cerchio per rimpicciolirlo
            if new_radius < 30:
                canvas.itemconfig(circle_id, fill='red')  # Imposta il colore a rosso se il raggio è inferiore a 30
            circle_info[circle_info.index(circle)] = (x, y, new_radius, circle_id)

    def move_circles_left():
        global circle_info
        for circle in circle_info:
            x, y, radius, circle_id = circle
            canvas.move(circle_id, -5, 0)  # Sposta il cerchio di -5 pixel in orizzontale
            x -= 5  # Aggiorna la posizione x
            circle_info[circle_info.index(circle)] = (x, y, radius, circle_id)

    def move_circles_right():
        global circle_info
        for circle in circle_info:
            x, y, radius, circle_id = circle
            canvas.move(circle_id, 5, 0)  # Sposta il cerchio di 5 pixel in orizzontale
            x += 5  # Aggiorna la posizione x
            circle_info[circle_info.index(circle)] = (x, y, radius, circle_id)

    def remove_circle(event):
        global cont
        global circle_info
        item_id = event.widget.find_closest(event.x, event.y)[0]
        for circle in circle_info:
            if circle[3] == item_id:  # Controlla se l'ID del cerchio corrisponde a quello cliccato
                if circle[2] >= 30:  # Verifica che il raggio sia maggiore o uguale a 30 (cerchio verde)
                    cont += 1
                    write_circle_dimension(circle[2])  # Scrivi le dimensioni del cerchio su un file
                    canvas.delete(item_id)  # Rimuovi il cerchio dalla canvas
                    circle_info.remove(circle)  # Rimuovi le informazioni del cerchio dalla lista
                    generate_circle()  # Genera un nuovo cerchio
                    if cont >= 10:  # Controlla se sono stati eliminati 5 cerchi
                        root.destroy()  # Chiudi la finestra
                break


    def write_circle_dimension(radius):
        with open("circle_dimensions.txt", "a") as file:
            file.write(f"{radius}\n")

    def distance(x1, y1, x2, y2):
        return ((x2 - x1)**2 + (y2 - y1)**2)**0.5


    
    root.bind('w', lambda event: enlarge_all_circles())
    root.bind('s', lambda event: shrink_all_circles())
    root.bind('d', lambda event: move_circles_left())
    root.bind('a', lambda event: move_circles_right())
    root.bind('W', lambda event: enlarge_all_circles())
    root.bind('S', lambda event: shrink_all_circles())
    root.bind('D', lambda event: move_circles_left())
    root.bind('A', lambda event: move_circles_right())

    root.attributes("-transparentcolor", "white")
    root.attributes('-fullscreen', True)
    root.update_idletasks()

    canvas = tk.Canvas(root, bg='white', highlightthickness=0, bd=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    generate_circles()

    canvas.bind("<Button-1>", remove_circle)  # Associa la funzione remove_circle all'evento di clic sinistro sulla canvas

    root.mainloop()
