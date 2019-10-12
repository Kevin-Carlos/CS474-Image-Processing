from PIL import Image
import numpy as np

def Correlation(mask_size, mask):
    image = Image.open("./data_input/Image.pgm")
    # im.save("./data_output/Pattern.pgm")

    width = mask_size[0]
    height = mask_size[1]

    normalizedMask = Normalize(width, height, mask)

    MapCorrelation(mask, image, normalizedMask)
    

def Normalize(width, height, mask):    
    normalizeVal = width * height

    pixels = list(mask.getdata())
    pixels = [pixels[i * width: (i+1) * width] for i in range(height)]

    for rows in range(height):
        for cols in range(width):
            pixels[rows][cols] = ((pixels[rows][cols] / normalizeVal)) # I took out the * 255 idk if its needed :shrugs:
    return pixels

def MapCorrelation(mask, image, normalizedMask):
    # Initiffize pixel values
    imagePixels = list(image.getdata())
    imagePixels = [imagePixels[i * image.size[0]: (i+1) * image.size[0]] for i in range(image.size[1])]
    
    # Allocate a new image type of same size
    correlatedMap = Image.new("L", (image.size[0], image.size[1]))
    # print("Size:", correlatedMap.size)
    # correlatedPixels = list(correlatedMap.getdata())
    # correlatedPixels = [correlatedPixels[i * image.size[0]: (i+1) * image.size[0]] for i in range(image.size[1])]


    # This loop is for the image itself, going from 0 to whatever the end is
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            
            # This goes into a funciton to do the summation/apply the mask for the i, j pixel position
            value = int(ApplyMask(i, j, mask, image, normalizedMask, imagePixels))

            try:
                correlatedMap.putpixel((i,j), value)
                # correlatedPixels[i][j] = value / 64.5
            except:
                pass
            
    # print(correlatedPixels)

    correlatedMap.save("./data_output/Correlation.pgm")
    
    
            


def ApplyMask(i, j, mask, image, maskPixels, imagePixels):
    summation = 0

    # This loop loops from -K/2 to K/2 on the mask and calculates the corresponding coordinate to map it to, so 0,0 on the image is -41, -27 for the pattern
    for row in range(-(mask.size[0] // 2), mask.size[0] // 2):
        for col in range(-(mask.size[1] // 2), mask.size[1] // 2):
            imageCoordW = i - (mask.size[0] // 2)
            imageCoordH = j - (mask.size[1] // 2)

            # Make sure the coord is within bounds otherwise just call it 0
            try:
                if (imageCoordW > 0 and imageCoordW < image.size[0] and imageCoordH > 0 and imageCoordH < image.size[1]):
                    summation = summation + (maskPixels[row][col] * imagePixels[imageCoordW][imageCoordH])
                    summation = summation // (i*j)
            except:
                summation = summation + 0

    return summation 


maskImage = Image.open("./data_input/Pattern.pgm")
Correlation(maskImage.size, maskImage)