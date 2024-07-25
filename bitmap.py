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
        if 0 <= ny < arr.shape[0] and 0 <= nx < arr.shape[1]:
            sum += arr[ny, nx]

    return sum

# Addition of 8 pixels around each pixel of layer_1
def layer_2(binary):

    layer_2_arr = np.zeros_like(binary, dtype=np.uint8)

    # Assign sum of surrounding pixels to layer_2_arr
    for y in range(binary.shape[0]):
        for x in range(binary.shape[1]):
            layer_2_arr[y,x] = sum(binary, y, x)
    
    return layer_2_arr

# Average activation of 1 layer of units around unit Ui
def A(arr, y, x):
    return sum(arr, y, x) / 8

# Extract notable features using formula
def layer_3(layer_2_arr):
    layer_3_arr = np.zeros_like(layer_2_arr, dtype=np.float32)
    temp = np.zeros_like(layer_2_arr, dtype=np.float32)

    for y in range(layer_2_arr.shape[0]):
        for x in range(layer_2_arr.shape[1]):
            av_activation = A(layer_2_arr, y, x)
            temp[y,x] = round(av_activation, 1)

            if layer_2_arr[y,x] != 0 and av_activation != 0:
                threshold = layer_2_arr[y,x] / round(av_activation, 1) - 1
                layer_3_arr[y,x] = round(threshold, 1)
            else:
                layer_3_arr[y,x] = 0
    print(temp)

    return layer_3_arr




# Declare bitmap image
image_path = 'Bitmaps/BM3.bmp'
image = Image.open(image_path).convert('1')

# Binary array
binary = layer_1(image)
print(binary)

# Layer 2
## Same name? Feel like I should have binary as a parameter
layer_2_arr = layer_2(binary)
print(layer_2_arr)

layer_3_arr = layer_3(layer_2_arr)
print(layer_3_arr)