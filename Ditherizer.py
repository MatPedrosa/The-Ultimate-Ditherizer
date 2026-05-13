from PIL import Image
import numpy as np
import colour

input_image = Image.open("USC-SIPI-4.2.06.tiff").convert("RGB")
input_sRGB = np.asarray(input_image)
input_Oklab = colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(input_sRGB / 255))

def OklabDistance(color1, color2):
    diff = color1 - color2
    return np.dot(diff, diff)

output_image = Image.new(mode="1", size = input_image.size)
output_pixels = output_image.load()
for j in range(input_image.height):
    for i in range(input_image.width):
        if OklabDistance(input_Oklab[j, i, 0], np.array([0, 0, 0])) > OklabDistance(input_Oklab[j, i, 0], np.array([1.00000174e+00, 2.28547958e-06, -1.13652666e-04])):
            output_pixels[i, j] = 1
        else:
            output_pixels[i, j] = 0

output_image.show()
