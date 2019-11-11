#
# Authors: Kevin Carlos and Aditya Sidher
# Details: This file contains the implementation for Experiment 1

from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt


def Experiment1():
    data = np.array([2, 3, 4, 4])
    N = 2
    isign = -1

     #******************Part A******************#
    # Push the array right since data[0] isn't used
    # divide by nn or 1/N for normalization
    data = np.append(data/N,np.array([0]))
    newData = shiftLeft(data)

    # Do fft to data
    retData = fft(newData, N, isign) 
    print(retData)

    # Do Inverse FFT
    retData = fft(retData, N, 1)

    # turn the Array back to size 4 instead of 5
    retData = np.delete(retData,0) 

    
    print(retData)

    #******************Part B******************#
    # N = 64x2
    N = 64
    partb = generateCosine()
    print(partb)
    print()
    # Push the array right since data[0] isn't used
    partb1 = np.append(partb/N,np.array([0]))
    partb2 = shiftLeft(partb1)

    # Do fft to data
    partb3 = fft(partb2, N, isign) 
    # print(retData)
    plotFunction(partb3, "./cosFFT")

    # Do Inverse FFT
    partb3 = fft(partb3, N, 1)

    # turn the Array back to size 4 instead of 5
    partb3 = np.delete(partb3, 0) 

    print()
    print(partb3)
    plotFunction(partb3, "./cosOriginal")
    

def shiftLeft(data):
    for i in range(data.size-1, 0, -1):
        data[i] = data[i-1]
    data[0] = 0
    return data
    

def fft(data, nn, isign):
    n = mmax = m = j = istep = i = 0
    wtemp = wr = wpr = wpi = wi = theta = 0.0
    tempr = tempi = float(0)

    n = nn << 1
    j = 1
    for i in range(1, n, 2):
        if(j > i):
           SWAP(data[j],data[i])
           SWAP(data[j+1], data[i+1])
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
            wr = wtemp = wr * wpr - wi * wpi + wr
            wi = wi * wpr + wtemp * wpi + wi
        mmax = istep
    return data

def SWAP(data1, data2):
    temp1 = data1
    data1 = data2
    data2 = temp1


# Part b
def generateCosine():
    cosineData = np.array([])

    # u = magnitude | N = samples or normalization
    u = 8
    N = 128
    
    x = np.arange(N)
    y = np.cos((2*math.pi*u*x)/N)
    # print(y)
    fig = plt.figure()
    plt.plot(x,y)
    plt.xlabel('sample(N)')
    plt.ylabel('cosine(f(x))')
    plt.savefig("./cos.png")
    return y

def plotFunction(array, name):
    # array = np.insert(array, array.size//2, array[1])
    # array = np.delete(array, 1)

    # print()
    # print(array)
    fig = plt.figure()
    plt.plot(np.arange(array.size), array)
    plt.xlabel('sample(N)')
    plt.ylabel('cosine(FFT)')
    plt.savefig(name + ".png")


# maskImage = Image.open("./data_input/sf.pgm")
Experiment1()
#generateCosine()