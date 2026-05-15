from PIL import Image
import numpy as np
import colour

def sRGB_to_Oklab(color):
    return colour.XYZ_to_Oklab(colour.sRGB_to_XYZ(color / 255))

def Oklab_to_sRGB(color):
    return 255 * colour.XYZ_to_sRGB(colour.Oklab_to_XYZ(color))

def OklabSquaredDistance(color1, color2):
    diff = color1 - color2
    #calculating the actual distance would need a square root
    #but we don't need that if we're just comparing distances
    return np.dot(diff, diff)

def OklabQuantize(color, palette):
    distances = np.array([OklabSquaredDistance(color, item) for item in palette])
    sorted_indices = np.argsort(distances)
    return palette[sorted_indices[0]], sorted_indices


input_image = Image.open("Teste1.png").convert("RGB")
input_sRGB = np.asarray(input_image)
input_Oklab = sRGB_to_Oklab(input_sRGB)
#For some unknown reason, these image arrays are adderessed in the order (y, x)

color_palette_sRGB = np.asarray([
    [0, 0, 0],
    [255, 0, 0],
    [0, 255, 0],
    [0, 0, 255],
    [0, 255, 255],
    [255, 0, 255],
    [255, 255, 0],
    [255, 255, 255]
])
color_palette_Oklab = sRGB_to_Oklab(color_palette_sRGB)

output_Oklab = np.empty_like(input_Oklab)
for j in range(input_image.height):
    for i in range(input_image.width):
        #Test Floyd-Steinberg implementation
        output_Oklab[j, i] = tuple(OklabQuantize(input_Oklab[j, i], color_palette_Oklab)[0])
        current_error = output_Oklab[j, i] - input_Oklab[j, i]
        if i + 1 < input_image.width:
            input_Oklab[j, i + 1] -= 7 * current_error / 16
        if i + 1 < input_image.width and j + 1 < input_image.height:
            input_Oklab[j + 1, i + 1] -= current_error / 16
        if j + 1 < input_image.height:
            input_Oklab[j + 1, i] -= 5 * current_error / 16
        if i - 1 < input_image.width and j + 1 < input_image.height:
            input_Oklab[j + 1, i - 1] -= 3 * current_error / 16

output_sRGB = Oklab_to_sRGB(output_Oklab)
output_image = Image.fromarray(output_sRGB.astype('uint8'))
output_image.show()
