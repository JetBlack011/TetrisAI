import numpy as np 
import time

class VirtualGrid:

    def __init__(self):
        self.grid = np.zeroes(20, 10)

        self.aggregateHeight = 0
        self.completeLines = 0
        self.holes = 0
        self.bumpiness = 0
    
    def clear_lines:
        for row in grid:
            if (row == 1).all():
                row.fill(0)
                grid[:row]

class Grid:

    def __init__(self):

    def update(self):

class Game:

    def __init__(self, vision, controller, show_window=True):
        self.vision = vision
        self.controller = controller
        self.show_window = show_window
        self.running = False
    
    def run(self):
        while True:
            self.vision.refresh_frame()

            if self.show_window:
                self.vision.display_frame()
            
            print(self.on_choose_level())

#            if not self.running and self.on_choose_level():
#                self.choose_level()
    
    def can_see_object(self, template, threshold=0.9):
        matches = self.vision.find_template(template, threshold=threshold)
        return np.shape(matches)[1] >= 1
    
    ## On Event functions
    def on_choose_level(self):
        return self.can_see_object("level")
    
    ## Control functions
    def choose_level(self):
        self.controller.press_start()