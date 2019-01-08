import time
import pyautogui
import numpy as np
from vision import Vision
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
    def __init__(self, vision, controller, height_weight, lines_weight, holes_weight, bumpiness_weight, starting_level=0):
        self.vision = vision
        self.controller = controller

        # Optimal coefficents (weights) for score calulation
        self.height_weight = -height_weight
        self.lines_weight = lines_weight
        self.holes_weight = -holes_weight
        self.bumpiness_weight = -bumpiness_weight

        # Configurable game options
        self.starting_level = starting_level

        self.grid = Grid()

    def run(self):
        """Main game loop; play until told to stop"""

        self.controller.click_screen()

        if self.vision.on_playing():
            print("[+] Resetting game")
            self.reset_game()
        
        self.vision.update()
        
        if self.vision.on_game_over():
            print("[+] Game over! Restarting...")
            self.controller.press_start()
            time.sleep(1)

        self.vision.update()

        while not self.vision.on_playing():
            self.vision.update()
            if self.vision.on_start():
                print("[+] Pressing start")
                self.controller.press_start()
            
            if self.vision.on_choose_game_type():
                print("[+] Choosing game type")
                self.controller.press_start()
            
            if self.vision.on_choose_level():
                print("[+] Choosing level " + str(self.starting_level))
                for _ in range(9):
                    self.controller.press_left()
                for _ in range(self.starting_level):
                    self.controller.press_right()
                self.controller.press_start()

        while self.vision.on_playing():
            self.vision.update()

            if self.grid.current_piece == None:
                self.grid.current_piece = self.vision.current_piece()
            else:
                self.grid.current_piece = self.grid.next_piece

            self.grid.next_piece = self.vision.next_piece()

            origin, rotation = self.best_move()
            
            for _ in range(rotation):
                self.controller.rotate_ccw()
                
            location = self.grid.get_piece_start(rotation)

            if origin <= location:
                for _ in range(abs(location - origin)):
                    self.controller.press_left()
                    print("Left")
            else:
                for _ in range(abs(location - origin) + 1):
                    self.controller.press_right()
                    print("Right")
            
            self.vision.update_stats()
            while not self.vision.is_block_down():
                self.controller.hold_down()
            self.controller.release_down()

            self.grid.drop(self.grid.current_piece, origin, rotation)
            print(self.grid)
            print("Current Piece: {}, Next Piece: {}\nBest Origin: {}, Best Rotation: {}".format(self.grid.current_piece, self.grid.next_piece, origin, rotation))
            print("Location: {}".format(location))

    def drop_block(self):
        start = time.time()
        elapsed_time = 0
        self.vision.update_stats()
        self.controller.release_down()
        while not self.vision.is_block_down() and elapsed_time < 3:
            self.controller.hold_down()
            elapsed_time = time.time() - start
        self.controller.release_down()

    def reset_game(self):
        while not self.vision.on_game_over():
            self.controller.rotate_cw()
            self.drop_block()
            self.vision.update()
                
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

        best_score = -1000000
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