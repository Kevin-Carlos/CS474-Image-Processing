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
            pixels[rows][cols] = ((pixels[rows][cols] / normalizeVal))
    return pixels

def MapCorrelation(mask, image, normalizedMask):
    # Initiffize pixel values
    imagePixels = list(image.getdata())
    imagePixels = [imagePixels[i * image.size[0]: (i+1) * image.size[0]] for i in range(image.size[1])]
    
    correlatedMap = Image.new("L", (image.size[0], image.size[1]))
    # print("Size:", correlatedMap.size)
    # correlatedPixels = list(correlatedMap.getdata())
    # correlatedPixels = [correlatedPixels[i * image.size[0]: (i+1) * image.size[0]] for i in range(image.size[1])]

    for i in range(image.size[0]):
        for j in range(image.size[1]):
            
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
    for row in range(-(mask.size[0] // 2), mask.size[0] // 2):
        for col in range(-(mask.size[1] // 2), mask.size[1] // 2):
            imageCoordW = i - (mask.size[0] // 2)
            imageCoordH = j - (mask.size[1] // 2)

            try:
                summation = summation + (maskPixels[row][col] * imagePixels[imageCoordW][imageCoordH])
            except:
                summation = summation + 0

    return summation


maskImage = Image.open("./data_input/Pattern.pgm")
Correlation(maskImage.size, maskImage)