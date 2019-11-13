#
# Authors: Kevin Carlos and Aditya Sidher
# Details: This file contains the implementation for Experiment 1

from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt


def Experiment1():
    # PartA()
    # PartB()
    # PartC()
    
#******************Part A******************#
def PartA():
    data = np.array([2, 3, 4, 4])
    N = 2
    isign = -1
    plotFunction(data, "./data_output/Experiment1/Exp1a", 'x', 'y', 'Original signal of f = [2,3,4,4]')
    
    # Push the array right since data[0] isn't used
    # divide by nn or 1/N for normalization
    newData = np.insert(data/N, 0, 0.0)
    print(newData)

    # Do fft to data
    retData = fft(newData, N, isign)

    # Plot the output without 0
    retData = np.delete(retData, 0)
    plotFunction(retData, "./data_output/Experiment1/Exp1aFFT", 'x', 'y', 'FFT signal of f = [2,3,4,4]')

    magnitudeData = getMagnitude(retData, N)
    plotFunction(magnitudeData, "./data_output/Experiment1/Exp1aMagnitudeFFT", 'x', 'y', 'Magnitude FFT signal of f = [2,3,4,4]')

    retData = np.insert(retData, 0, 0)

    # Do Inverse FFT
    retData = fft(retData, N, 1)

    # turn the Array back to size 4 instead of 5
    retData = np.delete(retData,0) 

#******************Part B******************#
def PartB():
    # N = 64x2
    N = 64
    isign = -1

    partb = generateCosine()

    # Push the array right since data[0] isn't used
    partb2 = np.insert(partb, 0, 0.0)

    # Do fft to data
    partb3 = fft(partb2/N, N, isign) 

    # Delete first element and shift everything left by N
    partb3 = np.delete(partb3, 0)

    partb3 = changeAmplitudeFrequency(partb3)

   
    # print(retData)
    plotFunction(partb3, "./data_output/Experiment1/cosFFT", 'Sample(N)', 'Amplitude', 'Fourier Transform of Cosine')

    magnitudeData = getMagnitude(partb3, N)
    plotFunction(magnitudeData, "./data_output/Experiment1/cosMagnitudeFFT", 'x', 'y', 'Magnitude Fourier Transform of Cosine')

    # Shift Everything back left by N and then add a 0 to the beginning
    partb3 = changeAmplitudeFrequency(partb3)
    partb3 = np.insert(partb3, 0 , 0)

    # Do Inverse FFT
    partb3 = fft(partb3, N, 1)

    # turn the Array back to size 4 instead of 5
    partb3 = np.delete(partb3, 0) 
    plotFunction(partb3, "./data_output/Experiment1/cosOriginal", 'Sample(N)', 'Amplitude', 'Inverse Fourier Transform of Cosine')

#******************Part C******************#
def PartC():
   
    partc = np.loadtxt('./data_input/Rect_128.dat')

    plotFunction(partc, "./data_output/Experiment1/Exp1c", 'x', 'y', 'Original signal of Rect_128.dat')

    # N = 64x2
    N = 64
    isign = -1

    # Push the array right since data[0] isn't used
    partc = np.insert(partc, 0, 0.0)

    # Do fft to data
    partc = fft(partc/N, N, isign) 

    # Delete first element and shift everything left by N
    partc = np.delete(partc, 0)
    partc = changeAmplitudeFrequency(partc)

    # magnitudeData = getMagnitude(partc, N)
    # plotFunction(magnitudeData, "./data_output/Experiment1/RectMagnitudeFFT", 'x', 'y', 'Magnitude Fourier Transform of Rect_128.dat')

    # print(retData)
    plotFunction(partc, "./data_output/Experiment1/RectFFT", 'Sample(N)', 'Amplitude', 'Fourier Transform of Rect_128.dat')

    # Shift Everything back left by N and then add a 0 to the beginning
    partc = changeAmplitudeFrequency(partc)
    partc = np.insert(partc, 0 , 0)

    # Do Inverse FFT
    partc = fft(partc, N, 1)

    # turn the Array back to size 4 instead of 5
    partc = np.delete(partc, 0) 
    plotFunction(partc, "./data_output/Experiment1/RectOriginal", 'Sample(N)', 'Amplitude', 'Inverse Fourier Transform of Rect_128.dat')


    

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
            wr =  wr * wpr - wi * wpi + wr
            wi = wi * wpr + wtemp * wpi + wi
        mmax = istep
    return data


# Will Swap array[data1] with array[data2]
def SWAP(array, data1, data2):
    temp1 = array[data1]
    array[data1] = array[data2]
    array[data2] = temp1
    return array


# Part b
def generateCosine():
    cosineData = np.array([])

    # u = magnitude | N = samples or normalization
    u = 8
    N = 128
    phi = 20.0
    
    x = np.arange(N)
    y = np.cos((2*math.pi*u*x)/N + phi)
    fig = plt.figure()
    plt.plot(x,y)
    plt.title('Cosine Function')
    plt.xlabel('Sample(N)')
    plt.ylabel('Amplitude')
    plt.savefig("./data_output/Experiment1/cos.png")
    return y


def changeAmplitudeSpatial(array):
    for i in range(0, array.size, 1):
        array[i] = array[i]*((-1)**i)
    return array

def changeAmplitudeFrequency(array):
    array = np.roll(array, array.size//2)
    return array

def plotFunction(array, name, xlabel, ylabel, title):
    fig = plt.figure()
    plt.title(title)
    plt.plot(np.arange(array.size), array)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(name + ".png")

# get the Magnitude of the Fourier transform For "Fun"
def getMagnitude(array, N):
    size = N*2
    for rows in range(size):
            val = array[rows]
            val = abs(val)
            array[rows] = val
    return array

# maskImage = Image.open("./data_input/sf.pgm")
Experiment1()