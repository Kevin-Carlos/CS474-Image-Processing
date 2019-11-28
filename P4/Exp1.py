from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt
from FFT import *


def Experiment1():
  DFT2D()


# Does the FFT of a 2D image
def DFT2D():
   
    image = Image.open("./data_input/boy_noisy.pgm")
    pixels = list(image.getdata())
    width, height = image.size
    newImage = Image.new("L", (width, height))
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    # # N = height x width
    N = (newImage.size[0] + newImage.size[1]) // 4
    print(N, width, height)
    isign = -1
    pixels = normalizeImage(pixels, height, width, N)
            
    # Iterate over all the rows and store it into test2D
    pixels = ApplyFFTRow(pixels, width, N, isign)
            
    # Iterate over all the columns and store it into pixels
    pixels = ApplyFFTCol(pixels, height, N, isign)

    minVal = 1000000000000000000000000000
    maxVal = -101010100000000000000000000

    pixels = GBRF(pixels, 72, 6, width, height, False)

    
    # newImage = LinearScaleValues(newImage, maxVal, minVal, pixels, height, width)

    # newImage = LogScaleValues(newImage, maxVal, minVal, pixels, height, width)


    

    ################################## Do the reverse ##################################   
    # Iterate over all the columns and store it into pixels
    pixels = ApplyFFTCol(pixels, height, N, 1)

    # Iterate over all the rows and store it into test2D
    pixels = ApplyFFTRow(pixels, width, N, 1)

    # pixels = changeAmplitudeSpatial(pixels, height, width, N, 1)
    newImage = LinearScaleValues(newImage, maxVal, minVal, pixels, height, width)

                
    # # Only if we don't linearScale to see what it looks like.
    # for rows in range(height):
    #     for cols in range(width):
    #         val = int(pixels[rows][cols])
    #         val1 = int(pixels1[rows][cols])
    #         val2 = int(newPixels[rows][cols])

    #         newImage.putpixel((cols,rows), val)
    #         newImage1.putpixel((cols,rows), val1)
    #         newImage2.putpixel((cols,rows), val2)

    

    newImage.save("./data_output/New_noisy_boy.png")
    # newImage1.save("./data_output/GaussianRadius.png")



def GBRF(array, C0, W, Width, Height, PassReject=True):
    # center = 128 # math.sqrt((Width//2)**2 + (Height//2)**2)
    # newArray = array

    for i in range(Width):
      for j in range(Height):
        distanceToCenter = math.sqrt((i - (Width//2))**2 + (j - (Height//2))**2)
        # print(distanceToCenter, i, j, ((i - (Width//2))**2), ((j - (Height//2))**2))
        # print(distanceToCenter)
        
        # Gaussian Band Reject Filtering
        H = 1 - math.e**(-( (distanceToCenter - C0)**2 / (W)**2 )**2)
       
        # Band Pass = H_bp(u,v) = 1 - H_br
        if PassReject is True:
          H = 1 - H

        array[i][j] = array[i][j] * H
    return array

Experiment1()