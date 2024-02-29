import tkinter as tk
import random

MAX_CIRCLES = 3  # Maximum number of circles to generate
MIN_DISTANCE = 40  # Minimum distance between circles to avoid overlap
circle_info = []  # List to keep track of positions and radii of generated circles
global cont  # Global variable to keep track of the number of circles clicked and deleted
cont = 0  # Initial value for the number of circles clicked


def run():
    """
    Initializes and runs the tkinter application to display circles and perform actions like enlarging, shrinking, and moving circles.
    
    Args:
        None

    Returns:
        float: Mean of the filtered values.
    """
    root = tk.Tk()  # Create the root window
    root.lift()
    
    def generate_circles():  
        """
        Generates circles on the canvas up to the maximum limit defined by MAX_CIRCLES using the generate_circle function.
        """
        for _ in range(MAX_CIRCLES):
            generate_circle()


    def generate_circle(x=None, y=None, radius=None):  
        """
        Generates a circle on the canvas with random parameters if not specified.
        
        Args:
            x (int): x-coordinate of the center of the circle.
            y (int): y-coordinate of the center of the circle.
            radius (int): radius of the circle.

        Returns:
            None
        """
        
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
                overlapping = False
                
                for circle in circle_info: 
                    if distance(x, y, circle[0], circle[1]) < MIN_DISTANCE + radius + circle[2]:
                        overlapping = True
                        break
                
                if not overlapping:
                    circle_id = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill=color)
                    circle_info.append((x, y, radius, circle_id))  
                    break


    def enlarge_all_circles():  
        """
        Enlarges all circles by a fixed number of units and updates their information.
        """
        global circle_info
        for circle in circle_info:
            x, y, radius, circle_id = circle  
            new_radius = radius + 4  
            canvas.coords(circle_id, x - new_radius, y - new_radius, x + new_radius, y + new_radius)  
            if new_radius >= 30:  
                canvas.itemconfig(circle_id, fill='green')  
            circle_info[circle_info.index(circle)] = (x, y, new_radius, circle_id)  


    def shrink_all_circles():  
        """
        Shrinks all circles by a fixed number of units and updates their information.
        """
        global circle_info
        for circle in circle_info:
            x, y, radius, circle_id = circle  
            new_radius = max(radius - 4, 5)  
            canvas.coords(circle_id, x - new_radius, y - new_radius, x + new_radius, y + new_radius)  
            if new_radius < 30:  
                canvas.itemconfig(circle_id, fill='red')  
            circle_info[circle_info.index(circle)] = (x, y, new_radius, circle_id)  


    def move_circles_left():  
        """
        Moves all circles to the left by a fixed number of pixels and updates their information.
        """
        global circle_info
        for circle in circle_info:
            x, y, radius, circle_id = circle  
            canvas.move(circle_id, -5, 0)  
            x -= 5  
            circle_info[circle_info.index(circle)] = (x, y, radius, circle_id)  


    def move_circles_right():  
        """
        Moves all circles to the right by a fixed number of pixels and updates their information.
        """
        global circle_info
        for circle in circle_info:
            x, y, radius, circle_id = circle  
            canvas.move(circle_id, 5, 0)  
            x += 5  
            circle_info[circle_info.index(circle)] = (x, y, radius, circle_id)  


    def remove_circle(event):  
        """
        Removes a circle from the canvas when clicked.
        
        Args:
            event (tk.Event): Mouse event containing information about the click event.

        Returns:
            None
        """
        global cont
        global circle_info
        item_id = event.widget.find_closest(event.x, event.y)[0]  
        for circle in circle_info:
            if circle[3] == item_id:  
                if circle[2] >= 30:  
                    cont += 1  
                    write_circle_dimension(circle[2])  
                    canvas.delete(item_id)  
                    circle_info.remove(circle)  
                    generate_circle()  
                    if cont >= 6:  
                        root.destroy()  
                break


    def write_circle_dimension(radius):  
        """
        Writes the radius of the circle to a text file.
        
        Args:
            radius (int): Radius of the circle to be written to the text file.

        Returns:
            None
        """
        with open("circle_dimensions.txt", "a") as file:  
            file.write(f"{radius}\n")  


    def distance(x1, y1, x2, y2):  
        """
        Calculates the distance between two points in a 2D plane using the Euclidean distance formula.
        
        Args:
            x1 (int): x-coordinate of the first point.
            y1 (int): y-coordinate of the first point.
            x2 (int): x-coordinate of the second point.
            y2 (int): y-coordinate of the second point.

        Returns:
            float: Distance between the two points.
        """
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

    canvas.bind("<Button-1>", remove_circle)  

    root.mainloop() 
