#
# Authors: Kevin Carlos and Aditya Sidher
# Details: This file contains the implementation for Smoothing "lenna" and "sf" using 
# 7x7 and 15x15 averaging filters and 7x7 and 15x15 Guassian filters

from PIL import Image
import numpy as np
import math


prewittMaskX = np.array([[-1, -1, -1],
                         [ 0,  0,  0],
                         [ 1,  1,  1]], np.int32)

prewittMaskY = np.array([[-1, 0, 1],
                        [ -1, 0, 1],
                        [ -1, 0, 1]], np.int32)

SobelMaskX = np.array([[-1, -2, -1],
                       [ 0,  0,  0],
                       [ 1,  2,  1]], np.int32)

SobelMaskY = np.array([[-1, 0, 1],
                       [ -2, 0, 2],
                       [ -1, 0, 1]], np.int32)

LaplacianMask = np.array([[ 0,  1, 0],
                          [ 1, -4, 1],
                          [ 0,  1, 0]], np.int32)

def Smoothing(mask_size, image):
    imageX = Image.open("./data_output/Q04/sf_Prewitt_X.pgm")
    imageY = Image.open("./data_output/Q04/sf_Prewitt_Y.pgm")

    # MapSharpening(LaplacianMask, image)

    Gradient(imageX, imageY)
 

def Gradient(imageX, imageY):

    # Initialize new Image to store the Average pixels
    combinedImage = Image.new("L", (imageX.size[0], imageX.size[1]))
    
    # new array to combine the two
    arrayImageX = np.array(imageX, np.int32)
    arrayImageY = np.array(imageY, np.int32)

    combinedArray = np.array(imageX, np.int32)

    maxVal = 0
    minVal = 4546465165

    for rows in range(imageX.size[1]): #256 Row
        for cols in range(imageX.size[0]): #256 Col
            
            valX = arrayImageX[rows][cols]
            valY = arrayImageY[rows][cols]

            # Calculate the Gradient
            combinedArray[rows][cols] = math.sqrt((valX)**2 + (valY)**2)

            # find Min Max Values
            if (arrayImageX[rows][cols] > maxVal):
                maxVal = arrayImageX[rows][cols]
            if (arrayImageX[rows][cols] < minVal):
                minVal = arrayImageX[rows][cols]

    newImage = ScaleValues(combinedImage, maxVal, minVal, combinedArray)

    newImage.save("./data_output/Q04/sf_Prewitt_GradientMagnitude.pgm")

def MapSharpening(mask, image):
    # Initialize new Image to store the Average pixels
    newImage = Image.new("L", (image.size[0], image.size[1]))

    # new array to store the summation values
    arrayImage = np.array(newImage, np.int32)

    maxVal = 0
    minVal = 4546465165

    for rows in range(image.size[1]): #256 Row
        for cols in range(image.size[0]): #256 Col
            
            value = int(ApplyMask(mask, image, cols, rows))
            arrayImage[rows][cols] = value
    
            # find Min Max Values
            if (arrayImage[rows][cols] > maxVal):
                maxVal = arrayImage[rows][cols]
            if (arrayImage[rows][cols] < minVal):
                minVal = arrayImage[rows][cols]

    
    newImage = ScaleValues(newImage, maxVal, minVal, arrayImage)

    newImage.save("./data_output/Q04/sf_Laplacian.pgm")

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


# Averaging summation on the mask overlay and Pad area around
def ApplyMask(mask, image, imageCols, imageRows):
    summation = 0

    for maskRows in range(mask.shape[1]): #mxm row
        for maskCols in range(mask.shape[0]): #mxm col

            # Get the image col and row
            coordCol = imageCols - maskCols
            coordRow = imageRows - maskRows

            # Check right and bottom Bounds
            checkBottom = image.size[1] - (coordRow)
            checkRight = image.size[0] - (coordCol)

            # check all bounds that are negative
            if(coordCol >= 0 and coordRow >= 0 and checkBottom >= 0 and checkRight >= 0):
                try:
                    F = image.getpixel((coordCol, coordRow))
                    W = mask[maskRows][maskCols]
                    summation = summation + (F * W)
                    
                except:
                    summation += 0

            else:     
                summation += 0

    return summation
    
maskImage = Image.open("./data_input/sf.pgm")
Smoothing(maskImage.size, maskImage)