import pyautogui
import numpy as np
from vision import Vision
from time import sleep
from grid import Grid

class AI:
    """
    A simple Tetris AI designed to interact with a running emulator through the visual analysis and
    interpretation of the game.

    Attributes
    ----------
        height_weight : float
            Weight for aggregate height during heuristic claculation (negated)
        lines_weight : float
            Weight for completed lines
        holes_weight : float
            Weight for existing holes (negated)
        bumpiness_weight : float
            Weight for bumpiness of the grid (negated)
    """
    def __init__(self, vision, controller, height_weight, lines_weight, holes_weight, bumpiness_weight, starting_level=0, show_window=False):
        self.vision = vision
        self.controller = controller

        # Optimal coefficents (weights) for score calulation
        self.height_weight = -height_weight
        self.lines_weight = lines_weight
        self.holes_weight = -holes_weight
        self.bumpiness_weight = -bumpiness_weight

        # Configurable options
        self.show_window = show_window
        self.starting_level = starting_level

        self.grid = Grid()

    def run(self):
        """Main game loop; play until told to stop"""

        self.controller.click_screen()
        self.controller.hold_down()
        sleep(5)
        self.controller.release_down()

        """
        self.update()
        #print("On Start: {}, On Game Type: {}, On Level: {}, Playing: {}".format(self.vision.on_start(), self.vision.on_choose_game_type(), self.vision.on_choose_level(), self.vision.on_playing()))
        
        #print("[+] Resetting field")
        #self.reset_field()

        while not self.vision.on_playing():
            self.update()             
            if self.vision.on_start():
                print("[+] Pressing start")
                self.controller.press_start()
            
            if self.vision.on_choose_game_type():
                print("[+] Choosing game type")
                self.controller.press_start()
            
            if self.vision.on_choose_level():
                print("[+] Choosing level " + str(self.starting_level))
                for _ in range(4):
                    self.controller.press_left()
                self.controller.press_up()
                self.controller.press_start()

        while self.vision.on_playing():
            self.update()

            if self.grid.current_piece == None:
                self.grid.current_piece = self.vision.current_piece()
            else:
                self.grid.current_piece = self.grid.next_piece()

            self.grid.next_piece = self.vision.next_piece()

            origin, rotation = self.best_move()

            print("Current Piece: {}, Next Piece: {}\nBest Origin: {}, Best Rotation: {}".format(self.grid.current_piece, self.grid.next_piece, origin, rotation))
            print(self.grid)

            for _ in range(10):
                self.controller.press_left()

            for _ in range(origin):
                self.controller.press_right()
            
            for _ in range(rotation):
                self.controller.rotate_ccw()
            
            while self.vision.next_piece() != None:
                self.controller.hold_down()
            while self.vision.next_piece() == None:
                self.controller.hold_down()

            self.controller.release_down()
            self.grid.drop(self.grid.current_piece, origin, rotation)
        """

                
    # def reset_field(self):
    #     while self.vision.on_playing():
    #         self.update()
    #         self.controller.hold_down()
    #         self.controller.press_start()
    #         self.controller.release_down()
                
    def score(self):
        """
        Calculate the score of the current grid using the
        weighted summation of the heuristic variables
        """
        return self.height_weight * self.grid.aggregate_height() + \
               self.lines_weight * self.grid.lines() + \
               self.holes_weight * self.grid.holes() + \
               self.bumpiness_weight * self.grid.bumpiness()

    def best_move(self):
        """Determine the optimal move given a particular game state"""
        piece = self.grid.current_piece

        best_score = -10
        best_origin = 0
        best_rotation = 0
        best_piece = None
        for rotation in range(5):
            _piece = self.grid.pieces[piece]
            for _ in range(rotation):
                _piece = np.rot90(_piece)
            for origin in range(self.grid.width - _piece.shape[1]):
                self.grid.drop(piece, origin, rotation)
                score = self.score()
                self.grid.revert_state()
                if score > best_score:
                    best_score = score
                    best_origin = origin
                    best_rotation = rotation
                    best_piece = piece

        return (best_origin, best_rotation)
    
    def update(self):
        self.vision.refresh_frame()

        if self.show_window:
            self.vision.display_frame()