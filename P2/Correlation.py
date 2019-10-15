#
# Authors: Kevin Carlos and Aditya Sidher
# Details: This file contains the implementation for correlating a pattern image 
#             and  a source image

from PIL import Image
import numpy as np
import math

def Correlation(mask_size, mask):
    image = Image.open("./data_input/Image.pgm")

    normalizedMask = NormalizeMask(mask)

    MapCorrelation(normalizedMask, image)


def NormalizeMask(mask):
    summation = 0

    # Convert image from Image type to list of pixels
    pixels = list(mask.getdata())
    width, height = mask.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    # Find the sum of the elements in the mask
    for i in range(mask.size[0]):
        for j in range(mask.size[1]):
            value = mask.getpixel((i,j))
            summation += value
    
    # All values should add up to 1
    for i in range(mask.size[0]):
        for j in range(mask.size[1]):
            value = pixels[j][i]
            value = value / summation
            pixels[j][i] = value
    
    return pixels


def MapCorrelation(mask, image):
    # Initialize new Image to store the correlated pixels
    correlatedImage = Image.new("L", (image.size[0], image.size[1]))

    maxVal = 0
    minVal = 4546465165

    for rows in range(image.size[1]): #288 Row
        for cols in range(image.size[0]): #442 Col
            
            value = int(ApplyMask(mask, image, cols, rows))
            
            correlatedImage.putpixel((cols, rows), value)

            # find Min Max Values
            if (correlatedImage.getpixel((cols, rows)) > maxVal):
                maxVal = correlatedImage.getpixel((cols, rows))
            if (correlatedImage.getpixel((cols, rows)) < minVal):
                minVal = correlatedImage.getpixel((cols, rows))

    correlatedImage = ScaleValues(correlatedImage, maxVal, minVal)

    correlatedImage.save("./data_output/Q01/Correlation.pgm")

# Get the values back from [0, 255]
def ScaleValues(img, maxVal, minVal):
    scalar = 255 / maxVal
    scalar = round(scalar, 2)

    for cols in range(img.size[0]):
        for rows in range(img.size[1]):
            val = img.getpixel((cols, rows))

            val = int(val * scalar)

            img.putpixel((cols, rows), val)
    
    return img

# Correlation summation on the mask overlay and Pad area around
def ApplyMask(mask, image, imageCols, imageRows):
    summation = 0

    mask = np.asarray(mask)

    for maskRows in range(-(mask.shape[1] // 2), mask.shape[1] // 2): #55 = 27
        for maskCols in range(-(mask.shape[0] // 2), mask.shape[0] // 2): #83 = 41

            # Get the image col and row
            coordCol = maskCols + imageCols
            coordRow = maskRows + imageRows

            # Check right and bottom Bounds
            checkBottom = image.size[1] - (coordRow)
            checkRight = image.size[0] - (coordCol)
            
            # Get the original row and col for the mask, not -41,-27 but 0,0
            colMask = maskCols + (mask.shape[0] // 2)
            rowMask = maskRows + (mask.shape[1] // 2)

            # print(rowMask, colMask)

            # check all bounds that are negative
            if(coordCol >= 0 and coordRow >= 0 and checkBottom >= 0 and checkRight >= 0):
                try:
                    F = image.getpixel((coordCol, coordRow))
                    W = mask[rowMask][colMask]
                    summation = summation + (F * W)
                except:
                    summation += 0
            else:
                summation += 0

    return summation

maskImage = Image.open("./data_input/Pattern.pgm")
Correlation(maskImage.size, maskImage)