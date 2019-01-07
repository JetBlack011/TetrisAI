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

            "T" : np.array([[0, 1, 0],
                            [1, 1, 1]]),

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

        self.previous_state = None
        self.current_piece = None
        self.next_piece = None

    def revert_state(self):
        self.grid = self.previous_state

    ## Methods to calculate heuristic variables of the field

    def lines(self):
        """Determines the number of completed lines on the grid"""
        lines = 0
        for row in self.grid:
            if len(np.where(row == 1)[0]) == 10:
                lines += 1
        return lines

    def column_height(self, column):
        """Finds the row of the topmost mino in a given column"""
        indices = np.where(self.grid[:, column] == 1)[0]
        return self.height - indices[0] if indices.size != 0 else 0

    def aggregate_height(self):
        height = 0
        for column in range(self.width):
            height += self.column_holes(column)
        return height

    def column_holes(self, column):
        column = self.grid[self.height - self.column_height(column):self.height, column]
        return column.size - np.count_nonzero(column)

    def holes(self):
        holes = 0
        for column in range(self.width):
            holes += self.column_holes(column)
        return holes
    
    def bumpiness(self):
        total = 0
        for column in range(self.width):
            next_height = 0
            if column < self.width - 1:
                next_height = self.column_height(column + 1)
            total += abs(self.column_height(column) - next_height)
        return total

    ## Simulation methods
    def drop(self, piece_str, origin, rotation):
        """Drop a given piece on the simulated grid at a sepcific column and rotation
        Parameters
        ----------
        piece : str
            Tetromino to drop
        origin : int
            Column at which to drop the given piece
        rotation : int
            How many times to rotate the piece clockwise
        """
        self.previous_state = self.grid.copy()

        piece = self.pieces[piece_str]
        for _ in range(rotation):
            piece = np.rot90(piece)
        piece_height = piece.shape[0]
        piece_width = piece.shape[1]

        if piece_str is "I":
            offset = 0 if piece_height == 1 else 3
        else:
            offset = 1 if piece_height < 3 else 2

        assert origin >= 0 and origin + piece_width < self.width

        active_columns = []
        for i in range(len(piece[0])):
            active_columns.append(origin + i)

        smallest_drop = 20
        for piece_column, column in enumerate(active_columns):
            lowest_block = np.where(piece[:, piece_column] == 1)[0][-1]
            height = self.height - self.column_height(column)
            drop = height - lowest_block + offset
            if drop < smallest_drop:
                smallest_drop = drop

        top = smallest_drop - piece_height
        bottom = smallest_drop
        left = origin
        right = origin + piece_width

        ones_location = []
        for row in range(top, bottom):
            for column in range(left, right):
                if self.grid[row][column] == 1:
                    ones_location.append((row, column))

        self.grid[top:bottom, left:right] = piece

        for point in ones_location:
            self.grid[point[0]][point[1]] = 1
        
    def __str__(self):
        return str(self.grid)
