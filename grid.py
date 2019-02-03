import numpy as np
import piece

WIDTH = 10
HEIGHT = 22

class Grid:

    def __init__(self):
        self.grid = np.zeros((HEIGHT, WIDTH))

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
            if len(np.where(row == 1)[0]) == WIDTH:
                lines += 1
        return lines
    
    def clear_lines(self):
        for index, row in enumerate(self.grid):
            if len(np.where(row == 1)[0]) == WIDTH:
                row.fill(0)
                self.grid = np.append(np.roll(self.grid[:index + 1, :], WIDTH), self.grid[index + 1:, :], axis=0)

    def column_height(self, column):
        """Finds the row of the topmost mino in a given column"""
        indices = np.where(self.grid[:, column] == 1)[0]
        return HEIGHT - indices[0] if indices.size != 0 else 0

    def aggregate_height(self):
        height = 0
        for column in range(WIDTH):
            height += self.column_height(column)
        return height

    def column_holes(self, column):
        column = self.grid[HEIGHT - self.column_height(column):HEIGHT, column]
        return column.size - np.count_nonzero(column)

    def holes(self):
        holes = 0
        for column in range(WIDTH):
            holes += self.column_holes(column)
        return holes

    def bumpiness(self):
        total = 0
        for column in range(WIDTH):
            next_height = 0
            if column < WIDTH - 1:
                next_height = self.column_height(column + 1)
            total += abs(self.column_height(column) - next_height)
        return total

    ## Simulation methods
    def drop(self, piece, origin, rotation):
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

        for _ in range(rotation):
            piece = np.rot90(piece)
            
        piece_height = piece.shape[0]
        piece_width = piece.shape[1]

        assert origin >= 0 and origin + piece_width <= WIDTH

        active_columns = []
        for i in range(len(piece[0])):
            active_columns.append(origin + i)

        smallest_drop = HEIGHT
        for piece_column, column in enumerate(active_columns):
            drop = HEIGHT - 1 - self.column_height(column) - np.where(piece[:, piece_column] == 1)[0][-1]
            if drop < smallest_drop:
                smallest_drop = drop

        top = smallest_drop
        bottom = smallest_drop + piece_height
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

if __name__ == "__main__":
    grid = Grid()
    print(grid)
    #grid.drop(piece.I, 1, 1)
    grid.clear_lines()
    print(grid)