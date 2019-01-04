import time
import numpy as np
from grid import Grid

class AI:
    """
    A simple Tetris AI designed to interact with a running emulator through the visual analysis and interpretation of the game.

    Attributes
    ----------
        vision (Vision): The vision instance used to see and interpret the game state
        controller (Controller): The controller instance used to send keystrokes to manipulate the game
        height_weight (float): Weight for aggregate height during heuristic claculation (negated)
        lines_weight (float): Weight for completed lines
        holes_weight (float): Weight for existing holes (negated)
        bumpiness_weight (float): Weight for bumpiness of the grid (negated)
    """

    def __init__(self, vision, controller, height_weight, lines_weight, holes_weight, bumpiness_weight, show_window=True):
        self.vision = vision
        self.controller = controller
        self.show_window = show_window
        self.playing = False
        
        # Optimal coefficents (weights) for score calulation
        self.height_weight = -height_weight
        self.lines_weight = lines_weight
        self.holes_weight = -holes_weight
        self.bumpiness_weight = -bumpiness_weight

        self.grid = Grid()
    
    def run(self):
        """Main game loop; play until told to stop"""
        while True:
            self.vision.refresh_frame()

            if self.show_window:
                self.vision.display_frame()
            
            print(self.vision.on_choose_level())

#            if not self.running and self.on_choose_level():
#                self.choose_level()

    def score(self):
        """Calculate the score of the current grid using the weighted summation of the heuristic variables"""
        return self.height_weight * self.grid.aggregate_height() + self.lines_weight * self.grid.lines() + self.holes_weight * self.grid.holes() + self.bumpiness_weight * self.grid.bumpiness()

    def best_move(self):
        """Determine the optimal move given a particular game state"""

        best_score = 0
        best_origin = 0
        best_rotation = 0
        for origin in range(10):
            for rotation in range(4):
                score = self.grid.simulate_drop(self.grid.current_piece, origin, rotation)
                if score > best_score:
                    best_score = score
                    best_origin = origin
                    best_rotation = rotation
        return (best_origin, best_rotation)
    
    ## Control functions
    def choose_level(self):
        self.controller.press_start()