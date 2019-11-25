#
# Authors: Kevin Carlos and Aditya Sidher
# Details: This file contains the implementation for Experiment 2

from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt


def Experiment2():
    # generateImg()
    DFT2D()
    
    
# Does the FFT of a 2D image
def DFT2D():
   
    image = Image.open("./data_input/lenna.pgm")
    pixels = list(image.getdata())
    width, height = image.size
    newImage = Image.new("L", (width, height))
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    # # N = 64x2
    N = (image.size[0] + image.size[1]) // 4
    isign = -1
    print(N, height, width)

    pixels = normalizeImage(pixels, height, width, N)
            
    # Iterate over all the rows and store it into test2D
    pixels = ApplyFFTRow(pixels, width, N, isign)
            
    # Iterate over all the columns and store it into pixels
    pixels = ApplyFFTCol(pixels, height, N, isign)
    
    minVal = 1000000000000000000000000000
    maxVal = -101010100000000000000000000
    # newImage = LinearScaleValues(newImage, maxVal, minVal, pixels, height, width)
    # newImage = LogScaleValues(newImage, maxVal, minVal, pixels, height, width)

    

    ################################## Do the reverse ##################################   
    # # Iterate over all the columns and store it into pixels
    # pixels = ApplyFFTCol(pixels, height, N, 1)

    # # Iterate over all the rows and store it into test2D
    # pixels = ApplyFFTRow(pixels, width, N, 1)
    # # pixels = changeAmplitudeSpatial(pixels, height, width, N, 1)
    # newImage = LinearScaleValues(newImage, maxVal, minVal, pixels, height, width)
                
   
    # for rows in range(height):
    #     for cols in range(width):
    #         val = int(pixels[rows][cols])
    #         newImage.putpixel((cols,rows), val)

    newImage.save("./data_output/Potato.png")


# Iterate over all the rows and store it into pixels
def ApplyFFTRow(pixels, width, N, isign):
    for i in range(width):
        if(isign == -1): # Forward
            test2D = np.array(pixels)[i, 0:width] # set test2D equal to the pixel row of i
            test2D = np.insert(test2D, 0, 0.0)  # Add 0 in the front because we don't use data[0]
            test2D = fft(test2D, N, isign) # Do the fft on the current Row
            test2D = np.delete(test2D, 0) # Delete data[0]
            test2D = changeAmplitudeFrequency(test2D, N) # Move the entire 1-D array over by N
        elif(isign == 1): # Inverse
            test2D = np.array(pixels)[i, 0:width] # set test2D equal to the pixel row of i
            test2D = changeAmplitudeFrequency(test2D, N) # Move the entire 1-D array over by N
            test2D = np.insert(test2D, 0, 0.0)  # Add 0 in the front because we don't use data[0]
            test2D = fft(test2D/N, N, 1) # Do the Inverse fft on the current Row
            test2D = np.delete(test2D, 0) # Delete data[0]
        else:
            print("Error isign can only be 1 or -1, exiting.")
            break

        # Now place test2D into the current row of pixels
        for j in range(width):  
            pixels[i][j] = test2D[j]

    return pixels

# Iterate over all the columns and store it into pixels
def ApplyFFTCol(pixels, height, N, isign):
    for i in range(height):
        if(isign == -1): # Forward
            test2D = np.array(pixels)[0:height, i]
            test2D = np.insert(test2D, 0, 0.0)
            test2D = fft(test2D, N, isign) 
            test2D = np.delete(test2D, 0)
            test2D = changeAmplitudeFrequency(test2D, N)
        elif(isign == 1): # Inverse
            test2D = np.array(pixels)[0:height, i]
            test2D = changeAmplitudeFrequency(test2D, N)
            test2D = np.insert(test2D, 0, 0.0)
            test2D = fft(test2D/N, N, isign) 
            test2D = np.delete(test2D, 0)
        else:
            print("Error isign can only be 1 or -1, exiting.")
            break

        for j in range(height):
            pixels[j][i] = test2D[j]
    return pixels

# Scale the image Linearly through min max values 
def LinearScaleValues(img, maxVal, minVal, arrayImage, Height, Width):
    
    # find Min Max
    for rows in range(Height):
        for cols in range(Width):
            # find Min Max Values
            if (arrayImage[rows][cols] > maxVal):
                maxVal = arrayImage[rows][cols]
            if (arrayImage[rows][cols] < minVal):
                minVal = arrayImage[rows][cols]

    scalar = 255 / maxVal
    scalar = round(scalar, 10)
    for rows in range(Height):
        for cols in range(Width):
            val = arrayImage[rows][cols]
            val = int(val * scalar)
            img.putpixel((cols, rows), val)
            arrayImage[rows][cols] = val
    
    return img

#Log Scale the images and then bring the values back in range from 0 - 255
def LogScaleValues(img, maxVal, minVal, arrayImage, Height, Width):
    img = LinearScaleValues(img, maxVal, minVal, arrayImage, Height, Width)

    # Gets the Magnitude of the image
    arrayImage = getMagnitude(arrayImage, Height, Width)
    for rows in range(Height):
        for cols in range(Width):
            val = arrayImage[rows][cols]
            val = int(math.log(1 + (abs(val))))
            img.putpixel((cols, rows), val)
            arrayImage[rows][cols] = val
    img = LinearScaleValues(img, maxVal, minVal, arrayImage, Height, Width)        
    

    return img


# Fast Fourier Transform for Discrete 1-D Array
def fft(data, nn, isign):
    n = mmax = m = j = istep = i = 0
    wtemp = wr = wpr = wpi = wi = theta = 0.0
    tempr = tempi = float(0)

    n = nn << 1
    j = 1
    for i in range(1, n, 2):
        if(j > i):
            data = SWAP(data, j, i)
            data = SWAP(data, j+1, i+1)
        m = n >> 1
        while (m >= 2 and j > m):
            j -= m
            m = m >> 1
        j += m
    mmax = 2
    while (n > mmax):
        istep = mmax << 1
        theta = isign * (6.28318530717959/mmax)
        wtemp = math.sin(0.5 * theta)
        wpr = -2.0 * wtemp * wtemp
        wpi = math.sin(theta)
        wr = 1.0
        wi = 0.0
        for m in range(1, mmax, 2): #start at 1 because 0 isn't used
            for i in range(m, n+1, istep):
                j = i + mmax
                tempr = (wr * data[j]) - (wi * data[j+1])
                tempi = wr * data[j+1] + wi * data[j]
                data[j] = data[i] - tempr 
                data[j+1] = data[i+1] - tempi
                data[i] += tempr
                data[i+1] += tempi
            wtemp = wr
            wr = wr * wpr - wi * wpi + wr
            wi = wi * wpr + wtemp * wpi + wi

        mmax = istep
    return data


# Will Swap array[data1] with array[data2]
def SWAP(array, data1, data2):
    temp1 = array[data1]
    array[data1] = array[data2]
    array[data2] = temp1
    return array

# Translate to the center of the frequency in the spatial domain f(x)
def normalizeImage(array, Height, Width, N):
    for i in range(0,  Height, 1):
        for j in range(0, Width, 1):
            val = float(array[i][j] / N)
            array[i][j] = float(val)
    return array

# Translate to the center of the frequency in the Frequency domain F(u)
def changeAmplitudeFrequency(array, N):
    array = np.roll(array, N)
    return array


# get the Magnitude of the Fourier transform For Fun
def getMagnitude(array, Height, Width):
    for rows in range(Height):
        for cols in range(Width):
            val = array[rows][cols]
            val = abs(val)
            array[rows][cols] = val
    return array



Experiment2()