import numpy as np



def mat2tikz(M):
    for r in range(M.shape[0]):
        for c in range(M.shape[1]):
            print("%d/%d/black!%d/%d, " %(r+1, c+1, int(0.3*abs(100-100*abs(M[r, c])/255)),  M[r, c]))

def gradx(M):
    g_x = np.zeros(M.shape, np.int32)
    for r in range(1, M.shape[0]-1):
        for c in range(1, M.shape[1]-1):
            g_x[r, c] = M[r, c+1] - M[r, c-1] 
    return g_x

def grady(M):
    g_y = np.zeros(M.shape, np.int32)
    for r in range(1, M.shape[0]-1):
        for c in range(1, M.shape[1]-1):
            g_y[r, c] = M[r+1, c] - M[r-1, c]
    return g_y

M = np.zeros((8, 8), np.int32)
M[:2, :] = 10
M[3:, 3:] = 30
M[5:, 2:] = 30
M[4:, 4:] = 40

M1 = M.copy()
M2 = M.copy()
M1[2:6, 2:6] = 150
M2[1:5, 1:5] = 150


print(M2)
print()
mat2tikz(M2 - M1)
