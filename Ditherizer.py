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

def OklabClosestColor(color, palette):
    distances = np.array([OklabSquaredDistance(color, item) for item in palette])
    sorted_indices = np.argsort(distances)
    return palette[sorted_indices[0]], sorted_indices


input_image = Image.open("C:\\Users\\mathe\\Documentos\\Projects\\ditherizer\\USC-SIPI-4.2.06.tiff").convert("RGB")
input_sRGB = np.asarray(input_image)
input_Oklab = sRGB_to_Oklab(input_sRGB)

color_palette_sRGB = np.asarray([[0, 0, 0], [255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 255, 255], [255, 0, 255], [255, 255, 0], [255, 255, 255]])
color_palette_Oklab = sRGB_to_Oklab(color_palette_sRGB)

output_Oklab = np.empty_like(input_Oklab)
for i, j in np.ndindex(input_Oklab.shape[:2]):
    output_Oklab[j, i] = tuple(OklabClosestColor(input_Oklab[j, i], color_palette_Oklab)[0])
    #if j == 0 : print(output_Oklab[i, j])

output_sRGB = Oklab_to_sRGB(output_Oklab)
output_image = Image.fromarray(output_sRGB.astype('uint8'))
output_image.show()
