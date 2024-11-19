# location.py
import random

class Location:
    def __init__(self, x, y, depot=False):
        self.id = str(random.random())
        self.x = x
        self.y = y
        self.depot = depot
    
    def draw_location(self, canvas, color="white"):
        # Canvas location
        radius = 7 if self.depot else 5
        fill_color = "black" if self.depot else color
        x, y = self.x * 20, self.y * 20
        canvas.create_oval(
            x - radius, y - radius, 
            x + radius, y + radius, 
            fill=fill_color,
            outline="black" if color == "white" else fill_color
        )
        return (x, y)
