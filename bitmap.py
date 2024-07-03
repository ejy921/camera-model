from PIL import Image
import numpy as np

image_path = 'Bitmaps/BM3.bmp'
image = Image.open(image_path).convert('1')

print(image.format, image.size, image.mode)
pixels = np.array(list(image.getdata()))
pixels = pixels.reshape(image.height, image.width)
print(pixels)

width, height = image.size

binary = np.zeros_like(pixels, dtype=np.uint8)
binary[pixels == 255] = 1 

for y in range(height):
    for x in range(width):
        