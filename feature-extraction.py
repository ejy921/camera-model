# Simplify code of looking at surrounding pixels



import numpy as np
import matplotlib.pyplot as plt



########################################################
# SECTION 1: Plotting bitmap (manually for testing)
########################################################

binary = np.zeros((50, 50), dtype=np.uint8)
binary[4, 6:48] = 1
binary[4:48, 6] = 1

# decide end coords of coordinates
x1 = 12
y1 = 10
x2 = 35
y2 = 35



# Bresenham's algorithm to draw line onto 'array'
def bresenham(x1, x2, y1, y2):
    arr = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    stepx = 1 if x1 < x2 else -1
    stepy = 1 if y1 < y2 else -1
    error = dx - dy

    while True:
        arr.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        error2 = 2 * error
        if error2 > -dy:
            error -= dy
            x1 += stepx
        if error2 < dx:
            error += dx
            y1 += stepy        
        
    return arr
        
arr = bresenham(x1, x2, y1, y2)
# print(arr)

# Set new array coords as 1 in binary
for x, y in arr:
    binary[x, y] = 1

# Output of bitmap
plt.imshow(binary, cmap='gray', origin='lower')
plt.title('Binary Array Visualization')
plt.show()

########################################################
# SECTION 2: Detecting lines in bitmap
########################################################

x, y = np.where(binary == 1)
coords = np.column_stack((x, y))
# print(coords)

def find_origin(binary):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for x in range(binary.shape[0]-1):
        for y in range(binary.shape[1]-1, -1, -1):
            count = 0

            # If there are at least two pixels colored around a certain coordinate, then it is the origin
            for dy, dx in directions:
                ny, nx = y+dy, x+dx
                if 0 <= ny < binary.shape[0] and 0 <= nx < binary.shape[1]:
                    if binary[y, x] == 1 and binary[ny, nx] == 1:
                        count += 1
                if count >= 2:
                    origin = (x, binary.shape[0] - y)
                    return origin


origin = find_origin(binary)
print("Origin:")
print(origin)
# Equations of each axis
y_axis = (f"x = {origin[0]}")
x_axis = (f"y = {origin[1]}")
print("Y axis: " + y_axis + " (in bitmap)\nX axis: " + x_axis + " (in bitmap)")

# Coordinates making up each axis
y_axis_coords = []
for y in range(binary.shape[1]-1, -1, -1):
    if binary[y, origin[0]] == 1:
        y_axis_coords.append((origin[0], y))
x_axis_coords = []
for x in range(binary.shape[0]-1):
    if binary[origin[1], x] == 1:
        x_axis_coords.append((x, origin[1]))
print(x_axis_coords)

def find_line(binary):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    endpoints = []
    for x in range(binary.shape[0]-1):
        for y in range(binary.shape[1]-1, -1, -1):
            count = 0

            # If there are at least two pixels colored around a certain coordinate, then it is the origin
            for dy, dx in directions:
                ny, nx = y+dy, x+dx
                if 0 <= ny < binary.shape[0] and 0 <= nx < binary.shape[1]:
                    if binary[y, x] == 1 and binary[ny, nx] == 1:
                        count += 1
            if count == 1 and (x, y) not in y_axis_coords and (x, y) not in x_axis_coords:
                endpoints.append((x, y))
    
    return endpoints

endpoints = find_line(binary)
print(endpoints)

endpoint1 = endpoints[0]
endpoint2 = endpoints[1]

dy = abs(endpoint1[1] - endpoint2[1]) 
dx = abs(endpoint1[0] - endpoint2[0])
slope = dy / dx
print(slope) 
y-intercept = 
