import numpy as np
import grid

class Piece(np.ndarray):

    def __new__(cls, input_array, name, max_rotation):
        obj = np.asarray(input_array).view(cls)
        obj.name = name
        obj.max_rotation = max_rotation
        return obj
    
    def __array_finalize__(self, obj):
        if obj is None: return
        self.max_rotation = getattr(obj, 'max_rotation', None)
        self.name = getattr(obj, "name", None)
    
    def max_origin(self):
        return grid.WIDTH - self.shape[1]
    
    def start_location(self):
        return 3 if self.shape[1] == 4 else 4
    
    def __str__(self):
        return self.name

## Piece template constants
I = Piece([[1, 1, 1, 1]], "I", 1)

O = Piece([[1, 1],
           [1, 1]], "O", 0)

T = Piece([[1, 1, 1],
           [0, 1, 0]], "T", 3)

S = Piece([[0, 1, 1],
           [1, 1, 0]], "S", 1)

Z = Piece([[1, 1, 0],
           [0, 1, 1]], "Z", 1)

L = Piece([[1, 1, 1],
           [1, 0, 0]], "L", 3)

J = Piece([[1, 1, 1],
           [0, 0, 1]], "J", 3)

PIECE_SET = {"I": I, "O": O, "T": T, "S": S, "Z": Z, "L": L, "J": J}