#
# Authors: Kevin Carlos and Aditya Sidher
# Details: This file contains the implementation for Experiment 1

from PIL import Image
import numpy as np
import math


prewittMaskX = np.array([[-1, -1, -1],
                         [ 0,  0,  0],
                         [ 1,  1,  1]], np.int32)


def Experiment1():
    data = np.array([2, 3, 4, 4])
    nn = 1
    isign = -1
    retData = fft(data-1,nn,isign)
    print(retData)
    retData = fft(retData-1, nn, 1)
    print(retData)

def fft(data1 , nn, isign):
    data = data1
    n = mmax = m = j = istep = i = 0
    wtemp = wr = wpr = wpi = wi = theta = 0
    tempr = tempi = 0

    n = nn << 1
    j = 1
    for i in range(1, n, 2):
        if(j > 1):
           SWAP(data[j],data[i])
           SWAP(data[j+1], data[i+1])
        m = n >> 1
        while m >= 2 and j > m:
            j -= m
            m = m >> 1
        j += m
    mmax = 2
    while n > mmax:
        istep = mmax << 1
        theta = isign * (6.28318530717959/mmax)
        wtemp = math.sin(0.5 * theta)
        wpr = -2.0 * wtemp * wtemp
        wpi = math.sin(theta)
        wr = 1.0
        wi = 0.0
        for m in range(1, mmax, 2):
            for i in range(m, n + 1, istep):
                j = i + mmax
                tempr = wr * data[j] - wi * data[j+1]
                tempi = wr * data[j+1] + wi * data[j]
                data[j] = data[i] - tempr
                data[j+1] = data[i+1] - tempi
                data[i] += tempr
                data[i+1] += tempi
            wr = wtemp = wr * wpr - wi * wpi + wr
            wi = wi * wpr + wtemp * wpi + wi
        mmax = istep
    return data


def SWAP(data1, data2):
    temp1 = data1
    data1 = data2
    data2 = temp1

 
    
# maskImage = Image.open("./data_input/sf.pgm")
Experiment1()