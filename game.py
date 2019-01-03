import time
import numpy as np

class Grid:

    def __init__(self, height_weight, lines_weight, holes_weight, bumpiness_weight):
        self.grid = np.zeros(20, 10)
        self.virtual_grid = self.grid

        self.pieces = {
            "I" : [[1, 1, 1, 1],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]],

            "O" : [[1, 1],
                [1, 1]],

            "S" : [[0, 1, 1],
                [1, 1, 0]],

            "Z" : [[1, 1, 0],
                [0, 1, 1]],

            "L" : [[1, 0],
                [1, 0],
                [1, 1]],

            "L" : [[0, 1],
                [0, 1],
                [1, 1]]
        }

        self.current_piece = None
        self.next_piece = None

        # Optimal coefficents (weights) for score calulation
        self.height_weight = -height_weight
        self.lines_weight = lines_weight
        self.holes_weight = -holes_weight
        self.bumpiness_weight = -bumpiness_weight

    def zeros(self, column):
        spaces = 0
        while self.grid[spaces][column] == 0:
            spaces += 1
        return spaces

    def height(self, column):
        return len(self.grid) - self.zeros(column)

    def holes(self, column):
        column = self.grid[:,column][self.zeros(column)]
        return len(column) - np.count_nonzero(column)

    ## Calculate heuristic variables of the field
    def aggregate_height(self):
        total = 0
        
    def score(self):
        return self.height_weight * self.aggregate_height() + self.lines_weight * self.lines() + self.holes_weight * self.holes() + self.bumpiness_weight * self.bumpiness()

    def __simulate_drop(self, piece, origin, rotation):
        assert (origin > 0 and origin < 10) or (piece == self.pieces["I"] and origin > 1 and origin < 10)
        
        piece = np.copy(piece)
        for _ in range(rotation):
            piece = np.rot90(piece)

        active_rows = [2, 3, 4]
        smallest_drop = 0
        for row in active_rows:
            self.height()

    def __best_move(self):
        best_score    = 0
        best_origin   = 0
        best_rotation = 0
        for origin in range(10):
            for rotation in range(4):
                score = self.__simulate_drop(self.current_piece, origin, rotation)
                if score > best_score:
                    best_score    = score
                    best_origin   = origin
                    best_rotation = rotation
        return (best_origin, best_rotation)
            
        
    def update(self):
        self

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