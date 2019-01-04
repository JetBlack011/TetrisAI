import numpy as np

class Grid:

    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height

        self.grid = np.zeros((self.height, self.width))

        self.pieces = {
            "I" : np.array([[1, 1, 1, 1]]),

            "O" : np.array([[1, 1],
                            [1, 1]]),

            "S" : np.array([[0, 1, 1],
                            [1, 1, 0]]),

            "Z" : np.array([[1, 1, 0],
                            [0, 1, 1]]),

            "L" : np.array([[1, 0],
                            [1, 0],
                            [1, 1]]),

            "J" : np.array([[0, 1],
                            [0, 1],
                            [1, 1]])
        }

        self.current_piece = None
        self.next_piece = None

    ## Methods to calculate heuristic variables of the field

    def lines(self):
        """Determines the number of completed lines on the grid"""
        completed_lines = 0
        for row in self.grid:
            if len(np.where(row == 1)[0]) == 10:
                completed_lines += 1
        return completed_lines

    def column_height(self, column):
        """Finds the row of the topmost mino in a given column"""

        indices = np.where(self.grid[:, column] == 1)[0]
        return indices[0] if len(indices) > 0 else 0

    def aggregate_height(self):
        return np.sum(np.apply_along_axis(self.column_height, 1, self.grid))

    def column_holes(self, column):
        column = self.grid[:,column][self.zeros(column)]
        return len(column) - np.count_nonzero(column)

    def holes(self):
        return np.sum(np.apply_along_axis(self.column_holes, 1, self.grid))

    ## Simulation methods
    def simulate_drop(self, piece, origin, rotation):
        """Drop a given piece on the simulated grid at a sepcific column and rotation
        Parameters
        ----------
        piece : ndarray(dtype=int, ndim=2)
            Array representing a tetromino
        origin : int
            Column at which to drop the given piece
        rotation : int
            How many times to rotate the piece clockwise
        """
        piece = self.pieces[piece]
        for _ in range(rotation):
            piece = np.rot90(piece)
        piece_height = piece.shape[0]
        piece_width = piece.shape[1]

        assert origin >= 0 and origin + piece_width < self.width
        
        active_columns = []
        for i in range(len(piece[0])):
            active_columns.append(origin + i)

        smallest_drop = 20
        for column in active_columns:
            drop = self.column_height(column) - piece_height + 1
            if drop < smallest_drop:
                smallest_drop = drop

        self.grid[smallest_drop:piece_height, origin:piece_width] = piece

        return self.grid
    
    def __str__(self):
        return str(self.grid)