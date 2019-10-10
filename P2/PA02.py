from PIL import Image
import numpy as np

def normalize(width, height, mask):    
    normalizeVal = width * height

    pixels = list(mask.getdata())
    pixels = [pixels[i * width: (i+1) * width] for i in range(height)]

    for rows in range(height):
        for cols in range(width):
            pixels[rows][cols] = ((pixels[rows][cols] / normalizeVal) * 255)
            boundCheck(rows, cols, width, height)
        break
    return pixels

def boundCheck(currRow, currCol, width, height):
    #truncate the height and width becasue we start our origin at the center
    #so if its 5x5 we will be going up and down 2 and left and right 2
    #that means the topright corner will be technically -2,-2 or
    #3 from the origin diagnally
    masktempHeight = height - 2 #example 3 to right go 1 to get to boundary
    masktempWidth = width - 2

    #actual image width = 5
    #Actual image width - masktempwidth == 0
    
    bounds = []
    # [left, right, top, bottom]

    #if we are going out of bounds in the left boundary
    if (tempWidth - currRow < 0):
        # print("Width - 2: ", tempWidth)
        # print("Row: ", currRow)
        bounds.append(1)
    else:
        bounds.append(0)

    #if we are going out of bounds in the right boundary
    if(currRow - tempWidth < 0):
        bounds.append(1)
    else:
        bounds.append(0)
        
    #if we are going out of bounds in the top boundary
    if (tempHeight - currCol < 0):
        bounds.append(1)
    else:
        bounds.append(0)

    #if we are going out of bounds in the bottom boundary
    if(currCol - tempHeight < 0):
        # print("Height - 1: ", tempHeight)
        # print("Column: ", currCol)
        bounds.append(1)
    else:
        bounds.append(0)
    
    print(currRow, currCol)
    print(bounds)

def Correlation(mask_size, mask):
    image = Image.open("./data_input/Image.pgm")
    # im.save("./data_output/Pattern.pgm")

    width = mask_size[0]
    height = mask_size[1]

    normalizedMask = normalize(width, height, mask)

    

    
    # center = []
    # center.append([width//2, height//2])

maskImage = Image.open("./data_input/Pattern.pgm")
Correlation(maskImage.size, maskImage)