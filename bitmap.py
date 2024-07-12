from PIL import Image
import numpy as np

# Convert bitmap image to array
def layer_1(image):

    # Get pixels as array
    pixels = np.array(list(image.getdata()))

    # Binary array of pixels
    binary = np.zeros_like(pixels, dtype=np.uint8)
    binary[pixels == 255] = 1 
    binary = binary.reshape(image.height, image.width)
   
    return binary

# Sum of surrounding 8 neighboring pixels of pixel (x, y)
def sum(arr, y, x):
    # Define directions for 8 neighboring pixels
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    sum = 0
    for dy, dx in directions:
        ny, nx = y + dy, x + dx
        if 0 <= ny < height and 0 <= nx < width:
            sum += arr[ny, nx]

    return sum

# Addition of 8 pixels around each pixel of layer_1
def layer_2():

    layer_2_arr = np.zeros_like(binary, dtype=np.uint8)

    # Assign sum of surrounding pixels to layer_2_arr
    for y in range(height):
        for x in range(width):
            layer_2_arr[x,y] = sum(binary, y, x)
    
    return layer_2_arr

# Average activation of 1 layer of units around unit Ui
def A(arr, y, x):
    average_activ = sum(arr, y, x) / 8
    return average_activ

# Extract notable features using formula
def layer_3():
    layer_3_arr = np.zeros_like(layer_2_arr, dtype=np.float32)
    temp = np.zeros_like(layer_2_arr, dtype=np.float32)

    for y in range(height):
        for x in range(width):
            # temp[x,y] = round(A(layer_2_arr, y, x), 1)
            threshold = (layer_2_arr[x,y] / A(layer_2_arr, y, x)) - 1
            layer_3_arr[x,y] = round(threshold, 1)
    # print(temp)

    return layer_3_arr



# Declare bitmap image
image_path = 'CaMeRa/Bitmaps/BM3.bmp'
image = Image.open(image_path).convert('1')

# Binary array
binary = layer_1(image)

# Get width & height of size
width, height = image.size

# Layer 2
## Same name? Feel like I should have binary as a parameter
layer_2_arr = layer_2()
# print(layer_2_arr)

layer_3_arr = layer_3()
print(layer_3_arr)