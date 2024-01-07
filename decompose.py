import numpy as np
""" Nota bene : il seguente non è stato debuggato neppure tanto meno ottimizzato, manca la parte di automatizzazione del processo di calcolo dei termini. 
Non è stato eseguito nessun controllo sull'efficacia dell'algoritmo... bisogna fidarsi :) """
def find_largest_submatrix(matrix):
    nrows, ncols = matrix.shape
    max_area = 0
    max_pos = (0, 0)
    max_size = (0, 0)

    for r in range(nrows):
        for c in range(ncols):
            if matrix[r, c] > 0:
                for h in range(1, nrows - r + 1):
                    for w in range(1, ncols - c + 1):
                        if can_subtract(matrix, r, c, h, w):
                            area = h * w
                            if area > max_area:
                                max_area = area
                                max_pos = (r, c)
                                max_size = (h, w)
    return max_pos[0], max_pos[1], max_size[0], max_size[1]

def can_subtract(matrix, row, col, height, width):
    for r in range(row, row + height):
        for c in range(col, col + width):
            if matrix[r, c] < 1:
                return False
    return True

def subtract_submatrix(copymatrix, row, col, height, width):
    for r in range(row, row + height):
        for c in range(col, col + width):
            copymatrix[r, c] -= 1

def create_submatrix(height, width):
    return np.ones((height, width), dtype=int)

def decompose_matrix(matrix):
    copymatrix = np.copy(matrix)
    decompositions = []
    momenta = []
    while np.any(copymatrix > 0):
        row, col, height, width = find_largest_submatrix(copymatrix)
        if height == 0 or width == 0:
            break
        subtract_submatrix(copymatrix, row, col, height, width)
        decompositions.append((row, col, height, width))
        momenta.append( [(height-1)/2 , (width-1)/2])
    return momenta

def print_submatrix(row, col, height, width):
    submatrix = create_submatrix(height, width)
    
    print(submatrix)
    
    print()

    return [(height-1)/2 , (width-1)/2]
