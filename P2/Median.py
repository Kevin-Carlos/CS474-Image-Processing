#
# Authors: Kevin Carlos and Aditya Sidher
# Details: This file contains the implementation for Median filtering "lenna" 
# and "boat" using  7x7 and 15x15 averaging/median filters

from PIL import Image
import numpy as np
import math
import random

# 7x7
averagingMask7 = np.array([[1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1],                
                           [1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1]], np.float32)

                
averagingMask15 = np.array(
    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],                
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]], np.float32)


def Median(mask_size, image):

    # corruptedImage =  Corrupt(image, 255) 
    # corruptedImage = Corrupt(corruptedImage, 0)
    corruptedImage = Image.open("./data_output/Q03/lenna_Corrupted30.pgm")
    MapMedian(averagingMask15, corruptedImage)
    

def MapMedian(mask, image):
    # Initialize new Image to store the Median pixels and Pad area around
    newImage = Image.new("L", (image.size[0], image.size[1]))

    # new array to store the summation values
    arrayImage = np.array(newImage, np.int32)

    maxVal = 0
    minVal = 4546465165

    for rows in range(image.size[1]): #256 Row
        for cols in range(image.size[0]): #256 Col
            
            value = int(ApplyMask(mask, image, cols, rows))
            newImage.putpixel((cols, rows), value)

    
    # newImage = ScaleValues(newImage, maxVal, minVal, arrayImage)

    newImage.save("./data_output/Q03/lenna_Corrupted30_MED15x15.pgm")

# Get the values back from [0, 255]
def ScaleValues(img, maxVal, minVal, arrayImage):
    scalar = 255 / maxVal
    scalar = round(scalar, 2)

    for rows in range(arrayImage.shape[1]):
        for cols in range(arrayImage.shape[0]):
            val = arrayImage[rows][cols]
            # print(val)
            val = int(val * scalar)
            # print(val)
            img.putpixel((cols, rows), val)
    
    return img


# Averaging summation on the mask overlay
def ApplyMask(mask, image, imageCols, imageRows):
    summation = 0

    neighborhoodSize = mask.shape[0] * mask.shape[1]

    # print(neighborhoodSize)
    # new array to store the summation values mxm size list
    arrayMaskandImage = [neighborhoodSize]


    for maskRows in range(-(mask.shape[1] // 2), mask.shape[1] // 2):#m row
        for maskCols in range(-(mask.shape[0] // 2), mask.shape[0] // 2):#m col

            # Get the image col and row
            coordCol = maskCols + imageCols
            coordRow = maskRows + imageRows

            # Check right and bottom Bounds
            checkBottom = image.size[1] - (coordRow)
            checkRight = image.size[0] - (coordCol)
            
            # Get the original row and col for the mask, not -41,-27 but 0,0
            colMask = maskCols + (mask.shape[0] // 2)
            rowMask = maskRows + (mask.shape[1] // 2)

            # check all bounds that are negative
            if(coordCol >= 0 and coordRow >= 0 and checkBottom >= 0 and checkRight >= 0):
                try:
                    F = image.getpixel((coordCol, coordRow))
                    W = mask[rowMask][colMask]

                    # Multiple the image coord with the mask coord
                    summation = (F * W)

                    # Put the array into a list
                    arrayMaskandImage.append(summation)
                except:
                    summation = 0
                    arrayMaskandImage.append(summation)
            else:
                summation = 0
                arrayMaskandImage.append(summation)

    #sort the list and get the Median
    arrayMaskandImage.sort()
    Median = int(arrayMaskandImage[(neighborhoodSize + 1) // 2])

    return Median

# Function to Corrupt the image with val = 0 or 255
def Corrupt(image, val):
    # Corrupt the original image and make a new one
    newImage = Image.new("L", (image.size[0], image.size[1]))

    for rows in range(image.size[1]): #256 Row
        for cols in range(image.size[0]): #256 Col

            newImage.putpixel((cols, rows), image.getpixel((cols, rows)))

            # random number from 1 - 100
            randomVal = random.randint(1,100)

            # Determines what percentage of the image will be corrupted
            if(randomVal < 30):
                value = val
                newImage.putpixel((cols, rows), value)


    newImage.save("./data_output/Q03/lenna_Corrupted30.pgm")
    return newImage

maskImage = Image.open("./data_input/lenna.pgm")
Median(maskImage.size, maskImage)