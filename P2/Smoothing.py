#
# Authors: Kevin Carlos and Aditya Sidher
# Details: This file contains the implementation for Smoothing "lenna" and "sf" using 
# 7x7 and 15x15 averaging filters and 7x7 and 15x15 Guassian filters

from PIL import Image
import numpy as np
import math

# 7x7
averagingMask7 = np.array([[1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1],                
                           [1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1],
                           [1, 1, 1, 1, 1, 1, 1]], np.float32)

                
averagingMask15 = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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

gaussianMask7 = np.array([[1, 1, 2, 2,  2, 1, 1],
                          [1, 2, 2, 4,  2, 2, 1],
                          [2, 2, 4, 8,  4, 2, 2],                
                          [2, 4, 8, 16, 8, 4, 2],
                          [2, 2, 4, 8,  4, 2, 2],
                          [1, 2, 2, 4,  2, 2, 1],
                          [1, 1, 2, 2,  2, 1, 1]], np.float32)


gaussianMask15 = np.array([[2, 2, 3,  4,  5,  5,  6,  6,  6,  5,  5,  4,  3,  2, 2],
                           [2, 3, 4,  5,  7,  7,  8,  8,  8,  7,  7,  5,  4,  3, 2],
                           [3, 4, 6,  7,  9,  10, 10, 11, 10, 10, 9,  7,  6,  4, 3],                
                           [4, 5, 7,  9,  10, 12, 13, 13, 13, 12, 10, 9,  7,  5, 4],
                           [5, 7, 9,  11, 13, 14, 15, 16, 15, 14, 13, 11, 9,  7, 5],
                           [5, 7, 10, 12, 14, 16, 17, 18, 17, 16, 14, 12, 10, 7, 5],
                           [6, 8, 10, 13, 15, 17, 19, 19, 19, 17, 15, 13, 10, 8, 6],
                           [6, 8, 11, 13, 16, 18, 19, 20, 19, 18, 16, 13, 11, 8, 6],
                           [6, 8, 10, 13, 15, 17, 19, 19, 19, 17, 15, 13, 10, 8, 6],
                           [5, 7, 10, 12, 14, 16, 17, 18, 17, 16, 14, 12, 10, 7, 5],
                           [5, 7, 9,  11, 13, 14, 15, 16, 15, 14, 13, 11, 9,  7, 5],
                           [4, 5, 7,  9,  10, 12, 13, 13, 13, 12, 10, 9,  7,  5, 4],
                           [3, 4, 6,  7,  9,  10, 10, 11, 10, 10, 9,  7,  6,  4, 3],
                           [2, 3, 4,  5,  7,  7,  8,  8,  8,  7,  7,  5,  4,  3, 2],
                           [2, 2, 3,  4,  5,  5,  6,  6,  6,  5,  5,  4,  3,  2, 2]], np.float32)

def Smoothing(mask_size, image):

    averagedMask = Average(averagingMask7)

    MapSmoothing(averagedMask, image)
    

def Average(mask):
    
    # Find the sum of the elements in the mask
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            value = mask[i][j]
            average = value / (mask.shape[0] * mask.shape[1])
            mask[i][j] = average
            

    return mask


def MapSmoothing(mask, image):
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

    newImage.save("./data_output/Q02/sf_7x7.pgm")

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

    for maskRows in range(-(mask.shape[1] // 2), mask.shape[1] // 2): #mxm row
        for maskCols in range(-(mask.shape[0] // 2), mask.shape[0] // 2): #mxm col

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
maskImage = Image.open("./data_input/sf.pgm")
Smoothing(maskImage.size, maskImage)