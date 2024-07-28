# Simplify code of looking at surrounding pixels



import numpy as np
import matplotlib.pyplot as plt



########################################################
# SECTION 1: Plotting bitmap (manually for testing)
########################################################

# Initialize bitmap with x,y-axis
binary = np.zeros((50, 50), dtype=np.uint8)
binary[4, 6:48] = 1
binary[4:48, 6] = 1

# End coords of line1: (x1, y1, x2, y2)
line1_coords = [14, 12, 37, 37]

# End coords of line2: (x1, y1, x2, y2)
line2_coords = [14, 37, 37, 12]


# Bresenham's algorithm to draw line onto 'array'
def bresenham(line_coords):
    x1 = line_coords[0]
    y1 = line_coords[1]
    x2 = line_coords[2]
    y2 = line_coords[3]

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
        
l1_coords = bresenham(line1_coords)
l2_coords = bresenham(line2_coords)

# Set new coords as 1 in numpy array
def set_new_coords(binary, coords):
    for x, y in coords:
        binary[x, y] = 1

set_new_coords(binary, l1_coords)
set_new_coords(binary, l2_coords)


# Output of bitmap
plt.imshow(binary, cmap='gray', origin='lower')
plt.title('Binary Array Visualization')
plt.show()




########################################################
# SECTION 2: Detecting lines in bitmap
########################################################

# Obtain all coordinates of colored pixels
x, y = np.where(binary == 1)
coords = np.column_stack((x, y))
# print(coords)

# Global variable directions for looking at surrounding pixels
directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# Find origin of Cartesian graph
def find_origin(binary):

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
# print("Origin:")
# print(origin)
# Equations of each axis
y_axis = (f"x = {origin[0]}")
x_axis = (f"y = {origin[1]}")
# print("Y axis: " + y_axis + " (in bitmap)\nX axis: " + x_axis + " (in bitmap)")

# Coordinates making up each axis
y_axis_coords = []
for y in range(binary.shape[1]-1, -1, -1):
    if binary[y, origin[0]] == 1:
        y_axis_coords.append((origin[0], y))
x_axis_coords = []
for x in range(binary.shape[0]-1):
    if binary[origin[1], x] == 1:
        x_axis_coords.append((x, origin[1]))

# Detect all endpoints in the bitmap
def find_endpoints(binary):
    endpoints = []
    # Start from origin
    for x in range(binary.shape[0]-1):
        for y in range(binary.shape[1]-1, -1, -1):
            count = 0

            # If there is only one adjacent colored pixel, then it is an endpoint
            for dy, dx in directions:
                ny, nx = y+dy, x+dx
                if 0 <= ny < binary.shape[0] and 0 <= nx < binary.shape[1]:
                    if binary[y, x] == 1 and binary[ny, nx] == 1:
                        count += 1
            if count == 1 and (x, y) not in y_axis_coords and (x, y) not in x_axis_coords:
                endpoints.append((x, y))
    
    return endpoints

endpoints = find_endpoints(binary)
print(endpoints)

# Find coordinates for short line
def find_short_line_coords(endpoint):
    x0 = endpoint[0]
    y0 = endpoint[1]

    count = 0
    x, y = x0, y0
    tracking = [(x, y)]

    # Find coordinate with distance 5 from endpoint along the line
    while count <= 7:
        for dy, dx in directions:
            ny, nx = y+dy, x+dx
            if 0 <= ny < binary.shape[0] and 0 <= nx < binary.shape[1]:
                if binary[ny, nx] == 1 and (nx, ny) not in tracking:
                    tracking.append((nx, ny))
                    x, y = nx, ny
                    count += 1

    return [(x0, y0), (x, y)]

# Find short line from endpoint + near_coords. This will help later in finding
# the matching endpoint
def find_short_line(near_coords):
    endpoint = near_coords[0]
    near_coord = near_coords[1]

    dy = abs(endpoint[1] - near_coord[1])
    dx = endpoint[0] - near_coord[0]

    slope = round(dy / dx, 2)
    y_intercept = round(y - slope * x, 2)

    return (slope, y_intercept)

# # Find endpoint that is nearest/close to what would make sense from short line obtained
# def find_matching_endpoint(endpoint, endpoint_list, line):
#     line_endpoints = [endpoint]

#     slope = line[0]
#     y_intercept = line[1]

#     for ep in endpoint_list:
#         if ep != (endpoint[0], endpoint[1]):
#             supposed_y = slope * ep[0] + y_intercept
#             # If the distance between the 'supposed_y' is less than 5
#             # Might/should change to nearest coordinate of ep to supposed_y
#             if abs(supposed_y - ep[1]) <= 5:
#                 line_endpoints.append((ep[0], ep[1]))
    
#     return line_endpoints

def find_matching(line, ep_lines):
    for ep_line in ep_lines:
        # if ep_lines.index(line) != ep_lines.index(ep_line) # and 
        print(line)
        print(ep_line)
        if ep_lines == line:
            print("pass")
            return (line, ep_line)

# Determine slope and y-intercept from endpoints of all the lines
def lines(endpoints):
    # Find short lines for each point
    ep_lines = []
    for ep in endpoints:
        short_line = find_short_line(find_short_line_coords(ep))
        ep_lines.append(short_line)

    lines = []
    for line in ep_lines:
        matching_lines = find_matching(line, ep_lines)
        lines.append(matching_lines)
    
    return lines

lines = lines(endpoints)
print(lines)